import os

from flask import Flask
from flask_mail import Mail
from flask_pymongo import PyMongo

mail = Mail()
mongo = PyMongo()


def create_app() -> Flask:
    """Create the Flask app.

    This function is responsible for creating the main Flask app and it's the entry
    point for the factory pattern.
    """
    app = Flask(__name__, instance_relative_config=True)

    load_configuration(app)
    init_extensions(app)
    register_blueprints(app)

    return app


def load_configuration(app: Flask) -> None:
    """Load the configuration.

    The configuration will be loaded either from a configuration file or from
    environment variables.

    The following variables can be configured:
    - SECRET_KEY: A secret key that will be used for securely signing the session cookie
        and can be used for any other security related needs by extensions or your
        application. It should be a long random bytes or str.
    - SERVER_NAME: Inform the application what host and port it is bound to.
    - MONGO_URI: The connection URI to the MongoDB database. It should specify the
        database name as well.
    - MAIL_SERVER: The SMTP server to connect to.
    - MAIL_PORT: The port of the SMTP server.
    - MAIL_USE_TLS: True if TLS is to be used.
    - MAIL_USE_SSL: True if SSL is to be used.
    - MAIL_USERNAME: The email adress to send the mail from.
    - MAIL_PASSWORD: The password of the email adress.
    - MAIL_DEFAULT_SENDER: The name of the email sender.
    - WRITER_WEBHOOK: The URL of the Discord webhook to send writer apply requests.
    """
    try:
        app.config.from_pyfile("config.py")
    except OSError:
        app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
        app.config["SERVER_NAME"] = os.environ.get("SERVER_NAME")
        app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
        app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
        app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
        app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
        app.config["MAIL_USE_SSL"] = os.environ.get("MAIL_USE_SSL")
        app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
        app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
        app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")
        app.config["WRITER_WEBHOOK"] = os.environ.get("WRITER_WEBHOOK")

        if app.config["MAIL_DEFAULT_SENDER"]:
            app.config["MAIL_DEFAULT_SENDER"] = (
                app.config["MAIL_DEFAULT_SENDER"],
                app.config["MAIL_USERNAME"],
            )
        if app.config["MAIL_PORT"]:
            app.config["MAIL_PORT"] = int(app.config["MAIL_PORT"])


def init_extensions(app: Flask) -> None:
    """Initialize Flask extensions."""
    mail.init_app(app)
    mongo.init_app(app)


def register_blueprints(app: Flask) -> None:
    """Register Flask blueprints."""
    from . import commands, views

    app.register_blueprint(commands.bp)
    app.register_blueprint(views.bp)
