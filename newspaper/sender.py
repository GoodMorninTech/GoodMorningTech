import atexit
import datetime

from apscheduler.schedulers.background import BackgroundScheduler


def send_email():
    print(datetime.datetime.now())

    # now = datetime.datetime.utcnow()
    # now = now.replace(second=0, microsecond=0, minute=30 if now.minute >= 30 else 0)
    # now = now.time()

    # test = True
    # if test == True:
    #    now = datetime.time(5, 0, 0)

    # with current_app.app_context():
    #    db = current_app.mongo.db
    # users = db.users

    # posts = save_posts()
    ## Send the emails
    # print(now)
    # confirmed_users = 0
    # for user in users.find({"confirmed": True}):
    #    # Add to a dictionary
    #    data = {
    #        "email": user["email"],
    #    }
    #    confirmed_users += 1

    #    msg = Message(
    #        "Daily News",
    #        recipients=[data["email"]],
    #        body=render_template("news.html", posts=posts),
    #    )
    #    print(msg.recipients)

    # print(confirmed_users)


def register_jobs():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=send_email, trigger="interval", seconds=5)
    scheduler.start()

    atexit.register(scheduler.shutdown)
