"""Flask commands.

This file contains Flask commands that can be executed from the command line.
At the moment this only contains a command that can be run from a cron job that has been
set up with GitHub Actions.
"""

import datetime
import json
import os
import re

import requests
from flask import Blueprint, render_template, current_app
from flask_mail import Message
from markdown import markdown

from .. import mail, mongo
from ..news import get_news

bp = Blueprint("commands", __name__)


def get_current_time() -> str:
    """Return the current time.

    The function will round the time to 30 minutes. To ensure the email will be sent
    correctly.
    """
    current_time = datetime.datetime.utcnow()
    current_time = current_time.replace(minute=30 if current_time.minute >= 30 else 0)
    current_time = datetime.datetime.strftime(current_time, "%H:%M")
    return current_time


@bp.cli.command()
def send_emails() -> None:
    """Send the emails.

    The function will send the emails containing the rendered template of the daily news
    to every confirmed user in the database.
    """
    current_time = get_current_time()
    print(f"Sending email batch of {current_time} UTC")

    users = mongo.db.users.find({"time": current_time, "confirmed": True})

    configs = {}
    for user in users:
        # if the user has a frequency and the current day is not in the frequency skip the user
        if not datetime.datetime.utcnow().weekday() + 1 in user["frequency"]:
            continue
        # appends all the options into a string and separates news and extras with a '|'
        user_string = ""
        user_string += " ".join(user["news"])
        user_string += "|"
        user_string += " ".join(user["extras"])

        # if the unique config is not already stored add it to the dictionary
        if user_string not in configs:
            configs[user_string] = [user["email"]]
        else:
            configs[user_string].append(user["email"])

    for config, emails in configs.items():
        sources = config.split("|")[0].split(" ")
        extras = config.split("|")[1].split(" ")

        news = mongo.db.articles.find({"source": {"$in": sources}, "date": {"$gte": datetime.datetime.utcnow() - datetime.timedelta(days=1)}})

        html = render_template("general/news.html", posts=news, markdown=markdown, domain_name=current_app.config["DOMAIN_NAME"])
        msg = Message(
            subject=f"Tech News",
            sender=current_app.config["MAIL_USERNAME"],
            bcc=emails,
            html=html,
        )
        mail.send(msg)

    # print(configs)


@bp.cli.command()
def summarize_news():
    """Summarize the news."""
    summarized_news_collection = []
    api_key = current_app.config["SUMMARIZATION_API_KEY"]
    with open("rss.json") as f:
        rss = json.load(f)
        for key, value in rss.items():
            if key.startswith("_"):
                continue
            raw_news = get_news(key)
            url = "https://api.meaningcloud.com/summarization-1.0"

            for news in raw_news:
                payload = {"key": api_key, "url": news["url"], "sentences": 4}

                response = requests.post(url, data=payload)
                if response.status_code != 200:
                    print("error", response.status_code, response.json())
                    continue

                if response:
                    try:
                        if int(response.json()["status"]["remaining_credits"]) < 20:
                            api_key = current_app.config["SUMMARIZATION_API_KEY_2"]

                        description = response.json()["summary"]
                        description = description.replace("[...] ", "")
                    except KeyError:
                        description = None

                if description is None or description == "" or len(description) < 10:
                    description = news["description"]

                for link in re.findall(
                    pattern=r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))""",
                    string=description,
                ):

                    # Replace the link with a Markdown link
                    description = description.replace(link, f"[link]({link})")

                summarized_news = {
                    "title": news["title"],
                    "description": description,
                    "url": news["url"],
                    "author": None,
                    "thumbnail": news["thumbnail"],
                    "date": datetime.datetime.utcnow(),
                    "source": key.lower(),
                    "formatted_source": key,
                }
                summarized_news_collection.append(summarized_news)
                print("summarized")

    if summarized_news_collection:
        # delete all articles that are not from GMT
        mongo.db.articles.delete_many({"source": {"$ne": "GMT"}})

    mongo.db.articles.insert_many(summarized_news_collection)
