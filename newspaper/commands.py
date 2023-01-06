import datetime

from flask import Blueprint, render_template
from flask_mail import Message

from . import mail, mongo
from .news import get_news

bp = Blueprint("commands", __name__)


@bp.cli.command()
def send_emails():
    html = render_template(
        "news.html", posts=get_news(choice="BBC")
    )  # TODO remove the hardcoded choice, make it a user preference

    current_date = datetime.datetime.utcnow()
    current_date = current_date.replace(minute=30 if current_date.minute > 30 else 0)
    current_time = datetime.datetime.strftime(current_date, "%H:%M")

    # Get confirmed users whose time is within an hour range
    users = mongo.db.users.find({"confirmed": True, "time": current_time})

    for user in users:
        msg = Message("Daily News!", recipients=[user["email"]], html=html)
        mail.send(msg)
