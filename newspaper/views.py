import datetime

from email_validator import EmailNotValidError, validate_email
from flask import (Blueprint, current_app, redirect, render_template, request, session, abort,
                   url_for)
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import SignatureExpired

from . import mail
from .models import User, db
from .news import save_posts

bp = Blueprint("views", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/register", methods=("GET", "POST"))
def register():
    error = None
    if request.method == "POST":
        # Get and validate the email
        email = request.form["email"]
        try:
            validate_email(email)
        except EmailNotValidError:
            error = "Invalid email"

        # Check if the email is already used
        db_user = User.query.filter_by(email=email).first()
        if db_user and db_user.confirmed:
            error = "Email already used"

        # Get and validate the time
        time = request.form[
            "time-preference"
        ]  # TODO transform to UTC time and get time zone selection
        try:
            time = datetime.datetime.strptime(time, "%H").time()
        except ValueError:
            error = "Invalid time"

        if not error:
            # Create the user
            user = User(
                email=email,
                time=time,
            )

            # Add the user to the database
            if not db_user:
                db.session.add(user)
                db.session.commit()

            session["confirmed"] = {"email": email, "confirmed": False}

            return redirect(url_for("views.confirm", email=email, next="views.register"))

    if session.get("confirmed")["confirmed"]:
        email = session.get("confirmed")["email"]
        user = User.query.filter_by(email=email).first()
        user.confirmed = True

        db.session.commit()
        session["confirmed"] = {"email": email, "confirmed": False}
        return redirect(url_for("views.news"))

    return render_template("signup.html", error=error)


@bp.route("/leave", methods=("POST", "GET"))
def leave():
    error = None
    if request.method == "POST":
        # Get and validate the email
        email = request.form["email"]
        try:
            validate_email(email)
        except EmailNotValidError:
            error = "Invalid email"

        # Check if the email is already used
        if not User.query.filter_by(email=email).first():
            error = "No user exists with this email"
        if not error:
            return redirect(url_for("views.confirm", email=email, next="views.leave"))

    if session.get("confirmed")["confirmed"]:
        email = session.get("confirmed")["email"]

        user = User.query.filter_by(email=email).first()

        # Delete the user from the database
        db.session.delete(user)
        db.session.commit()

        session["confirmed"] = {"email": email, "confirmed": False}

        return "<h1>Successfully unsubscribed!</h1>"

    return render_template("leave.html", error=error)


@bp.route("/confirm/<email>", methods=("POST", "GET"))
def confirm(email: str):
    next = request.args.get("next")
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    token = serializer.dumps(email)

    if not User.query.filter_by(email=email).first():
        return abort(404)

    # Create and send the confirmation message
    msg = Message(
        "Confirm Email",
        recipients=[email],
        body=f"Token: {token}",
    )
    mail.send(msg)
    if request.method == "POST":
        token = request.form["token"]
        try:
            serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
            email = serializer.loads(token, max_age=3600)
        except SignatureExpired:
            return render_template("confirm.html", error="Token expired")
        except:
            return render_template("confirm.html", error="The token is invalid!")

        session["confirmed"] = {"email": email, "confirmed": True}
        return redirect(url_for(next, email=email))

    return render_template("confirm.html")


@bp.route("/news")
def news():
    posts = save_posts()
    return render_template("news.html", posts=posts)


@bp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')
