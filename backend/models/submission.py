from datetime import datetime, timezone

from extensions import db


class Submission(db.Model):
    __tablename__ = "submissions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey("challenges.id"), nullable=True, index=True)
    submitted_flag = db.Column(db.String(255), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False, default=False)
    points_awarded = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    user = db.relationship("User", back_populates="submissions")
    challenge = db.relationship("Challenge", back_populates="submissions")

    def to_dict(self):
        return {
            "id": self.id,
            "challenge": self.challenge.to_public_dict() if self.challenge else None,
            "submitted_flag": self.submitted_flag,
            "is_correct": self.is_correct,
            "points_awarded": self.points_awarded,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
