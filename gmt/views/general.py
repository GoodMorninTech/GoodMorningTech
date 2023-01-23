from flask import Blueprint, render_template, redirect, request, url_for
from werkzeug import Response

from ..news import get_news

bp = Blueprint("general", __name__)


@bp.route("/", methods=["GET", "POST"])
def index():
    """Render the home page."""
    if request.method == "POST":
        email = request.form.get("email")
        if email:
            return redirect(url_for("auth.subscribe", email=email))

    return render_template("general/index.html")


@bp.route("/news")
def news():
    """Render the newspaper."""
    return render_template("general/news.html", posts=get_news(choice="BBC"))

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