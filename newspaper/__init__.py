from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("config.py")

from .models import db

db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

from . import views
