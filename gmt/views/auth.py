import datetime
from urllib.parse import unquote_plus

import pytz
import requests
from bson import ObjectId

from email_validator import validate_email, EmailNotValidError
from flask import (
    Blueprint,
    abort,
    current_app,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import current_user
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature, SignatureExpired

from .. import mail, mongo, turnstile

bp = Blueprint("auth", __name__)


@bp.route("/subscribe", methods=("GET", "POST"))
def subscribe():
    if current_user.is_authenticated:
        current_user.writer = mongo.db.writers.find_one(
            {"_id": ObjectId(current_user.id)}
        )
    error = None
    timezones = pytz.all_timezones
    if request.method == "POST":
        if not turnstile.verify():
            return abort(400)

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
            time = request.form.get("time-selection", None)
            if time is None:
                raise ValueError
            time = int(time)
        except ValueError:
            error = "Invalid time"

        # Get and validate the timezone, example: America/New_York
        timezone = request.form.get("timezone-selection", None)
        if timezone not in timezones:
            error = "Invalid timezone"

        news_ = []
        bbc = request.form.get("bbc", False)
        techcrunch = request.form.get("techcrunch", False)
        verge = request.form.get("verge", False)
        cnn = request.form.get("cnn", False)
        gmt = request.form.get("gmt", False)
        guardian = request.form.get("guardian", False)
        for a in [bbc, techcrunch, verge, cnn, gmt, guardian]:
            if a:
                news_.append(a)

        # Check if the user has selected at least one news source
        if not news_:
            error = "Please select at least one news source"

        extras = []

        for key in ["codingchallenge", "repositories", "surprise"]:
            try:
                if request.form[key]:
                    extras.append(key)
            except KeyError:
                pass

        theme = request.form.get("theme", None)
        if theme == "very_real_option":
            # The registrar is a bot
            requests.post(
                current_app.config["FORM_WEBHOOK"],
                json={"content": f"A bot has been prevented from signing up."},
            )
            error = "Something went wrong!"
        if theme not in ["light", "dark"]:
            error = "Invalid theme"

        if not error:
            frequency = request.form["frequency"]
            if frequency == "everyday":
                frequency = [1, 2, 3, 4, 5, 6, 7]
            elif frequency == "weekdays":
                frequency = [1, 2, 3, 4, 5]
            elif frequency == "weekends":
                frequency = [6, 7]
            else:
                return abort(400)

            # Create the user
            user = {
                "email": email,
                "time": time,  # time in Local Time like 12:00
                "confirmed": False,
                "frequency": frequency,
                "news": news_,
                "extras": extras,
                "timezone": timezone,
                "theme": theme,
            }

            # Insert the user
            if not mongo.db.users.find_one({"email": email}):
                mongo.db.users.insert_one(user)
            else:
                mongo.db.users.update_one({"email": email}, {"$set": user})

            session["confirmed"] = {"email": email, "confirmed": False}

            if current_app.config["FORM_WEBHOOK"]:
                total_users = mongo.db.users.count_documents({})
                requests.post(
                    current_app.config["FORM_WEBHOOK"],
                    json={
                        "content": f"New user registered: `{email[0]}****@{email.split('@')[1][0]}****.{email.split('@')[1].split('.')[1]}`. Total users: `{total_users}`"
                    },
                )
            else:
                print("Form Webhook not set")

            return redirect(url_for("auth.confirm", email=email, next="auth.subscribe"))

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
            return render_template("auth/success.html", status="subscribed")
    except TypeError:
        pass

    email = request.args.get("email")

    return render_template(
        "auth/subscribe.html",
        error=error,
        email=email,
        timezones=timezones,
        no_meta=True,
    )
    # in case an email is passed along from views.index pass it into register to prefill the form


@bp.route("/settings", methods=("GET", "POST"))
def settings():
    if current_user.is_authenticated:
        current_user.writer = mongo.db.writers.find_one(
            {"_id": ObjectId(current_user.id)}
        )
    error = None
    timezones = pytz.all_timezones

    if request.method == "POST":
        try:
            # if the user is confirmed AND the email they confirmed matches the settings they updated
            if session.get("confirmed")["confirmed"] and session.get("confirmed")[
                "email"
            ] == request.form.get("email"):
                email = session.get("confirmed")["email"]

                # Get and validate the time
                time = request.form["time-selection"]
                try:
                    time = datetime.datetime.strptime(time, "%H")
                    time = request.form.get("time-selection", None)
                    if time is None:
                        raise ValueError
                    time = int(time)
                except ValueError:
                    error = "Invalid time"

                # Get and validate the timezone, example: America/New_York
                timezone = request.form.get("timezone-selection", None)
                if timezone not in timezones:
                    error = "Invalid timezone"

                news_ = []
                bbc = request.form.get("bbc", False)
                techcrunch = request.form.get("techcrunch", False)
                verge = request.form.get("verge", False)
                cnn = request.form.get("cnn", False)
                gmt = request.form.get("gmt", False)
                guardian = request.form.get("guardian", False)
                for a in [bbc, techcrunch, verge, cnn, gmt, guardian]:
                    if a:
                        news_.append(a)

                # Check if the user has selected at least one news source
                if not news_:
                    error = "Please select at least one news source"

                extras = []

                try:
                    if request.form["codingchallenge"]:
                        extras.append("codingchallenge")
                except KeyError:
                    pass
                try:
                    if request.form["repositories"]:
                        extras.append("repositories")
                except KeyError:
                    pass
                try:
                    if request.form["surprise"]:
                        extras.append("surprise")
                except KeyError:
                    pass

                theme = request.form.get("theme", None)
                if theme not in ["light", "dark"]:
                    error = "Invalid theme"

                if not error:
                    frequency = request.form["frequency"]
                    if frequency == "everyday":
                        frequency = [1, 2, 3, 4, 5, 6, 7]
                    elif frequency == "weekdays":
                        frequency = [1, 2, 3, 4, 5]
                    elif frequency == "weekends":
                        frequency = [6, 7]
                    else:
                        return abort(400)

                    # Create the user
                    user = {
                        "time": time,  # time in Local Time like 12:00
                        "frequency": frequency,
                        "news": news_,
                        "extras": extras,
                        "timezone": timezone,
                        "theme": theme,
                    }

                    mongo.db.users.update_one({"email": email}, {"$set": user})

                    session["confirmed"] = {"email": email, "confirmed": False}
                    return render_template("auth/success.html", status="settings")

        except TypeError as e:
            pass
        # Get and validate the email
        email = request.form.get("email")
        try:
            validate_email(email)
        except EmailNotValidError:
            error = "Invalid email"

        # Check if the email is already used
        if not mongo.db.users.find_one({"email": email}):
            error = "Email not found"
        if not error:
            return redirect(url_for("auth.confirm", email=email, next="auth.settings"))

    try:
        # if the user is confirmed show them the settings page prefilled with their settings
        if session.get("confirmed")["confirmed"]:
            email = session.get("confirmed")["email"]
            # pass along the confirmed email
            if not mongo.db.users.find_one({"email": email}):
                error = "Email not found"
            else:
                user = mongo.db.users.find_one({"email": email})
                time = int(user["time"])
                timezone = user["timezone"]
                news = user["news"]

                codingchallenge = "codingchallenge" in user["extras"]
                repositories = "repositories" in user["extras"]
                surprise = "surprise" in user["extras"]

                if user["theme"] == "dark":
                    dark = True
                    light = False
                else:
                    light = True
                    dark = False

                bbc = "bbc" in news
                techcrunch = "techcrunch" in news
                verge = "verge" in news
                cnn = "cnn" in news
                gmt = "gmt" in news
                guardian = "guardian" in news

                everyday = [1, 2, 3, 4, 5, 6, 7] == user["frequency"]
                weekdays = [1, 2, 3, 4, 5] == user["frequency"]
                weekends = [6, 7] == user["frequency"]

                return render_template(
                    "auth/settings.html",
                    error=error,
                    timezones=timezones,
                    email_confirmed=True,
                    email=email,
                    no_meta=True,
                    time=time,
                    timezone=timezone,
                    codingchallenge=codingchallenge,
                    repositories=repositories,
                    surprise=surprise,
                    light=light,
                    dark=dark,
                    bbc=bbc,
                    techcrunch=techcrunch,
                    verge=verge,
                    cnn=cnn,
                    gmt=gmt,
                    guardian=guardian,
                    everyday=everyday,
                    weekdays=weekdays,
                    weekends=weekends,
                )

            return render_template(
                "auth/settings.html",
                error=error,
                timezones=timezones,
                email_confirmed=True,
                email=email,
                no_meta=True,
            )

    except TypeError:
        pass

    return render_template(
        "auth/settings.html",
        error=error,
        no_meta=True,
    )


@bp.route("/unsubscribe", methods=("POST", "GET"))
def unsubscribe():
    if current_user.is_authenticated:
        current_user.writer = mongo.db.writers.find_one(
            {"_id": ObjectId(current_user.id)}
        )
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
            return redirect(
                url_for("auth.confirm", email=email, next="auth.unsubscribe")
            )

    try:
        if session.get("confirmed")["confirmed"]:
            email = session.get("confirmed")["email"]

            # Get the user from the database
            user = mongo.db.users.find_one({"email": email})

            # Delete the user
            mongo.db.users.delete_one(user)

            session["confirmed"] = {"email": email, "confirmed": False}

            return render_template("auth/success.html", status="unsubscribed")
    except TypeError:
        pass

    return render_template("auth/unsubscribe.html", error=error)


@bp.route("/confirm/<email>", methods=("POST", "GET"))
def confirm(email: str):
    """Send a confirmation email to the user and confirms the email if the user clicks on the link
    SUPPLY 'next' argument to redirect it there after the email got confirmed. example: next='views.register'
    """
    if current_user.is_authenticated:
        current_user.writer = mongo.db.writers.find_one(
            {"_id": ObjectId(current_user.id)}
        )
    # next is where the user will be redirected after confirming
    next = request.args.get("next")
    email = unquote_plus(email)

    # the token
    token = request.args.get("token")

    # this is when the user clicks the confirm Email button
    if request.method == "POST" and token:
        try:
            serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
            email = serializer.loads(token, max_age=300)
        except SignatureExpired:
            return render_template(
                "auth/confirm.html",
                status="received",
                error="Token expired. Try again to get a new email with an up to date confirmation link.",
            )
        except BadSignature:
            return render_template(
                "auth/confirm.html",
                status="received",
                error="The token is invalid! Try again for a new confirmation email.",
            )

        session["confirmed"] = {"email": email, "confirmed": True}
        if not next:
            # if next is not defined he goes to the homepage
            return redirect(url_for("general.index"))
        # if next is defined he goes to the page he was on before and the session stuff above is to continue
        # from where he left off
        return redirect(url_for(next, email=email))

    # this is when the user clicks the link in the email and is presented with a confirm Email button
    if token and request.method == "GET":
        return render_template(
            "auth/confirm.html", error=None, email=email, status="received"
        )

    # Generate the token and send the email
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    token = serializer.dumps(email)
    confirmation_link = url_for(
        "auth.confirm", _external=True, token=token, email=email, next=next
    )

    # If the email is not in the db error out
    if not mongo.db.users.find_one({"email": email}):
        return abort(404)

    # Create and send the confirmation message
    msg = Message(
        "Confirm your email",
        recipients=[email],
        sender=("Good Morning Tech", current_app.config["MAIL_USERNAME"]),
        body=f"""Hi there,
                Please confirm your email address by clicking the link below:
                {confirmation_link}
                You can safely ignore this email if you didn't request confirmation.
                Someone else might have typed your email address by mistake.
                Thank you,
                Good Morning Tech""",
        html=render_template(
            "auth/email_confirm.html", confirmation_link=confirmation_link
        ),
    )
    mail.send(msg)

    return render_template("auth/confirm.html", error=None, email=email, status="sent")
