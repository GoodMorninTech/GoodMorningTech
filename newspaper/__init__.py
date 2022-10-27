from flask import Flask
from flask_mail import Mail
import os
mail = Mail()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    try:
        app.config.from_pyfile("config.py")
    except OSError:
        app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('SQLALCHEMY_DATABASE_URI')
        app.config["MAIL_SERVER"] = os.environ.get('MAIL_SERVER')
        app.config["MAIL_PORT"]: int = os.environ.get('MAIL_PORT')
        app.config["MAIL_USE_TLS"]: bool = os.environ.get('MAIL_USE_TLS')
        app.config["MAIL_USE_SSL"]: bool = os.environ.get('MAIL_USE_SSL')
        app.config["MAIL_USERNAME"] = os.environ.get('MAIL_USERNAME')
        app.config["MAIL_PASSWORD"] = os.environ.get('MAIL_PASSWORD')
        app.config["MAIL_DEFAULT_SENDER"] = os.environ.get('MAIL_DEFAULT_SENDER')

    print(app.config)

    mail.init_app(app)

    from .models import db
    db.init_app(app)

    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    from . import views
    app.register_blueprint(views.bp)

    return app
