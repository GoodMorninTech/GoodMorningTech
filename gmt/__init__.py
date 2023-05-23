import os

from flask import Flask, render_template
from flask_mail import Mail
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from flask_mde import Mde
from flask_login import LoginManager, UserMixin
from flask_admin import Admin

mail = Mail()
mongo = PyMongo()
csrf = CSRFProtect()
sess = Session()
mde = Mde()
login_manager = LoginManager()
admin = Admin(name="Admin Page", template_mode="bootstrap4")


class User(UserMixin):
    pass


def create_app() -> Flask:
    """Create the Flask app.

    This function is responsible for creating the main Flask app, and it's the entry point for the factory pattern.
    """
    app = Flask(__name__, instance_relative_config=True)

    load_configuration(app)
    init_extensions(app)
    register_blueprints(app)

    return app


def load_configuration(app: Flask) -> None:
    """Load the configuration.

    The configuration will be loaded either from a configuration file or from environment variables.

    The following variables can be configured:
    - SECRET_KEY: A secret key used for any security related needs. It should be a long random string.
    - SERVER_NAME: Inform the application what host and port it is bound to.
    - MONGO_URI: The connection URI to the MongoDB database. It should specify the database name as well.
    - MAIL_SERVER: The SMTP server to connect to.
    - MAIL_PORT: The port of the SMTP server.
    - MAIL_USE_TLS: True if TLS is to be used.
    - MAIL_USE_SSL: True if SSL is to be used.
    - MAIL_USERNAME: The email address to send the mail from.
    - MAIL_PASSWORD: The password of the email address.
    - WRITER_WEBHOOK: The URL of the Discord webhook to send writer apply requests.
    - FORM_WEBHOOK: The URL of the Discord webhook to send form requests.
    """
    app.config["FLASK_ADMIN_SWATCH"] = "lux"
    app.config["SESSION_TYPE"] = "mongodb"
    app.config["SESSION_MONGODB_DB"] = "goodmorningtech"
    app.config["SESSION_MONGODB_COLLECT"] = "sessions"
    try:
        app.config.from_pyfile("config.py")
        app.config["SESSION_MONGODB"] = MongoClient(app.config["MONGO_URI"])
    except OSError:
        app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
        app.config["DOMAIN_NAME"] = os.environ.get("DOMAIN_NAME")
        app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
        app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
        app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
        app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
        app.config["MAIL_USE_SSL"] = os.environ.get("MAIL_USE_SSL")
        app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
        app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
        app.config["WRITER_WEBHOOK"] = os.environ.get("WRITER_WEBHOOK")
        app.config["FORM_WEBHOOK"] = os.environ.get("FORM_WEBHOOK")
        app.config["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")
        app.config["FTP_USER"] = os.environ.get("FTP_USER")
        app.config["FTP_PASSWORD"] = os.environ.get("FTP_PASSWORD")
        app.config["FTP_HOST"] = os.environ.get("FTP_HOST")
        app.config["API_NINJA_KEY"] = os.environ.get("API_NINJA_KEY")
        app.config["ADMIN_USER_EMAILS"] = (
            os.environ.get("ADMIN_USER_EMAILS").split(",")
            if os.environ.get("ADMIN_USER_EMAILS")
            else []
        )
        app.config["SESSION_MONGODB"] = MongoClient(app.config["MONGO_URI"])

        if app.config["MAIL_PORT"]:
            app.config["MAIL_PORT"] = int(app.config["MAIL_PORT"])
        if app.config["MAIL_USE_TLS"]:
            app.config["MAIL_USE_TLS"] = app.config["MAIL_USE_TLS"].casefold() == "true"
        if app.config["MAIL_USE_SSL"]:
            app.config["MAIL_USE_SSL"] = app.config["MAIL_USE_SSL"].casefold() == "true"


def init_extensions(app: Flask) -> None:
    """Initialize Flask extensions."""
    csrf.init_app(app)
    mail.init_app(app)
    mongo.init_app(app)
    sess.init_app(app)
    mde.init_app(app)
    login_manager.init_app(app)
    admin.init_app(app)


def register_blueprints(app: Flask) -> None:
    """Register Flask blueprints."""
    from .views import articles, auth, commands, general, writers, admin

    @app.errorhandler(404)
    def page_not_found(_):
        return render_template("404.html")

    app.register_blueprint(articles.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(commands.bp)
    app.register_blueprint(general.bp)
    app.register_blueprint(writers.bp)
    app.register_blueprint(admin.bp)
