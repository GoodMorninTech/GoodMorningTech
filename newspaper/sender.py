import hashlib
import datetime

from flask import Blueprint, current_app, render_template, request
from flask_mail import Message

from . import mail
from newspaper.news import save_posts

bp = Blueprint("auth", __name__)


def hash_password(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode("UTF-8"), salt, 100000)


@bp.route("/send")
def send_emails():
    user_password = request.args.get("password")
    if not user_password:
        return {"message": "Password is missing!"}, 401

    user_password_hash = hash_password(user_password, current_app.config["PASSWORD_SALT"])
    if current_app.config["PASSWORD_HASH"] == user_password_hash:
        current_time = datetime.datetime.utcnow()
        html = render_template("news.html", posts=save_posts())

        users = current_app.mongo.db.users

        for user in users.find({"confirmed": True}):
            user_time = datetime.datetime.strptime(user["time"], "%H:%M:%S")
            if current_time.hour != user_time.hour:
                continue

            msg = Message("Daily News!", recipients=[user["email"]], html=html)
            mail.send(msg)

        return {"message": "Emails were sent correctly"}

    return {"message": "Password is incorrect!"}, 401
