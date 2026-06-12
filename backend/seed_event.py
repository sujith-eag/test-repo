import os

from sqlalchemy import inspect, text

from extensions import db
from models.challenge import Challenge


FRONTEND_FLAGS = {
    "FLAG_META_TAG_FRAGMENT": "CTF{meta_tag_fragment}",
    "FLAG_APP_SHELL_MARKER": "CTF{app_shell_marker}",
    "FLAG_HOME_INVISIBLE_FRAGMENT": "CTF{home_invisible_fragment}",
    "FLAG_CSS_CLASS_FRAGMENT": "CTF{css_class_fragment}",
    "FLAG_NAVBAR_TRACE": "CTF{navbar_trace}",
    "FLAG_SUBMIT_PANEL_TRACE": "CTF{submit_panel_trace}",
}

EVENT_CHALLENGES = [
    {
        "slug": "meta-tag-fragment",
        "title": "Meta Tag Fragment",
        "category": "Frontend Forensics",
        "difficulty": "Easy",
        "description": "The first fragment is attached to the document before the page even renders.",
        "hint": "Inspect the page head in the browser source.",
        "points": 50,
        "order_index": 5,
        "env_key": "FLAG_META_TAG_FRAGMENT",
        "fallback": FRONTEND_FLAGS["FLAG_META_TAG_FRAGMENT"],
    },
    {
        "slug": "app-shell-marker",
        "title": "App Shell Marker",
        "category": "Frontend Forensics",
        "difficulty": "Easy",
        "description": "The application shell carries a classified marker for operators who inspect the DOM.",
        "hint": "Inspect the top-level app container.",
        "points": 50,
        "order_index": 6,
        "env_key": "FLAG_APP_SHELL_MARKER",
        "fallback": FRONTEND_FLAGS["FLAG_APP_SHELL_MARKER"],
    },
    {
        "slug": "home-invisible-fragment",
        "title": "Home Invisible Fragment",
        "category": "Frontend Forensics",
        "difficulty": "Easy",
        "description": "A message is present on the home page, but not visible to normal operators.",
        "hint": "Inspect hidden elements on the homepage.",
        "points": 50,
        "order_index": 7,
        "env_key": "FLAG_HOME_INVISIBLE_FRAGMENT",
        "fallback": FRONTEND_FLAGS["FLAG_HOME_INVISIBLE_FRAGMENT"],
    },
    {
        "slug": "css-class-fragment",
        "title": "CSS Class Fragment",
        "category": "Frontend Forensics",
        "difficulty": "Easy",
        "description": "Some protocol fragments are hidden in styling rather than markup.",
        "hint": "Search the loaded CSS for unusual CTF class names.",
        "points": 50,
        "order_index": 8,
        "env_key": "FLAG_CSS_CLASS_FRAGMENT",
        "fallback": FRONTEND_FLAGS["FLAG_CSS_CLASS_FRAGMENT"],
    },
    {
        "slug": "navbar-trace",
        "title": "Navbar Trace",
        "category": "Frontend Forensics",
        "difficulty": "Easy",
        "description": "The navigation layer contains a trace left by the Shadow Protocol team.",
        "hint": "Inspect the navigation element attributes.",
        "points": 50,
        "order_index": 9,
        "env_key": "FLAG_NAVBAR_TRACE",
        "fallback": FRONTEND_FLAGS["FLAG_NAVBAR_TRACE"],
    },
    {
        "slug": "submit-panel-trace",
        "title": "Submit Panel Trace",
        "category": "Frontend Forensics",
        "difficulty": "Easy",
        "description": "The submission panel carries a quiet trace for those who inspect before transmitting.",
        "hint": "Inspect the submit form container.",
        "points": 50,
        "order_index": 10,
        "env_key": "FLAG_SUBMIT_PANEL_TRACE",
        "fallback": FRONTEND_FLAGS["FLAG_SUBMIT_PANEL_TRACE"],
    },
    {
        "slug": "console-whisper",
        "title": "Console Whisper",
        "category": "Frontend Forensics",
        "difficulty": "Easy",
        "description": "A loose script is whispering in the dark. Inspect the client lab and listen to the console.",
        "hint": "Visit /vuln/client-lab and open DevTools.",
        "points": 50,
        "order_index": 20,
        "env_key": "FLAG_CONSOLE_WHISPER",
        "fallback": "CTF{console_whisper}",
    },
    {
        "slug": "hidden-attribute",
        "title": "Hidden Attribute",
        "category": "Frontend Forensics",
        "difficulty": "Easy",
        "description": "An operator left a classified marker in plain sight, but not in visible text.",
        "hint": "Inspect elements on /vuln/client-lab.",
        "points": 50,
        "order_index": 30,
        "env_key": "FLAG_HIDDEN_ATTRIBUTE",
        "fallback": "CTF{hidden_attribute}",
    },
    {
        "slug": "local-storage-leak",
        "title": "Local Storage Leak",
        "category": "Frontend Forensics",
        "difficulty": "Easy",
        "description": "The browser remembers more than it should. Recover the leaked local storage value.",
        "hint": "Application tab. Local Storage. /vuln/client-lab.",
        "points": 75,
        "order_index": 40,
        "env_key": "FLAG_LOCAL_STORAGE_LEAK",
        "fallback": "CTF{local_storage_leak}",
    },
    {
        "slug": "ghosts-in-robots",
        "title": "Ghosts in robots.txt",
        "category": "Recon",
        "difficulty": "Easy",
        "description": "Automated crawlers were warned away from a ghost signal. Track the file they were told to avoid.",
        "hint": "Start at /robots.txt or /vuln/robots.txt.",
        "points": 75,
        "order_index": 50,
        "env_key": "FLAG_ROBOTS_GHOST",
        "fallback": "CTF{robots_ghost}",
    },
    {
        "slug": "forgotten-humans",
        "title": "Forgotten Humans",
        "category": "Recon",
        "difficulty": "Easy",
        "description": "Not every message is written for machines. Some are left for humans.",
        "hint": "Check /humans.txt or /vuln/humans.txt.",
        "points": 75,
        "order_index": 60,
        "env_key": "FLAG_FORGOTTEN_HUMANS",
        "fallback": "CTF{forgotten_humans}",
    },
    {
        "slug": "echoes-in-the-header",
        "title": "Echoes in the Header",
        "category": "Web Exploitation",
        "difficulty": "Easy",
        "description": "The response body is quiet, but the headers echo a classified signal.",
        "hint": "Inspect the response headers from /vuln/header.",
        "points": 100,
        "order_index": 70,
        "env_key": "FLAG_HEADER_ECHO",
        "fallback": "CTF{header_echo}",
    },
    {
        "slug": "encoded-transmission",
        "title": "Encoded Transmission",
        "category": "Crypto",
        "difficulty": "Medium",
        "description": "A recovered transmission was encoded before being abandoned in the archive.",
        "hint": "Visit /vuln/transmission and identify the encoding.",
        "points": 100,
        "order_index": 80,
        "env_key": "FLAG_ENCODED_TRANSMISSION",
        "fallback": "CTF{encoded_transmission}",
    },
    {
        "slug": "reversed-signal",
        "title": "Reversed Signal",
        "category": "Crypto",
        "difficulty": "Medium",
        "description": "The signal is intact, but its direction is wrong.",
        "hint": "Visit /vuln/reverse and reverse the recovered string.",
        "points": 100,
        "order_index": 90,
        "env_key": "FLAG_REVERSED_SIGNAL",
        "fallback": "CTF{reversed_signal}",
    },
    {
        "slug": "shadow-search",
        "title": "Shadow Search",
        "category": "Web Exploitation",
        "difficulty": "Medium",
        "description": "The search endpoint reveals different intel depending on how you query it.",
        "hint": "Try searching for shadow, vault, protocol, or flag at /vuln/search?q=shadow.",
        "points": 125,
        "order_index": 100,
        "env_key": "FLAG_SHADOW_SEARCH",
        "fallback": "CTF{shadow_search}",
    },
    {
        "slug": "vault-injection",
        "title": "Vault Injection",
        "category": "Web Exploitation",
        "difficulty": "Hard",
        "description": "A training vault performs unsafe SQL lookups against an isolated in-memory database.",
        "hint": "Try /vuln/vault-search?q=alpha, then think UNION-based extraction.",
        "points": 150,
        "order_index": 110,
        "env_key": "FLAG_VAULT_INJECTION",
        "fallback": "CTF{vault_injection}",
    },
]


def flag_value(env_key, fallback):
    return os.getenv(env_key, fallback)


def ensure_phase2_schema():
    inspector = inspect(db.engine)
    if "challenges" not in inspector.get_table_names():
        return

    existing_columns = {column["name"] for column in inspector.get_columns("challenges")}
    additions = {
        "difficulty": "ALTER TABLE challenges ADD COLUMN difficulty VARCHAR(40)",
        "hint": "ALTER TABLE challenges ADD COLUMN hint TEXT",
        "order_index": "ALTER TABLE challenges ADD COLUMN order_index INTEGER",
    }

    with db.engine.begin() as connection:
        for column_name, ddl in additions.items():
            if column_name not in existing_columns:
                connection.execute(text(ddl))


def seed_event_challenges():
    ensure_phase2_schema()
    event_slugs = {item["slug"] for item in EVENT_CHALLENGES}

    for item in EVENT_CHALLENGES:
        challenge = Challenge.query.filter_by(slug=item["slug"]).first()
        data = {
            "slug": item["slug"],
            "title": item["title"],
            "category": item["category"],
            "description": item["description"],
            "points": item["points"],
            "flag": flag_value(item["env_key"], item["fallback"]),
            "difficulty": item["difficulty"],
            "hint": item["hint"],
            "order_index": item["order_index"],
            "is_active": True,
        }

        if challenge:
            for key, value in data.items():
                setattr(challenge, key, value)
        else:
            db.session.add(Challenge(**data))

    Challenge.query.filter(~Challenge.slug.in_(event_slugs)).update(
        {Challenge.is_active: False},
        synchronize_session=False,
    )

    db.session.commit()