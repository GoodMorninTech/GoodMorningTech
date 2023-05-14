from bson import ObjectId
import markdown
from flask import (
    Blueprint,
    abort,
    redirect,
    render_template,
    request,
    session,
    url_for,
    current_app,
)
from datetime import datetime

from flask_login import login_required, current_user

from .. import mongo
from ..utils import clean_html, upload_file

bp = Blueprint("articles", __name__, url_prefix="/articles")


@bp.route("/<article_id>", methods=("POST", "GET"))
def article(article_id):
    if current_user.is_authenticated:
        current_user.writer = mongo.db.writers.find_one(
            {"_id": ObjectId(current_user.id)}
        )

    article_db = mongo.db.articles.find_one({"_id": ObjectId(article_id)})
    # if article doesnt exists 404
    if not article_db:
        return render_template("404.html")

    if request.method == "POST":
        # DELETES ARTICLE
        if current_user.is_authenticated:
            mongo.db.articles.delete_one({"_id": ObjectId(article_id)})
            return redirect(url_for("writers.portal"))

    content_md = markdown.markdown(article_db["content"])

    date = article_db["date"].strftime("%d %B %Y")

    article_db["views"] = int(article_db["views"]) + 1
    mongo.db.articles.update_one(
        {"_id": ObjectId(article_id)}, {"$set": {"views": article_db["views"]}}
    )

    return render_template(
        "articles/article.html",
        article=article_db,
        content=content_md,
        date=date,
        no_meta=True,
    )


@bp.route("/edit/<article_id>", methods=("POST", "GET"))
@login_required
def edit(article_id):
    current_user.writer = mongo.db.writers.find_one({"_id": ObjectId(current_user.id)})

    article_db = mongo.db.articles.find_one({"_id": ObjectId(article_id)})
    if not article_db:
        return render_template("404.html")
    if article_db["author"]["email"] != current_user.writer["email"]:
        return abort(403)

    if request.method == "POST":
        title = request.form.get("title")
        if not title:
            return render_template(
                "writers/create.html",
                status=f"Please enter a title!",
                article=article_db,
            )
        description = request.form.get("description")
        if not description:
            return render_template(
                "writers/create.html",
                status=f"Please enter a description!",
                article=article_db,
            )
        content = request.form.get("content")
        if not content:
            return render_template(
                "writers/create.html",
                status=f"Please enter some content!",
                article=article_db,
            )
        thumbnail = request.files.get("thumbnail", None)
        categories = request.form.getlist("category")

        if not categories:
            return render_template(
                "writers/create.html",
                status=f"Please select atleast one category!",
                article=article_db,
            )

        if thumbnail:
            if not upload_file(
                file=thumbnail, filename=article_db["_id"], current_app=current_app
            ):
                return render_template(
                    "writers/create.html",
                    status=f"Error uploading thumbnail! Uploaded without thumbnail,"
                    f" edit article to add one!",
                    article=article_db,
                )

        mongo.db.articles.update_one(
            {"_id": ObjectId(article_id)},
            {
                "$set": {
                    "title": title,
                    "description": description,
                    "content": clean_html(content),
                    "categories": categories,
                }
            },
        )
        return redirect(url_for("articles.article", article_id=article_id))

    return render_template("articles/edit.html", article=article_db)
