import datetime
from urllib.parse import unquote_plus
import requests

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
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature, SignatureExpired

from .. import mail
from ..models import User

bp = Blueprint("auth", __name__)


@bp.route("/subscribe", methods=("GET", "POST"))
def subscribe():
    error = None
    if request.method == "POST":
        # Get and validate the email
        email = request.form["email"]
        try:
            validate_email(email)
        except EmailNotValidError:
            error = "Invalid email"

        # Check if the email is already used
        if User.objects(email=email, confirmed=True):
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

            user = User(email=email, time=time)
            if not User.objects(email=email):
                user.save()

            # Create the user
            # user = {
            #    "email": email,
            #   "time": time,  # time in UTC (like 12:30 or 01:00)
            #    "confirmed": False,
            #    "frequency": frequency,
            #    "news": news_,
            #    "extras": extras,
            #}
            # TODO update the User model since it got some updates (Levani from the merge conflict fix)

            else:
                User.objects(email=email).update(**user.to_mongo())

            session["confirmed"] = {"email": email, "confirmed": False}

            if current_app.config["FORM_WEBHOOK"]:
                requests.post(
                    current_app.config["FORM_WEBHOOK"],
                    json={
                        "content": f"New user registered: `{email[0]}****@{email.split('@')[1][0]}****.{email.split('@')[1].split('.')[1]}`"
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
            User.objects(email=email).update(confirmed=True)
            session["confirmed"] = {
                "email": email,
                "confirmed": False,
            }  # set confirmed back to False
            return redirect(url_for("general.news"))
    except TypeError:
        pass

    email = request.args.get("email")

    return render_template("auth/subscribe.html", error=error, email=email)
    # in case an email is passed along from views.index pass it into register to prefill the form


@bp.route("/unsubscribe", methods=("POST", "GET"))
def unsubscribe():
    error = None
    if request.method == "POST":
        # Get and validate the email
        email = request.form["email"]
        try:
            validate_email(email)
        except EmailNotValidError:
            error = "Invalid email"

        # Check if the email is already used
        if not User.objects(email=email):
            error = "Email not found"
        if not error:
            return redirect(
                url_for("auth.confirm", email=email, next="auth.unsubscribe")
            )

    try:
        if session.get("confirmed")["confirmed"]:
            email = session.get("confirmed")["email"]
            User.objects(email=email).delete()
            session["confirmed"] = {"email": email, "confirmed": False}

            return "<h1>Successfully unsubscribed!</h1>"
    except TypeError:
        pass

    return render_template("auth/unsubscribe.html", error=error)


@bp.route("/confirm/<email>", methods=("POST", "GET"))
def confirm(email: str):
    """Send a confirmation email to the user and confirms the email if the user clicks on the link
    SUPPLY 'next' argument to redirect it there after the email got confirmed. example: next='views.register'"""
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
            return render_template("auth/confirm.html", error="Token expired")
        except BadSignature:
            return render_template("auth/confirm.html", error="The token is invalid!")

        session["confirmed"] = {"email": email, "confirmed": True}
        if not next:
            # if next is not defined he goes to the homepage
            return redirect(url_for("general.index"))
        # if next is defined he goes to the page he was on before and the session stuff above is to continue
        # from where he left off
        return redirect(url_for(next, email=email))

    # this is when the user clicks the link in the email and is presented with a confirm Email button
    if token and request.method == "GET":
        return render_template("auth/confirm.html", error=None, email=email, status="received")

    # Generate the token and send the email
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    token = serializer.dumps(email)
    confirmation_link = url_for("auth.confirm", _external=True, token=token, email=email, next=next)

    # If the email is not in the db error out
    if not User.objects(email=email):
        return abort(404)

    # Create and send the confirmation message
    msg = Message(
        "Confirm your email",
        recipients=[email],
        body=f"""Hi there,
                Please confirm your email address by clicking the link below:
                {confirmation_link}
                You can safely ignore this email if you didn't request confirmation.
                Someone else might have typed your email address by mistake.
                Thank you,
                Good Morning Tech""",
        html=render_template("auth/email_confirm.html", confirmation_link=confirmation_link),
    )
    mail.send(msg)

    return render_template("auth/confirm.html", error=None, email=email, status="sent")
