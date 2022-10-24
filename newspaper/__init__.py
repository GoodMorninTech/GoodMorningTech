from flask import Flask
from flask_mail import Mail
import os
mail = Mail()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    try:
        app.config.from_pyfile("config.py")
    except OSError:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///newspaper.db')
        # Print this variable in Flask
        print(app.config['SQLALCHEMY_DATABASE_URI'])

    mail.init_app(app)

    from .models import db
    db.init_app(app)

    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    from . import views
    app.register_blueprint(views.bp)

    return app
