import datetime
import random
import re

from bson import ObjectId
from email_validator import validate_email, EmailNotValidError
from flask import Blueprint, render_template, redirect, request, url_for, current_app
from flask_mail import Message
from werkzeug import Response
from markdown import markdown
from flask_login import login_required, current_user

from ..news import get_news
from .. import mongo, login_manager, User, mail
from ..utils import random_language_greeting

bp = Blueprint("general", __name__)


@bp.route("/", methods=["GET", "POST"])
def index():
    """Render the home page."""
    if request.method == "POST":
        email = request.form.get("email")
        if email:
            return redirect(url_for("auth.subscribe", email=email))

    if current_user.is_authenticated:
        current_user.writer = mongo.db.writers.find_one({"_id": ObjectId(current_user.id)})

    posts = mongo.db.articles.find(
        {"date": {"$gte": datetime.datetime.utcnow() - datetime.timedelta(hours=25)}}
    )

    # Mix the posts
    posts = list(posts)
    if not posts or len(posts) < 2:
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

    return render_template("general/index.html", news=[post1, post2], no_meta=True)


@bp.route("/news")
def news():
    """Render the newspaper."""
    posts = list(mongo.db.articles.find(
        {"date": {"$gte": datetime.datetime.utcnow() - datetime.timedelta(hours=25)}}
    ))

    if not posts:
        posts = get_news(choice="BBC")

    return render_template("general/news.html", posts=posts, markdown=markdown, domain_name=current_app.config["DOMAIN_NAME"], random_language_greeting=random_language_greeting())


@bp.route("/about")
def about():
    if current_user.is_authenticated:
        current_user.writer = mongo.db.writers.find_one({"_id": ObjectId(current_user.id)})
    return render_template("general/about.html", no_meta=True)


@bp.route("/contact", methods=["GET", "POST"])
def contact():
    if current_user.is_authenticated:
        current_user.writer = mongo.db.writers.find_one({"_id": ObjectId(current_user.id)})
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        subject = request.form.get("subject")
        message = request.form.get("message")
        try:
            validate_email(email)
        except EmailNotValidError as e:
            return render_template("general/contact.html", error="Invalid email address", success=False, no_meta=True)
        else:
            msg = Message(
                subject=f"Contact Form Submission from {name} - {subject}",
                sender=("Good Morning Tech", current_app.config["MAIL_USERNAME"]),
                recipients=["support@goodmorningtech.news"],
                body=f"From: {name} <{email}>,\n{message}"
            )
            mail.send(msg)
            return render_template("general/contact.html", success=True, error=None, no_meta=True)
    if current_user.is_authenticated:
        current_user.writer = mongo.db.writers.find_one({"_id": ObjectId(current_user.id)})
    return render_template("general/contact.html", success=False, error=None, no_meta=True)


@bp.route("/contribute")
def contribute():
    if current_user.is_authenticated:
        current_user.writer = mongo.db.writers.find_one({"_id": ObjectId(current_user.id)})
    return render_template("general/contribute.html")


@bp.route("/morning")
def morning():
    if current_user.is_authenticated:
        current_user.writer = mongo.db.writers.find_one({"_id": ObjectId(current_user.id)})
    return render_template("general/morning.html", no_meta=True)


@bp.route("/privacy")
def privacy():
    if current_user.is_authenticated:
        current_user.writer = mongo.db.writers.find_one({"_id": ObjectId(current_user.id)})
    return render_template("general/privacy_policy.html")


@bp.route("/tos")
def terms():
    if current_user.is_authenticated:
        current_user.writer = mongo.db.writers.find_one({"_id": ObjectId(current_user.id)})
    return render_template("general/tos.html")


@bp.route("/credits")
def credits():
    if current_user.is_authenticated:
        current_user.writer = mongo.db.writers.find_one({"_id": ObjectId(current_user.id)})
    return render_template("general/credits.html")


@bp.route("/sitemap.xml")
def sitemap():
    """Render the sitemap.xml."""

    sitemap_xml = render_template("general/sitemap.xml")
    response = Response(sitemap_xml, mimetype="text/xml")
    response.headers["Content-Type"] = "application/xml"

    return response

@login_manager.user_loader
def load_user(user_id):
    user_doc = mongo.db.writers.find_one({'_id': ObjectId(user_id)})
    if user_doc:
        user = User()
        user.id = str(user_doc['_id'])
        return user
    else:
        return None
