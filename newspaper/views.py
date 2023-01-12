import datetime

import markdown
from bson import ObjectId
from email_validator import EmailNotValidError, validate_email
from flask import (
    Blueprint,
    abort,
    current_app,
    redirect,
    render_template,
    request,
    session,
    url_for,
    jsonify,
)
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import SignatureExpired
from urllib.parse import unquote_plus

from werkzeug.security import check_password_hash, generate_password_hash

from . import mail, mongo
from .news import *

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
                url_for("views.confirm", email=email, next="views.register")
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
            return redirect(url_for("views.news"))
    except TypeError:
        pass

    return render_template(
        "signup.html", error=error, captcha_key=current_app.config["GOOGLE_CAPTCHA_KEY"]
    )


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
            return redirect(url_for("views.confirm", email=email, next="views.leave"))

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
    SUPPLY 'next' argument to redirect it there after the email got confirmed. example: next='views.register' """
    # next is where the user will be redirected after confirming
    next = request.args.get("next")
    email = unquote_plus(email)

    # the token
    token = request.args.get("token")

    # this is when the user clicks the link in the email and is presented with a confirm Email button
    if token and request.method == "GET":
        return render_template(
            "confirm.html", error=None, email=email, status="received"
        )

    # Generate the token and send the email
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    token = serializer.dumps(email)
    confirmation_link = url_for(
        "views.confirm", _external=True, token=token, email=email, next=next
    )

    # If the email is not in the db error out
    if not mongo.db.users.find_one({"email": email}):
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
        html=f"""
                <!doctype html>
                <html lang='en'>
                <body>
                  <p>Hi there,</p>
                  <p>Please confirm your email address by clicking the button below:</p>
                <a href="{confirmation_link}"
                   style="text-decoration:none;color:#fff;background-color:#007bff;border-color:#007bff;
                   padding:.4rem .75rem;border-radius:.50rem"
                   target="_blank">Confirm Email</a>
                <p>You can safely ignore this email if you didn't request confirmation.
                Someone else might have typed your email address by mistake.</p>
                <p>Thank you,</p>
                <p>Good Morning Tech</p>
                <hr style="border:solid 1px lightgray">
                <small>Sent automatically. <a href="{confirmation_link}">In case the button doesnt works click me</small>
                </body>
                </html>
    """,
    )
    mail.send(msg)

    # this is when the user clicks the confirm Email button
    if request.method == "POST" and token:
        try:
            serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
            email = serializer.loads(token, max_age=300)
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
    return render_template(
        "news.html", posts=get_news(choice="BBC")
    )  # TODO remove the hardcoded choice, make it a user preference


@bp.route("/api/news")
def api_news():
    return jsonify(get_news(choice="BBC"))


@bp.route("/writers/apply", methods=("POST", "GET"))
def writer_apply():
    if request.method == "POST":
        user_name = request.form["user_name"]
        email = request.form["email"]
        name = request.form["name"]
        reasoning = request.form["reasoning"]
        user = mongo.db.users.find_one({"email": email, "confirmed": True})
        if not user:
            return render_template(
                "apply.html",
                status=f"Please confirm your email first,"
                f" can be done by registering with this email again.",
            )
        elif mongo.db.writers.find_one({"email": email, "accepted": True}):
            return render_template("apply.html", status=f"You are already a writer!")
        elif mongo.db.writers.find_one({"email": email, "accepted": False}):
            return render_template("apply.html", status=f"You have already applied!")
        elif mongo.db.writers.find_one({"user_name": user_name}):
            return render_template(
                "apply.html", status=f"That user name is already taken!"
            )

        writer = {
            "email": email,
            "name": name,
            "reasoning": reasoning,
            "accepted": False,
            "password": None,
            "user_name": user_name, # NEEDS TO BE UNIQUE
            "confirmed": False # needs to confirm email when registering as writer
        }
        mongo.db.writers.insert_one(writer)

        if current_app.config["WRITER_WEBHOOK"] is None:
            print("No webhook set, please set WRITER_WEBHOOK")

        # POSTS the information to a discord channel using a webhook, so we can either accept it or not
        requests.post(
            current_app.config["WRITER_WEBHOOK"],
            json={
                "content": f"{name} with email {email} requested to join"
                f" the newsletter. Reasoning: {reasoning}"
            },
        )

    return render_template("apply.html", status=None)


@bp.route("/writers/login", methods=("POST", "GET"))
def writer_login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        writer_db = mongo.db.writers.find_one({"email": email, "accepted": True})

        if not writer_db:
            return render_template("writer_login.html", status=f"You are not a writer!")
        elif not check_password_hash(writer_db["password"], password):
            return render_template("writer_login.html", status=f"Wrong password!")
        elif writer_db["confirmed"] is False:
            return render_template("writer_login.html", status=f"Please confirm your email first!")

        session["writer"] = {"email": email, "logged_in": True}

        return redirect(url_for("views.writer_portal"))
    return render_template("writer_login.html", status=None)


@bp.route("/writers/logout", methods=("POST", "GET"))
def writer_logout():
    if not session.get("writer") or session.get("writer")["logged_in"] is False:
        return redirect(url_for("views.writer_login"))
    if request.method == "POST":
        session.pop("writer", None)
        return redirect(url_for("views.writer_login"))
    return render_template("writer_logout.html", status=None)

@bp.route("/writers/register", methods=("POST", "GET"))
def writer_register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        password_confirm = request.form["password_confirm"]

        if password != password_confirm:
            return render_template(
                "writer_register.html", status=f"Passwords dont match!"
            )

        writer = mongo.db.writers.find_one({"email": email, "accepted": True})
        if not writer:
            return render_template(
                "writer_register.html",
                status=f"You are not a writer! Please apply first",
            )
        elif writer["password"] and writer["confirmed"] is True: # if the writer isn't confirmed he can register again.
            return render_template(
                "writer_register.html",
                status=f"You are already registered! Please login",
            )

        mongo.db.writers.update_one(
            {"email": email, "accepted": True},
            {"$set": {"password": generate_password_hash(password)}},
        )

        return redirect(url_for("views.confirm", email=email, next="views.writer_register"))
    try:
        if session.get("confirmed")["confirmed"]:
            # ^ if there is a confirmed key in the session, and its value is True
            email = session.get("confirmed")["email"]
            mongo.db.writers.update_one({"email": email, "confirmed": False}, {"$set": {"confirmed": True}})
            session["confirmed"] = {
                "email": email,
                "confirmed": False,
            }  # set confirmed back to False
            return render_template("writer_register.html", status="You are now registered! You can login now")
    except TypeError:
        pass
    # If method is GET
    return render_template("writer_register.html", status=None)


# needs to be signed in to access
@bp.route("/writers/create", methods=("POST", "GET"))
def writer_create():
    if not session.get("writer") or session.get("writer")["logged_in"] is False:
        return redirect(url_for("views.writer_login"))

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        contnet = request.form["content"]
        email = session.get("writer")["email"]
        writer = mongo.db.writers.find_one({"email": email, "accepted": True})

        added_article = mongo.db.articles.insert_one(
            {
                "title": title,
                "description": description,
                "content": contnet,
                "author": writer["name"],
                "author_email": email,
                "author_user_name": writer["user_name"],
                "date": datetime.datetime.utcnow(),
            }
        )
        return redirect(url_for("views.article", article_id=added_article.inserted_id))
    return render_template("writer_create.html", status=None)


@bp.route("/writers/portal")
def writer_portal():
    if not session.get("writer") or session.get("writer")["logged_in"] is False:
        return redirect(url_for("views.writer_login"))
    articles = mongo.db.articles.find({"author_email": session["writer"]["email"]})
    writer_db = mongo.db.writers.find_one({"email": session["writer"]["email"]})
    return render_template("writer_portal.html", articles=articles, writer=writer_db)


@bp.route("/article/<article_id>", methods=("POST", "GET"))
def article(article_id):
    article_db = mongo.db.articles.find_one({"_id": ObjectId(article_id)})
    # if article doesnt exists 404
    if not article_db:
        return render_template("404.html")

    if request.method == "POST":
        # DELETES ARTICLE
        if session.get("writer")["logged_in"] and article_db["author_email"] == session["writer"]["email"]:
            mongo.db.articles.delete_one({"_id": ObjectId(article_id)})
            return redirect(url_for("views.writer_portal"))

    content_md = markdown.markdown(article_db["content"])
    try:
        if session.get("writer")["logged_in"] and article_db["author_email"] == session["writer"]["email"]:
            return render_template("article.html", article=article_db, content=content_md, edit=True)
    except TypeError:
        pass

    return render_template("article.html", article=article_db, content=content_md, edit=False)

@bp.route("/article/<article_id>/edit", methods=("POST", "GET"))
def article_edit(article_id):
    if not session.get("writer") or session.get("writer")["logged_in"] is False:
        return redirect(url_for("views.writer_login"))

    article_db = mongo.db.articles.find_one({"_id": ObjectId(article_id)})
    if not article_db:
        return render_template("404.html")
    if article_db["author_email"] != session["writer"]["email"]:
        return abort(403)

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        content = request.form["content"]

        mongo.db.articles.update_one(
            {"_id": ObjectId(article_id)},
            {
                "$set": {
                    "title": title,
                    "description": description,
                    "content": content,
                }
            },
        )
        return redirect(url_for("views.article", article_id=article_id))

    return render_template("article_edit.html", article=article_db)

@bp.route("/writer/<user_name>")
def writer(user_name):
    writer_db = mongo.db.writers.find_one({"user_name": user_name})
    if not writer_db:
        return render_template("404.html")
    articles = mongo.db.articles.find({"author_user_name": user_name})
    return render_template("writer.html", writer=writer_db, articles=articles)


@bp.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


@bp.route("/<path:path>")
def catch_all(path):
    return render_template("404.html")
