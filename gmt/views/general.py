from flask import Blueprint, render_template

from ..news import get_news

bp = Blueprint("general", __name__)


@bp.route("/")
def index() -> str:
    """Render the home page."""
    return render_template("general/index.html")


@bp.route("/news")
def news():
    """Render the newspaper."""
    return render_template("general/news.html", posts=get_news(choice="BBC"))
