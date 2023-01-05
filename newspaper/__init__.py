import os
import pymongo
from flask import Flask
from flask_mail import Mail
from flask_pymongo import PyMongo

mail = Mail()
mongo = PyMongo()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    try:
        # Get the config from the instance folder
        app.config.from_pyfile("config.py")
    except OSError:
        # Get the config from environment variables
        app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
        app.config["SERVER_NAME"] = os.environ.get("SERVER_NAME")
        app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
        app.config["MONGO_DATABASE"] = os.environ.get("MONGO_DATABASE")
        app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
        app.config["MAIL_PORT"] = int(os.environ.get("MAIL_PORT"))
        app.config["MAIL_USE_TLS"] = False
        app.config["MAIL_USE_SSL"] = True
        app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
        app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
        app.config["MAIL_DEFAULT_SENDER"] = (
            "Good Morning Tech",
            app.config["MAIL_USERNAME"],
        )
        app.config["GOOGLE_CAPTCHA_KEY"] = os.environ.get("GOOGLE_CAPTCHA_KEY")

    mail.init_app(app)
    mongo.init_app(app)

    from . import views

    app.register_blueprint(views.bp)

    from . import commands

    app.register_blueprint(commands.bp)

    return app
