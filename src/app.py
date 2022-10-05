import datetime

from email_validator import EmailNotValidError, validate_email
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

from news import save_posts

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ttmn.db"

db = SQLAlchemy()
db.init_app(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    time = db.Column(db.Time(timezone=True), default=datetime.time(9))


# Create tables if they don't exist
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=("GET", "POST"))
def register():
    error = False
    if request.method == "POST":
        # Get and validate the email
        email = request.form["email"]
        try:
            validate_email(email)
        except EmailNotValidError:
            error = "Invalid email"

        # Check if the email is already used
        used = User.query.filter_by(email=email).first()
        if used:
            error = "Email already used"

        # Get and validate the time
        time = request.form["timezone"]
        try:
            time = datetime.datetime.strptime(time, "%H").time()
        except ValueError:
            error = "Invalid time"

        if not error:
            # Create the user
            user = User(
                email=email,
                time=time,
            )

            # Add the user to the database
            db.session.add(user)
            db.session.commit()

            return redirect(url_for("news"))

    return render_template("signup.html", error=error)


@app.route("/news")
def news():
    posts = save_posts()
    return render_template("news.html", posts=posts)
