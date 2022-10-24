import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    time = db.Column(db.Time(timezone=True), default=datetime.time(8))
    confirmed = db.Column(db.Boolean, default=False)
