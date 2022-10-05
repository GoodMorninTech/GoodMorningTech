from flask import Flask, render_template
from news import save_posts
app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register')
def register():
    return render_template("signup.html")


@app.route('/news')
def news():
    posts = save_posts()
    return render_template("news.html", posts=posts)


if __name__ == "__main__":
    app.run()
