import datetime

from ftplib import FTP
import re


import requests
from flask import (
    Blueprint,
    current_app,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from .. import mongo

bp = Blueprint("writers", __name__, url_prefix="/writers")


@bp.route("/apply", methods=("POST", "GET"))
def apply():
    if request.method == "POST":
        user_name = request.form["user_name"]
        email = request.form["email"]
        name = request.form["name"]
        reasoning = request.form["reasoning"]
        user = mongo.db.users.find_one({"email": email, "confirmed": True})
        if not user:
            return render_template(
                "writers/apply.html",
                status=f"Please confirm your email first,"
                f" can be done by registering with this email again.",
            )
        elif mongo.db.writers.find_one({"email": email, "accepted": True}):
            return render_template(
                "writers/apply.html", status=f"You are already a writer!"
            )
        elif mongo.db.writers.find_one({"email": email, "accepted": False}):
            return render_template(
                "writers/apply.html", status=f"You have already applied!"
            )
        elif mongo.db.writers.find_one({"user_name": user_name}):
            return render_template(
                "writers/apply.html", status=f"That user name is already taken!"
            )
        elif len(user_name) < 3 or re.fullmatch("^[\w.-]+$", user_name) is None:
            return render_template(
                "writers/apply.html",
                status=f"User name must be at least 3 characters long and only contain"
                f" alphanumeric characters, underscores, dashes and dots.",
            )

        writer = {
            "email": email,
            "name": name,
            "reasoning": reasoning,
            "accepted": False,
            "password": None,
            "user_name": user_name,  # NEEDS TO BE UNIQUE
            "confirmed": False,  # needs to confirm email when registering as writer
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

    return render_template("writers/apply.html", status=None)


@bp.route("/login", methods=("POST", "GET"))
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        writer_db = mongo.db.writers.find_one({"email": email, "accepted": True})

        if not writer_db:
            return render_template(
                "writers/login.html", status=f"You are not a writer!"
            )
        elif not check_password_hash(writer_db["password"], password):
            return render_template("writers/login.html", status=f"Wrong password!")
        elif writer_db["confirmed"] is False:
            return render_template(
                "writers/login.html", status=f"Please confirm your email first!"
            )

        session["writer"] = {"email": email, "logged_in": True}

        return redirect(url_for("writers.portal"))
    return render_template("writers/login.html", status=None)


@bp.route("/logout", methods=("POST", "GET"))
def logout():
    if not session.get("writer") or session.get("writer")["logged_in"] is False:
        return redirect(url_for("writers.login"))
    if request.method == "POST":
        session.pop("writer", None)
        return redirect(url_for("writers.login"))
    return render_template("writers/logout.html", status=None)


@bp.route("/register", methods=("POST", "GET"))
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        password_confirm = request.form["password_confirm"]

        if password != password_confirm:
            return render_template(
                "writers/register.html", status=f"Passwords dont match!"
            )

        writer = mongo.db.writers.find_one({"email": email, "accepted": True})
        if not writer:
            return render_template(
                "writers/register.html",
                status=f"You are not a writer! Please apply first",
            )
        elif (
            writer["password"] and writer["confirmed"] is True
        ):  # if the writer isn't confirmed he can register again.
            return render_template(
                "writers/register.html",
                status=f"You are already registered! Please login",
            )

        mongo.db.writers.update_one(
            {"email": email, "accepted": True},
            {"$set": {"password": generate_password_hash(password)}},
        )

        return redirect(url_for("auth.confirm", email=email, next="writers.register"))
    try:
        if session.get("confirmed")["confirmed"]:
            # ^ if there is a confirmed key in the session, and its value is True
            email = session.get("confirmed")["email"]
            mongo.db.writers.update_one(
                {"email": email, "confirmed": False}, {"$set": {"confirmed": True}}
            )
            session["confirmed"] = {
                "email": email,
                "confirmed": False,
            }  # set confirmed back to False
            return render_template(
                "writers/register.html",
                status="You are now registered! You can login now",
            )
    except TypeError:
        pass
    # If method is GET
    return render_template("writers/register.html", status=None)


@bp.route("/create", methods=("POST", "GET"))
def create():
    if not session.get("writer") or session.get("writer")["logged_in"] is False:
        return redirect(url_for("writers.login"))

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        content = request.form["content"]
        email = session.get("writer")["email"]
        writer = mongo.db.writers.find_one({"email": email, "accepted": True})

        article = {
            "title": title,
            "description": description,
            "content": content,
            "author": {
                "name": writer["name"],
                "email": email,
                "user_name": writer["user_name"],
            },
            "date": datetime.datetime.utcnow(),
            "source": "gmt",
            "thumbnail": None,
        }

        added_article = mongo.db.articles.insert_one(article)
        # add url to article
        mongo.db.writers.update_one(
            article,
            {
                "$set": {
                    "url": url_for(
                        "articles.article", article_id=added_article.inserted_id
                    )
                }
            },
        )
        return redirect(
            url_for("articles.article", article_id=added_article.inserted_id)
        )
    return render_template("writers/create.html", status=None)


@bp.route("/portal")
def portal():
    if not session.get("writer") or session.get("writer")["logged_in"] is False:
        return redirect(url_for("writers.login"))
    articles = mongo.db.articles.find({"author.email": session["writer"]["email"]})
    writer_db = mongo.db.writers.find_one({"email": session["writer"]["email"]})
    profile_picture = f"https://profile.goodmorningtech.news/{writer_db['user_name']}.jpg" #TODO Change extension
    req = requests.get(profile_picture)
    response_code = req.status_code
    if response_code != 200:
        profile_picture = None

    return render_template("writers/portal.html", articles=articles, writer=writer_db, profile_picture=profile_picture)


@bp.route("/<user_name>")
def writer(user_name):
    writer_db = mongo.db.writers.find_one({"user_name": user_name})
    if not writer_db:
        return render_template("404.html")
    articles = mongo.db.articles.find({"author.user_name": user_name})
    return render_template("writers/writer.html", writer=writer_db, articles=articles)


@bp.route("/settings", methods=("POST", "GET"))
def settings():
    if not session.get("writer") or session.get("writer")["logged_in"] is False:
        return redirect(url_for("writers.login"))
    writer_db = mongo.db.writers.find_one({"email": session["writer"]["email"]})
    if request.method == "POST":

        name = request.form.get("name", writer_db["name"])
        user_name = request.form.get("user_name", writer_db["user_name"])

        # Update the name and user_name if they are different
        if name != writer_db["name"]:
            mongo.db.writers.update_one(
                {"email": session["writer"]["email"]},
                {
                    "$set": {
                        "name": name,
                    }
                },
            )

        file = request.files.get("file", None)
        allowed_file_types = lambda filename: "." in filename and filename.rsplit(".", 1)[1].lower() in ["png", "jpg",
                                                                                                      "jpeg"]
        # TODO Convert the images to one format, so we can use the same extension in /portal

        if file.filename and allowed_file_types(file.filename):
            # Rename the file to the user_name
            file.filename = f"{user_name}.jpg"
            # Connect to FTP server
            ftp = FTP(current_app.config["FTP_HOST"])
            ftp.login(user=current_app.config["FTP_USER"], passwd=current_app.config["FTP_PASSWORD"])
            # Upload file to the directory htdocs/images
            ftp.delete(f"htdocs/{file.filename}")
            ftp.storbinary(f"STOR /htdocs/{file.filename}", file)
            # Close FTP connection
            ftp.quit()
        elif file.filename and not allowed_file_types(file.filename):
            return render_template("writers/settings.html", status="File type not allowed", writer=writer_db)

        return render_template("writers/settings.html", status="Settings updated successfully", writer=writer_db)
    return render_template("writers/settings.html", writer=writer_db, status=None)


@bp.route("/<user_name>/upload", methods=("POST", "GET"))
def upload(user_name):
    allowed_file_types = lambda filename: "." in filename and filename.rsplit(".", 1)[1].lower() in ["png", "jpg", "jpeg"]
    # TODO Convert the images to one format, so we can use the same extension in /portal
    if not session.get("writer") or session.get("writer")["logged_in"] is False:
        return redirect(url_for("writers.login"))
    writer_db = mongo.db.writers.find_one({"user_name": user_name})
    if writer_db["email"] != session["writer"]["email"]:
        return redirect(url_for("writers.portal"))
    if request.method == "POST":
        file = request.files["file"]
        if file.filename == "":
            return render_template("writers/upload.html", status="No file selected")
        if file and allowed_file_types(file.filename):
            # Rename the file to the user_name
            file.filename = f"{user_name}.jpg"
            # Connect to FTP server
            ftp = FTP(current_app.config["FTP_HOST"])
            ftp.login(user=current_app.config["FTP_USER"], passwd=current_app.config["FTP_PASSWORD"])
            # Upload file to the direcoty htdocs/images
            ftp.storbinary(f"STOR /htdocs/{file.filename}", file)
            # Close FTP connection
            ftp.quit()
            return render_template("writers/upload.html", status="File uploaded successfully")
        return render_template("writers/upload.html", status="File type not allowed")
    return render_template("writers/upload.html", status=None)
