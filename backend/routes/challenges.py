from flask import Blueprint, jsonify

from models.challenge import Challenge


challenges_bp = Blueprint("challenges", __name__)


@challenges_bp.route("", methods=["GET"])
@challenges_bp.route("/", methods=["GET"])
def list_challenges():
    challenges = Challenge.query.filter_by(is_active=True).order_by(Challenge.points.asc(), Challenge.id.asc()).all()
    return jsonify({"challenges": [challenge.to_public_dict() for challenge in challenges]})


@challenges_bp.route("/<slug>", methods=["GET"])
def get_challenge(slug):
    challenge = Challenge.query.filter_by(slug=slug, is_active=True).first()
    if not challenge:
        return jsonify({"error": "Challenge not found."}), 404
    return jsonify({"challenge": challenge.to_public_dict()})
