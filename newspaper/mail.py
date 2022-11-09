import datetime
import os
import pymongo
from flask import current_app, render_template, Flask
from flask_mail import Message

from news import save_posts


def send_mail():
    """This function sends the email at a specific time. It's run by GitHub Actions and can have a delay up to 5 minutes. """
    now = datetime.datetime.utcnow()
    now = now.replace(second=0, microsecond=0, minute=30 if now.minute >= 30 else 0)
    now = now.time()

    test = True
    if test == True:
        now = datetime.time(5, 0, 0)

    db = current_app.mongo.db
    users = db.users

    posts = save_posts()
    # Send the emails
    print(now)
    for user in users.find({"confirmed": True, "time": str(now)}):
        # Add to a dictionary
        data = {
            "email": user["email"],
        }
        print(data)
        # Send the email
    if data != None:
        msg = Message(
            subject="Good Morning Tech",
            bcc=[data["email"]],
            html=render_template("news.html"),
        )
        print(msg)
    else:
        print("No users found")
        return
        # current_app.mail.send(msg)


if __name__ == "__main__":
    app = Flask(__name__, instance_relative_config=True)
    try:
        app.config.from_pyfile("config.py")
    except OSError:
        app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

    app.app_context().push()
    app.mongo = pymongo.MongoClient(app.config["MONGO_URI"])
    app.mongo.get_database("goodmorningtech")
    send_mail()
