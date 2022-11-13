import datetime
import jwt
from functools import wraps

from flask import Blueprint, current_app, make_response, jsonify, request

bp = Blueprint("auth", __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get("token")

        if not token:
            return jsonify({"message": "Token is missing"}), 403

        try:
            jwt.decode(token, current_app.config["SECRET_KEY"], ["HS256"])
        except:
            return jsonify({"message": "Token is invalid"}), 403

        return f(*args, **kwargs)

    return decorated


@bp.route("/send")
@token_required
def send_emails():
    return jsonify({"message": "You can view this!"})


@bp.route("/login")
def login():
    auth = request.authorization
    if auth and auth.password == "password":
        token = jwt.encode(
            {
                "user": auth.username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
            },
            current_app.config["SECRET_KEY"],
        )

        return jsonify({"token": token})

    return make_response("Could not verify!", 401, {"WWW-Authenticate": 'Basic realm="Login Required"'})
