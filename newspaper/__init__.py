import os
import pymongo
from flask import Flask
from flask_mail import Mail

mail = Mail()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    # Get the config from the instance folder
    try:
        app.config.from_pyfile("config.py")
    except OSError:
        app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
        app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
        app.config["MONGO_DATABASE"] = os.environ.get("MONGO_DATABASE")
        app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
        app.config["MAIL_PORT"] = int(os.environ.get("MAIL_PORT"))
        app.config["MAIL_USE_TLS"] = False  # Changed for security reasons
        app.config["MAIL_USE_SSL"] = True  # Changed for security reasons
        app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
        app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
        app.config["MAIL_DEFAULT_SENDER"] = ("Good Morning Tech", os.environ.get("MAIL_USERNAME"))

    mail.init_app(app)

    # Connect to the database
    app.mongo = pymongo.MongoClient(app.config["MONGO_URI"])
    app.mongo.db = app.mongo.get_database(app.config["MONGO_DATABASE"])

    from . import views

    app.register_blueprint(views.bp)

    return app
