from flask import Blueprint, jsonify
from sqlalchemy import func

from models.submission import Submission
from models.user import User


scoreboard_bp = Blueprint("scoreboard", __name__)


@scoreboard_bp.route("", methods=["GET"])
@scoreboard_bp.route("/", methods=["GET"])
def scoreboard():
    users = User.query.order_by(User.score.desc(), User.created_at.asc()).all()

    solved_counts = dict(
        Submission.query
        .with_entities(Submission.user_id, func.count(func.distinct(Submission.challenge_id)))
        .filter(Submission.is_correct.is_(True), Submission.challenge_id.isnot(None))
        .group_by(Submission.user_id)
        .all()
    )

    rows = [
        {
            "rank": index + 1,
            "username": user.username,
            "score": user.score,
            "solved_count": int(solved_counts.get(user.id, 0)),
        }
        for index, user in enumerate(users)
    ]

    return jsonify({"scoreboard": rows})
