"""Flask commands.

This file contains Flask commands that can be executed from the command line.
At the moment this only contains a command that can be run from a cron job that has been
set up with GitHub Actions.
"""

import datetime
import json
import os

import requests
from flask import Blueprint, render_template, current_app
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
    html = render_template("general/news.html", posts=get_news(choice="BBC"))
    current_time = get_current_time()

    users = mongo.db.users.find({"confirmed": True, "time": current_time})
    for user in users:
        msg = Message("Daily News!", recipients=[user["email"]], html=html)
        mail.send(msg)


@bp.cli.command()
def summarize_news():
    """Summarize the news."""
    with open("rss.json") as f:
        rss = json.load(f)
        for key, value in rss.items():
            if key.startswith("_"):
                continue
            raw_news = get_news(key)
            url = "https://api.meaningcloud.com/summarization-1.0"

            for news in raw_news:
                payload = {
                    'key': current_app.config["SUMMARIZATION_API_KEY"],
                    'url': news["url"],
                    'sentences': 4
                }

                response = requests.post(url, data=payload)
                if response.status_code == 200:
                    summarized_news = {"title": news["title"], "description": response.json()["summary"],
                                       "url": news["url"], "author": None,
                                       "thumbnail": news["thumbnail"],
                                       "date": datetime.datetime.utcnow(), "source": key}

                    mongo.db.articles.insert_one(summarized_news)

                else:
                    print("Error: ", response.status_code, response.reason, response.json())

    # delete all articles that are not from GMT
    mongo.db.articles.delete_many({"source": {"$ne": "GMT"}})
