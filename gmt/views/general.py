import datetime
import random
import re

from flask import Blueprint, render_template, redirect, request, url_for, current_app
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
    if not posts:
        posts = get_news(choice="BBC")

    # Gets a random post and removes it from the list
    post1 = random.choice(posts)
    posts.remove(post1)
    # Gets a second random post
    post2 = random.choice(posts)

    # set limits for the description to 360 characters and add more length for each [link] tag
    limit1 = 360 + post1["description"][:360].count("[link]") * 30
    limit2 = 360 + post2["description"][:360].count("[link]") * 30

    # slice the description to the limit
    post1["description"] = post1["description"][:limit1]
    post2["description"] = post2["description"][:limit2]

    # remove unterminated [link] tags
    if re.search("\[link\]\([^\)]*[^\)]$", post1["description"]):
        post1["description"] = re.sub("\[link\]\(.*[^\)]$", "", post1["description"])
    if re.search("\[link\]\([^\)]*[^\)]$", post2["description"]):
        post2["description"] = re.sub("\[link\]\([^\)]*[^\)]$", "", post2["description"])

    # add ellipses and markdown it
    post1["description"] = markdown(post1["description"] + "...")
    post2["description"] = markdown(post2["description"] + "...")

    return render_template("general/index.html", news=[post1, post2])


@bp.route("/news")
def news():
    """Render the newspaper."""
    posts = mongo.db.articles.find(
        {"date": {"$gte": datetime.datetime.utcnow() - datetime.timedelta(days=1)}}
    )
    if not list(posts):
        posts = get_news(choice="BBC")

    return render_template("general/news.html", posts=posts, markdown=markdown, domain_name=current_app.config["DOMAIN_NAME"])


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
