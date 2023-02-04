import datetime
import random

from flask import Blueprint, render_template, redirect, request, url_for
from werkzeug import Response
from markdown import markdown

from ..news import get_news
from .. import mongo

bp = Blueprint("general", __name__)


@bp.route("/", methods=["GET", "POST"])
def index():
    """Render the home page."""
    if request.method == "POST":
        email = request.form.get("email")
        if email:
            return redirect(url_for("auth.subscribe", email=email))

    posts = mongo.db.articles.find(
        {"date": {"$gte": datetime.datetime.utcnow() - datetime.timedelta(days=1)}}
    )

    # Mix the posts
    posts = list(posts)
    random.shuffle(posts)

    if not posts:
        posts = get_news(choice="BBC")

    return render_template("general/index.html", news=posts, markdown=markdown)


@bp.route("/news")
def news():
    """Render the newspaper."""
    posts = mongo.db.articles.find(
        {"date": {"$gte": datetime.datetime.utcnow() - datetime.timedelta(days=1)}}
    )
    if not posts:
        posts = get_news(choice="bbc")

    return render_template("general/news.html", posts=posts, markdown=markdown)


@bp.route("/about")
def about():
    return render_template("general/about.html")


@bp.route("/contact", methods=["GET", "POST"])
def contact():
    # if request.method == "POST":
    #     email = request.form.get("email")
    #     name = request.form.get("name")
    #     message = request.form.get("message")
    #     try:
    #         validate_email(email)
    #     except EmailNotValidError as e:
    #         return render_template("contact.html", error=e)
    #     else:
    #         msg = Message(
    #             subject=f"New message from {name}",
    #             sender=current_app.config["MAIL_USERNAME"],
    #             recipients=[current_app.config["MAIL_USERNAME"]],
    #             body=message,
    #         )
    #         mail.send(msg)
    #         return render_template("contact.html", success=True)
    return render_template("general/contact.html")


@bp.route("/contribute")
def contribute():
    return render_template("general/contribute.html")


@bp.route("/sitemap.xml")
def sitemap():
    """Render the sitemap.xml."""

    sitemap_xml = render_template("general/sitemap.xml")
    response = Response(sitemap_xml, mimetype="text/xml")
    response.headers["Content-Type"] = "application/xml"

    return response
