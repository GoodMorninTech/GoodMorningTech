import datetime

from email_validator import EmailNotValidError, validate_email
from flask import (Blueprint, current_app, redirect, render_template, request,
                   url_for)
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import SignatureExpired

from . import mail
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
        if current_app.mongo.db.users.find_one({"email": email}):
            error = "Email already used"
        else:
            print("Email is valid")

        # Get and validate the time
        time = request.form[
            "time-preference"
        ]  # TODO transform to UTC time and get time zone selection
        try:
            time = datetime.datetime.strptime(time, "%H").time()
        except ValueError:
            error = "Invalid time"

        if not error:
            # Create the token and the confirmation link
            serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
            token = serializer.dumps(email)
            confirmation_link = url_for(
                "views.confirm_email", _external=True, token=token
            )
            # Create the user
            user = {
                "email": email,
                "time": str(time),
                "confirmation_link": confirmation_link,
                "confirmed": False,
            }

            db = current_app.mongo.db
            users = db.users
            # Insert the user
            users.insert_one(user)

            # Create and send the confirmation message
            msg = Message(
                "Confirm Email",
                recipients=[email],
                body=f"Confirm your email by clicking this link: {confirmation_link}",
            )
            mail.send(msg)
            if not users.find_one({"email": email}):
                status = "Registration completed successfully! Confirm your email to receive the news."
            else:
                status = (
                    "Confirmation email resent! Confirm your email to receive the news."
                )

            return f"<h1>{status}</h1>"

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
        if not current_app.mongo.db.users.find_one({"email": email}):
            error = "Email not found"
        else:
            print("Email is valid")

        # Create the token and the confirmation link
        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        token = serializer.dumps(email)

        # Create and send the confirmation message
        msg = Message(
            "Confirm Email",
            recipients=[email],
            body=f"Token: {token}",
        )
        mail.send(msg)

        return redirect(url_for("views.confirm"))

    return render_template("leave.html", error=error)


@bp.route("/confirm", methods=("POST", "GET"))
def confirm():
    if request.method == "POST":
        token = request.form["token"]
        try:
            serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
            email = serializer.loads(token, max_age=3600)
        except SignatureExpired:
            return "<h1>The token is expired!</h1>"
        except:
            return "<h1>The token is invalid!</h1>"

        # Get the user from the database
        db = current_app.mongo.db
        users = db.users
        user = users.find_one({"email": email})
        # Delete the user
        users.delete_one(user)

        return "<h1>Successfully unsubscribed!</h1>"
    return render_template("confirm.html")


@bp.route("/confirm-email")
def confirm_email():
    token = request.args.get("token", None)

    if not token:
        return "<h1>Missing token...</h1>"

    try:
        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        email = serializer.loads(token, max_age=3600)
    except SignatureExpired:
        return "<h1>The token has expired...</h1>"
    except:
        return "<h1>The token is invalid...</h1>"

    # Set the confirmation field as True
    db = current_app.mongo.db
    users = db.users
    users.update_one({"email": email}, {"$set": {"confirmed": True}})

    return redirect(url_for("views.news"))



@bp.route("/news")
def news():
    posts = save_posts()
    return render_template("news.html", posts=posts)


@bp.route("/<path:path>")
def catch_all(path):
    return render_template("404.html")
