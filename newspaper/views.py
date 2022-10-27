import datetime

from email_validator import EmailNotValidError, validate_email
from flask import redirect, render_template, request, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature, BadTimeSignature, SignatureExpired

from . import app
from .models import User, db
from .news import save_posts

mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=("GET", "POST"))
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
        if User.query.filter_by(email=email).first():
            error = "Email already used"

        # Get and validate the time
        time = request.form["timezone"]
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
            db.session.add(user)
            db.session.commit()

            # Create the token and the confirmation link
            token = serializer.dumps(email)
            confirmation_link = url_for("confirm_email", _external=True, token=token)

            # Create and send the confirmation message
            msg = Message(
                "Confirm Email",
                recipients=[email],
                body=f"Confirm your email by clicking this link: {confirmation_link}",
            )
            mail.send(msg)

            return "<h1>Registration completed successfully! Confirm your email to receive the news.</h1>"

    return render_template("signup.html", error=error)


@app.route("/leave", methods=("POST", "GET"))
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
            return "<h1>There is no user with this email.</h1>"

        # Create the token and the confirmation link
        token = serializer.dumps(email)

        # Create and send the confirmation message
        msg = Message(
            "Confirm Email",
            recipients=[email],
            body=f"Token: {token}",
        )
        mail.send(msg)

        return redirect(url_for("confirm"))

    return render_template("leave.html", error=error)


@app.route("/confirm", methods=("POST", "GET"))
def confirm():
    if request.method == "POST":
        token = request.form["token"]
        try:
            email = serializer.loads(token, max_age=3600)
        except SignatureExpired:
            return "<h1>The token is expired!</h1>"
        except BadSignature:
            return "<h1>The token is invalid!</h1>"

        # Get the user from the database
        user = User.query.filter_by(email=email).first()

        # Delete the user from the database
        db.session.delete(user)
        db.session.commit()

        return "<h1>Successfully unsubscribed!</h1>"
    return render_template("confirm.html")


@app.route("/confirm-email")
def confirm_email():
    token = request.args.get("token", None)

    if not token:
        return "<h1>Missing token...</h1>"

    try:
        email = serializer.loads(token, max_age=3600)
    except SignatureExpired:
        return "<h1>The token has expired...</h1>"
    except (BadSignature, BadTimeSignature):
        return "<h1>The token is invalid...</h1>"

    # Set the confirmation field as True
    user = User.query.filter_by(email=email).first()
    user.confirmed = True

    db.session.commit()

    return redirect(url_for("news"))


@app.route("/news")
def news():
    posts = save_posts()
    return render_template("news.html", posts=posts)
