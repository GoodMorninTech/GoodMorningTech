import datetime

from email_validator import EmailNotValidError, validate_email
from flask import (Blueprint, current_app, redirect, render_template, request, session, abort,
                   url_for)
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import SignatureExpired
from urllib.parse import unquote_plus

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

        db = current_app.mongo.db
        users = db.users
        # Check if the email is already used
        if users.find_one({"email": email, "confirmed": True}):
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
            user = {
                "email": email,
                "time": str(time),
                "confirmed": False,
            }

            # Insert the user
            if not users.find_one({"email": email}):
                users.insert_one(user)

            session["confirmed"] = {"email": email, "confirmed": False}

            return redirect(url_for("views.confirm", email=email, next="views.register"))

    try:
        if session.get("confirmed")["confirmed"]:
            email = session.get("confirmed")["email"]
            db = current_app.mongo.db
            users = db.users
            users.update_one({"email": email}, {"$set": {"confirmed": True}})
            session["confirmed"] = {"email": email, "confirmed": False}
            return redirect(url_for("views.news"))
    except TypeError:
        pass

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
        if not error:
            return redirect(url_for("views.confirm", email=email, next="views.leave"))

    try:
        if session.get("confirmed")["confirmed"]:
            email = session.get("confirmed")["email"]

            # Get the user from the database
            db = current_app.mongo.db
            users = db.users
            user = users.find_one({"email": email})
            # Delete the user
            users.delete_one(user)

            session["confirmed"] = {"email": email, "confirmed": False}

            return "<h1>Successfully unsubscribed!</h1>"
    except TypeError:
        pass

    return render_template("leave.html", error=error)


@bp.route("/confirm/<email>", methods=("POST", "GET"))
def confirm(email: str):
    """Send a confirmation email to the user and confirms the email if the user clicks on the link
    please supply next arg and set it to the function you want to redirect to after confirmation"""
    # next is where the user will be redirected after confirming
    next = request.args.get("next")
    email = unquote_plus(email)

    # the token
    token = request.args.get("token")

    # this is when the user clicks the link in the email and is presented with a confirm Email button
    if token and request.method == "GET":
        return render_template("confirm.html", error=None, email=email, status="received")

    # Generate the token and send the email
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    token = serializer.dumps(email)
    confirmation_link = url_for(
        "views.confirm", _external=True, token=token, email=email, next=next
    )

    db = current_app.mongo.db
    users = db.users

    # If the email is not in the db error out
    if not users.find_one({"email": email}):
        return abort(404)

    # Create and send the confirmation message
    msg = Message(
        "Confirm Email",
        recipients=[email],
        body=f"Click here to confirm your Email: {confirmation_link}",
    )
    mail.send(msg)

    # this is when the user clicks the confirm Email button
    if request.method == "POST" and token:
        try:
            serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
            email = serializer.loads(token, max_age=3600)
        except SignatureExpired:
            return render_template("confirm.html", error="Token expired")
        except:
            return render_template("confirm.html", error="The token is invalid!")

        session["confirmed"] = {"email": email, "confirmed": True}
        if not next:
            # if next is not defined he goes to the homepage
            return redirect(url_for("views.index"))
        # if next is defined he goes to the page he was on before and the session stuff above is to continue
        # from where he left off
        return redirect(url_for(next, email=email))

    return render_template("confirm.html", error=None, email=email, status="sent")


@bp.route("/news")
def news():
    posts = save_posts()
    return render_template("news.html", posts=posts)

@bp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@bp.route("/<path:path>")
def catch_all(path):
    return render_template("404.html")
