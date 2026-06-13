from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from models.challenge import Challenge
from models.submission import Submission


challenges_bp = Blueprint("challenges", __name__)


def current_user_id_optional():
    try:
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        return int(identity) if identity else None
    except Exception:
        return None


def solved_ids_for_user(user_id):
    if not user_id:
        return set()

    rows = Submission.query.filter_by(user_id=user_id, is_correct=True).all()
    return {row.challenge_id for row in rows if row.challenge_id}


@challenges_bp.route("", methods=["GET"])
@challenges_bp.route("/", methods=["GET"])
def list_challenges():
    user_id = current_user_id_optional()
    solved_ids = solved_ids_for_user(user_id)

    challenges = (
        Challenge.query
        .filter_by(is_active=True)
        .order_by(Challenge.order_index.asc(), Challenge.points.asc())
        .all()
    )

    return jsonify({
        "challenges": [
            challenge.to_public_dict(challenge.id in solved_ids)
            for challenge in challenges
        ]
    })


@challenges_bp.route("/<slug>", methods=["GET"])
def get_challenge(slug):
    user_id = current_user_id_optional()
    solved_ids = solved_ids_for_user(user_id)

    challenge = Challenge.query.filter_by(slug=slug, is_active=True).first()
    if not challenge:
        return jsonify({"error": "Challenge not found."}), 404

    return jsonify({
        "challenge": challenge.to_public_dict(challenge.id in solved_ids)
    })
