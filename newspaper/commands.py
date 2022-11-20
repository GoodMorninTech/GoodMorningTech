import datetime

from flask import Blueprint, current_app, render_template
from flask_mail import Message

from . import mail
from .news import save_posts

bp = Blueprint("commands", __name__)


@bp.cli.command()
def send_emails():
    html = render_template("news.html", posts=save_posts())
    current_time = datetime.datetime.utcnow()

    for user in current_app.mongo.db.users.find({"confirmed": True}):
        user_time = datetime.datetime.strptime(user["time"], "%H:%M:%S")
        if current_time.hour != user_time.hour:
            continue

        msg = Message("Daily News!", recipients=[user["email"]], html=html)
        mail.send(msg)
