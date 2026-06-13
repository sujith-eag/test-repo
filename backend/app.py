from pathlib import Path

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

from config import Config
from event_config import get_event_info
from extensions import db, jwt
from routes.auth import auth_bp
from routes.challenges import challenges_bp
from routes.scoreboard import scoreboard_bp
from routes.submissions import submissions_bp
from routes.vuln_lab import vuln_lab_bp
from seed_event import seed_event_challenges

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIST = BASE_DIR.parent / "frontend" / "dist"


def create_app():
    app = Flask(__name__, static_folder=None)
    app.config.from_object(Config)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(challenges_bp, url_prefix="/api/challenges")
    app.register_blueprint(submissions_bp, url_prefix="/api/submissions")
    app.register_blueprint(scoreboard_bp, url_prefix="/api/scoreboard")
    app.register_blueprint(vuln_lab_bp)

    @app.route("/api/health")
    def health():
        return jsonify({"status": "ok", "service": "shadow-protocol", "phase": 2})

    @app.route("/api/event")
    def event_info():
        return jsonify({"event": get_event_info()})

    with app.app_context():
        db.create_all()
        seed_event_challenges()

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_frontend(path):
        if path.startswith("api/") or path.startswith("vuln/"):
            return jsonify({"error": "Route not found"}), 404

        if not FRONTEND_DIST.exists():
            return jsonify({
                "message": "Shadow Protocol backend is running.",
                "frontend": "Build the frontend with `npm run build` or use Vite in development.",
                "health": "/api/health"
            })

        file_path = FRONTEND_DIST / path
        if path and file_path.exists() and file_path.is_file():
            return send_from_directory(FRONTEND_DIST, path)

        return send_from_directory(FRONTEND_DIST, "index.html")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)
