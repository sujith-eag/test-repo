from flask import Blueprint, jsonify

from models.user import User


scoreboard_bp = Blueprint("scoreboard", __name__)


@scoreboard_bp.route("", methods=["GET"])
@scoreboard_bp.route("/", methods=["GET"])
def scoreboard():
    users = User.query.order_by(User.score.desc(), User.created_at.asc()).all()
    rows = [
        {"rank": index + 1, "username": user.username, "score": user.score}
        for index, user in enumerate(users)
    ]
    return jsonify({"scoreboard": rows})
