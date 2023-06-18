import datetime

from bson import ObjectId
from flask import Blueprint, Response, render_template, request
from flask_login import current_user

from gmt import mongo
from gmt.utils import parse_json

bp = Blueprint("api", __name__)


@bp.route("/api/")
def api():
    if current_user.is_authenticated:
        current_user.writer = mongo.db.writers.find_one(
            {"_id": ObjectId(current_user.id)}
        )

    return render_template("api/api.html")


@bp.route("/api/news/")
def news():
    api_key = request.headers.get("X-API-KEY")
    user = mongo.db.users.find_one({"_id": ObjectId(api_key)})

    # if the user with that id isn't in the db, return 401
    if not user:
        return Response(status=401)

    posts = list(
        mongo.db.articles.find(
            {
                "date": {
                    "$gte": datetime.datetime.utcnow() - datetime.timedelta(hours=25)
                }
            }
        )
    )

    return parse_json(posts)
