from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from extensions import db
from models.challenge import Challenge
from models.submission import Submission
from models.user import User


submissions_bp = Blueprint("submissions", __name__)


@submissions_bp.route("", methods=["POST"])
@submissions_bp.route("/", methods=["POST"])
@jwt_required()
def submit_flag():
    data = request.get_json(silent=True) or {}
    submitted_flag = (data.get("flag") or "").strip()

    if not submitted_flag:
        return jsonify({"error": "Flag is required."}), 400

    user = db.session.get(User, int(get_jwt_identity()))
    if not user:
        return jsonify({"error": "User not found."}), 404

    challenge = Challenge.query.filter_by(flag=submitted_flag, is_active=True).first()

    if not challenge:
        submission = Submission(
            user_id=user.id,
            submitted_flag=submitted_flag,
            is_correct=False,
            points_awarded=0,
        )
        db.session.add(submission)
        db.session.commit()
        return jsonify({
            "status": "incorrect",
            "message": "Incorrect flag. Keep investigating.",
            "user": user.to_public_dict(),
        }), 200

    existing_correct = Submission.query.filter_by(
        user_id=user.id,
        challenge_id=challenge.id,
        is_correct=True,
    ).first()

    if existing_correct:
        duplicate = Submission(
            user_id=user.id,
            challenge_id=challenge.id,
            submitted_flag=submitted_flag,
            is_correct=True,
            points_awarded=0,
        )
        db.session.add(duplicate)
        db.session.commit()
        return jsonify({
            "status": "duplicate",
            "message": "Correct flag, but points were already awarded for this challenge.",
            "challenge": challenge.to_public_dict(),
            "points_awarded": 0,
            "user": user.to_public_dict(),
        }), 200

    user.score += challenge.points
    submission = Submission(
        user_id=user.id,
        challenge_id=challenge.id,
        submitted_flag=submitted_flag,
        is_correct=True,
        points_awarded=challenge.points,
    )
    db.session.add(submission)
    db.session.commit()

    return jsonify({
        "status": "correct",
        "message": "Flag accepted. Points awarded.",
        "challenge": challenge.to_public_dict(),
        "points_awarded": challenge.points,
        "user": user.to_public_dict(),
    }), 200


@submissions_bp.route("/me", methods=["GET"])
@jwt_required()
def my_submissions():
    user = db.session.get(User, int(get_jwt_identity()))
    if not user:
        return jsonify({"error": "User not found."}), 404

    submissions = Submission.query.filter_by(user_id=user.id).order_by(Submission.created_at.desc()).all()
    return jsonify({"submissions": [submission.to_dict() for submission in submissions]})
