import datetime
from urllib.parse import unquote_plus

from email_validator import validate_email, EmailNotValidError
from flask import Blueprint, abort, current_app, redirect, render_template, request, session, url_for
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature, SignatureExpired

from .. import mail, mongo

EMAIL_TEMPLATE = """<!doctype html>
<html lang='en'>
<body>
    <p>Hi there,</p>
    <p>Please confirm your email address by clicking the button below:</p>
    <a href="{}"
        style="text-decoration:none;color:#fff;background-color:#007bff;
            border-color:#007bff;padding:.4rem .75rem;border-radius:.50rem"
        target="_blank">Confirm Email</a>
        <p>You can safely ignore this email if you didn't request confirmation.
        Someone else might have typed your email address by mistake.</p>
        <p>Thank you,</p>
        <p>Good Morning Tech</p>
        <hr style="border:solid 1px lightgray">
        <small>Sent automatically. <a href="{}">In case the button doesnt works click me</small>
    </body>
</html>"""

bp = Blueprint("auth", __name__)


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
        if mongo.db.users.find_one({"email": email, "confirmed": True}):
            error = "Email already used"

        # Get and validate the time
        time = request.form["time-selection"]
        try:
            time = datetime.datetime.strptime(time, "%H")
        except ValueError:
            error = "Invalid time"

        if not error:
            # Get and apply the timezone to transform it to UTC
            timezone = request.form["timezone-selection"]
            # ^ its a string like +1, -9 or +5.30 meaning the offset from UTC
            if "." in timezone:
                # a . is in a timezone like india when its +5.30 (weird)
                hours, minutes = timezone.split(".")
                time = time + datetime.timedelta(hours=int(hours), minutes=int(minutes))
                # remember math 10 + (-2) = 8 so this is correct
            else:
                time = time + datetime.timedelta(hours=int(timezone))

            time = datetime.datetime.strftime(time, "%H:%M")
            # formats time to be like 12:30 or 01:00. Using the obviously superior 24 hour system

            # Create the user
            user = {
                "email": email,
                "time": time,  # time in UTC (like 12:30 or 01:00)
                "confirmed": False,
            }

            # Insert the user
            if not mongo.db.users.find_one({"email": email}):
                mongo.db.users.insert_one(user)
            else:
                mongo.db.users.update_one({"email": email}, {"$set": user})

            session["confirmed"] = {"email": email, "confirmed": False}

            return redirect(
                url_for("auth.confirm", email=email, next="auth.register")
            )

    try:
        # if the user is already confirmed, redirect to the news page
        if session.get("confirmed")["confirmed"]:
            # ^ if there is a confirmed key in the session, and its value is True
            email = session.get("confirmed")["email"]
            mongo.db.users.update_one({"email": email}, {"$set": {"confirmed": True}})
            session["confirmed"] = {
                "email": email,
                "confirmed": False,
            }  # set confirmed back to False
            return redirect(url_for("general.news"))
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
        if not mongo.db.users.find_one({"email": email}):
            error = "Email not found"
        if not error:
            return redirect(url_for("auth.confirm", email=email, next="auth.leave"))

    try:
        if session.get("confirmed")["confirmed"]:
            email = session.get("confirmed")["email"]

            # Get the user from the database
            user = mongo.db.users.find_one({"email": email})

            # Delete the user
            mongo.db.users.delete_one(user)

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
    next_page = request.args.get("next")
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
        "auth.confirm", _external=True, token=token, email=email, next=next_page
    )

    # If the email is not in the db error out
    if not mongo.db.users.find_one({"email": email}):
        return abort(404)

    # Create and send the confirmation message
    msg = Message(
        "Confirm your email",
        recipients=[email],
        html=EMAIL_TEMPLATE.format(confirmation_link, confirmation_link),
    )
    mail.send(msg)

    # this is when the user clicks the confirm Email button
    if request.method == "POST" and token:
        try:
            serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
            email = serializer.loads(token, max_age=300)
        except SignatureExpired:
            return render_template("confirm.html", error="Token expired.")
        except BadSignature:
            return render_template("confirm.html", error="The token is invalid.")

        session["confirmed"] = {"email": email, "confirmed": True}
        if not next_page:
            # if next is not defined he goes to the homepage
            return redirect(url_for("general.index"))
        # if next is defined he goes to the page he was on before and the session stuff above is to continue
        # from where he left off
        return redirect(url_for(next_page, email=email))
    return render_template("confirm.html", error=None, email=email, status="sent")
