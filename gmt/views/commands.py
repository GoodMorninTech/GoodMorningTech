"""Flask commands.

This file contains Flask commands that can be executed from the command line.
At the moment this only contains a command that can be run from a cron job that has been
set up with GitHub Actions.
"""

import datetime

from flask import Blueprint, render_template
from flask_mail import Message

from .. import mail, mongo
from ..news import get_news

bp = Blueprint("commands", __name__)


def get_current_time() -> str:
    """Return the current time.

    The function will round the time to 30 minutes. To ensure the email will be sent
    correctly.
    """
    current_time = datetime.datetime.utcnow()
    current_time = current_time.replace(minute=30 if current_time.minute > 30 else 0)
    current_time = datetime.datetime.strftime(current_time, "%H:%M")
    return current_time


@bp.cli.command()
def send_emails() -> None:
    """Send the emails.

    The function will send the emails containing the rendered template of the daily news
    to every confirmed user in the database.
    """
    html = render_template("news.html", posts=get_news(choice="BBC"))
    current_time = get_current_time()

    users = mongo.db.users.find({"confirmed": True, "time": current_time})
    for user in users:
        msg = Message("Daily News!", recipients=[user["email"]], html=html)
        mail.send(msg)
