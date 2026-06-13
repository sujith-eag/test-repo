import os


EVENT_NAME = os.getenv("EVENT_NAME", "Shadow Protocol")
REGISTRATION_ENABLED = os.getenv("REGISTRATION_ENABLED", "true").lower() == "true"
SUBMISSIONS_ENABLED = os.getenv("SUBMISSIONS_ENABLED", "true").lower() == "true"
SCOREBOARD_VISIBLE = os.getenv("SCOREBOARD_VISIBLE", "true").lower() == "true"


def get_event_info():
    return {
        "name": EVENT_NAME,
        "registration_enabled": REGISTRATION_ENABLED,
        "submissions_enabled": SUBMISSIONS_ENABLED,
        "scoreboard_visible": SCOREBOARD_VISIBLE,
        "theme": "shadow-protocol",
        "status": "live" if SUBMISSIONS_ENABLED else "locked",
    }


def is_registration_enabled():
    return REGISTRATION_ENABLED


def is_submissions_enabled():
    return SUBMISSIONS_ENABLED


def is_scoreboard_visible():
    return SCOREBOARD_VISIBLE
