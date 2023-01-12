import requests
from flask import Blueprint, current_app, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from .. import mongo

bp = Blueprint("writers", __name__, url_prefix="/writers")


@bp.route("/apply", methods=("GET", "POST"))
def apply():
    if request.method == "POST":
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

        writer = {
            "email": email,
            "name": name,
            "reasoning": reasoning,
            "accepted": False,
            "password": None,
        }
        mongo.db.writers.insert_one(writer)

        # POSTS the information to a discord channel using a webhook, so we can either accept it or not
        requests.post(
            current_app.config["WRITER_WEBHOOK"],
            json={
                "content": f"{name} with email {email} requested to join"
                f" the newsletter. Reasoning: {reasoning}"
            },
        )

    return render_template("apply.html", status=None)


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        writer = mongo.db.writers.find_one({"email": email, "accepted": True})

        if not writer:
            return render_template("writer_login.html", status=f"You are not a writer!")
        elif not check_password_hash(writer["password"], password):
            return render_template("writer_login.html", status=f"Wrong password!")

        session["writer"] = {"email": email, "logged_in": True}

        return redirect(url_for("writers.portal"))
    return render_template("writer_login.html", status=None)


@bp.route("/register", methods=("GET", "POST"))
def register():
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
        elif writer["password"]:
            return render_template(
                "writer_register.html",
                status=f"You are already registered! Please login",
            )

        mongo.db.writers.update_one(
            {"email": email, "accepted": True},
            {"$set": {"password": generate_password_hash(password)}},
        )

        return render_template(
            "writer_register.html", status=f"You are now registered! You can now login."
        )
    # If method is GET
    return render_template("writer_register.html", status=None)


# needs to be signed in to access
@bp.route("/create")
def create():
    if not session.get("writer") or session.get("writer")["logged_in"] is False:
        return redirect(url_for("writers.login"))
    return render_template("writer_create.html", status=None)


@bp.route("/portal")
def portal():
    if not session.get("writer") or session.get("writer")["logged_in"] is False:
        return redirect(url_for("writers.login"))
    return render_template("writers_portal.html")
