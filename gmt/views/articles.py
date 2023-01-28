from bson import ObjectId
import markdown
from flask import Blueprint, abort, redirect, render_template, request, session, url_for
from datetime import datetime

from .. import mongo

bp = Blueprint("articles", __name__, url_prefix="/articles")


@bp.route("/<article_id>", methods=("POST", "GET"))
def article(article_id):
    article_db = mongo.db.articles.find_one({"_id": ObjectId(article_id)})
    # if article doesnt exists 404
    if not article_db:
        return render_template("404.html")

    if request.method == "POST":
        # DELETES ARTICLE
        if session.get("writer")["logged_in"] and article_db["author"]["email"] == session["writer"]["email"]:
            mongo.db.articles.delete_one({"_id": ObjectId(article_id)})
            return redirect(url_for("writers.portal"))

    content_md = markdown.markdown(article_db["content"])
    try:
        if session.get("writer")["logged_in"] and article_db["author"]["email"] == session["writer"]["email"]:
            return render_template("articles/article.html", article=article_db, content=content_md, edit=True)
    except TypeError:
        pass

    date = article_db["date"].strftime("%d %B %Y")

    return render_template("articles/article.html", article=article_db, content=content_md, edit=False, date=date)


@bp.route("/edit/<article_id>", methods=("POST", "GET"))
def edit(article_id):
    if not session.get("writer") or session.get("writer")["logged_in"] is False:
        return redirect(url_for("writers.login"))

    article_db = mongo.db.articles.find_one({"_id": ObjectId(article_id)})
    if not article_db:
        return render_template("404.html")
    if article_db["author"]["email"] != session["writer"]["email"]:
        return abort(403)

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        content = request.form["content"]

        mongo.db.articles.update_one(
            {"_id": ObjectId(article_id)},
            {
                "$set": {
                    "title": title,
                    "description": description,
                    "content": content,
                }
            },
        )
        return redirect(url_for("articles.article", article_id=article_id))

    return render_template("articles/edit.html", article=article_db)
