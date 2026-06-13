import os

from sqlalchemy import inspect, text

from extensions import db
from models.challenge import Challenge


FRONTEND_FLAGS = {
    "FLAG_META_TAG_FRAGMENT": "CTF{hawkins_meta_beacon}",
    "FLAG_APP_SHELL_MARKER": "CTF{upside_down_shell_marker}",
    "FLAG_HOME_INVISIBLE_FRAGMENT": "CTF{phantom_hawkins_signal}",
    "FLAG_CSS_CLASS_FRAGMENT": "CTF{hellfire_css_trace}",
    "FLAG_NAVBAR_TRACE": "CTF{walkie_nav_trace}",
    "FLAG_SUBMIT_PANEL_TRACE": "CTF{gate_submit_fragment}",
}

EVENT_CHALLENGES = [
    {
        "slug": "meta-tag-fragment",
        "title": "Hawkins Meta Beacon",
        "category": "Frontend Forensics",
        "difficulty": "Easy",
        "description": "A Hawkins-style beacon is attached to the document before the page even renders.",
        "hint": "Inspect the page head in the browser source.",
        "points": 50,
        "order_index": 5,
        "env_key": "FLAG_META_TAG_FRAGMENT",
        "fallback": FRONTEND_FLAGS["FLAG_META_TAG_FRAGMENT"],
    },
    {
        "slug": "app-shell-marker",
        "title": "Upside Down Shell Marker",
        "category": "Frontend Forensics",
        "difficulty": "Easy",
        "description": "The outer application shell carries a marker from the Upside Down.",
        "hint": "Inspect the top-level app container.",
        "points": 50,
        "order_index": 6,
        "env_key": "FLAG_APP_SHELL_MARKER",
        "fallback": FRONTEND_FLAGS["FLAG_APP_SHELL_MARKER"],
    },
    {
        "slug": "home-invisible-fragment",
        "title": "Phantom Hawkins Signal",
        "category": "Frontend Forensics",
        "difficulty": "Easy",
        "description": "A phantom signal is present on the homepage, but not visible to normal operators.",
        "hint": "Inspect hidden elements on the homepage.",
        "points": 50,
        "order_index": 7,
        "env_key": "FLAG_HOME_INVISIBLE_FRAGMENT",
        "fallback": FRONTEND_FLAGS["FLAG_HOME_INVISIBLE_FRAGMENT"],
    },
    {
        "slug": "css-class-fragment",
        "title": "Hellfire CSS Trace",
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
        "title": "Walkie Nav Trace",
        "category": "Frontend Forensics",
        "difficulty": "Easy",
        "description": "The navigation layer carries a walkie-style trace.",
        "hint": "Inspect the navigation element attributes.",
        "points": 50,
        "order_index": 9,
        "env_key": "FLAG_NAVBAR_TRACE",
        "fallback": FRONTEND_FLAGS["FLAG_NAVBAR_TRACE"],
    },
    {
        "slug": "submit-panel-trace",
        "title": "Gate Submit Fragment",
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
        "title": "Static on Channel 6",
        "category": "Frontend Forensics",
        "difficulty": "Easy",
        "description": "A client-side lab emits radio static. Listen to in console where it speaks.",
        "hint": "Visit /vuln/client-lab and open DevTools.",
        "points": 50,
        "order_index": 20,
        "env_key": "FLAG_CONSOLE_WHISPER",
        "fallback": "CTF{static_console_whisper}",
    },
    {
        "slug": "hidden-attribute",
        "title": "Hawkins Lab Attribute",
        "category": "Frontend Forensics",
        "difficulty": "Easy",
        "description": "A Hawkins Lab marker is attached to an element.",
        "hint": "Inspect elements on /vuln/client-lab.",
        "points": 50,
        "order_index": 30,
        "env_key": "FLAG_HIDDEN_ATTRIBUTE",
        "fallback": "CTF{hawkins_lab_attribute}",
    },
    {
        "slug": "local-storage-leak",
        "title": "Browser Memory Trace",
        "category": "Frontend Forensics",
        "difficulty": "Easy",
        "description": "The browser remembers more than it should. Recover the leaked local storage value.",
        "hint": "Application tab. Local Storage. /vuln/client-lab.",
        "points": 75,
        "order_index": 40,
        "env_key": "FLAG_LOCAL_STORAGE_LEAK",
        "fallback": "CTF{browser_memory_trace}",
    },
    {
        "slug": "ghosts-in-robots",
        "title": "Crawlers at the Gate",
        "category": "Recon",
        "difficulty": "Easy",
        "description": "A gate-related clue was left for crawlers. Read the standard crawler instruction file.",
        "hint": "Start at /robots.txt or /vuln/robots.txt.",
        "points": 75,
        "order_index": 50,
        "env_key": "FLAG_ROBOTS_GHOST",
        "fallback": "CTF{crawler_ignored_gate}",
    },
    {
        "slug": "forgotten-humans",
        "title": "Hawkins Lab Staff Note",
        "category": "Recon",
        "difficulty": "Easy",
        "description": "A lab note was written for humans, not machines.",
        "hint": "Check /humans.txt or /vuln/humans.txt.",
        "points": 75,
        "order_index": 60,
        "env_key": "FLAG_FORGOTTEN_HUMANS",
        "fallback": "CTF{human_lab_note}",
    },
    {
        "slug": "echoes-in-the-header",
        "title": "Signal Above the Body",
        "category": "Web Exploitation",
        "difficulty": "Easy",
        "description": "The body says little, but the signal travels above it.",
        "hint": "Inspect the response headers from /vuln/header.",
        "points": 100,
        "order_index": 70,
        "env_key": "FLAG_HEADER_ECHO",
        "fallback": "CTF{upside_down_header_echo}",
    },
    {
        "slug": "encoded-transmission",
        "title": "Encoded Walkie Transmission",
        "category": "Crypto",
        "difficulty": "Medium",
        "description": "A walkie transmission was archived in a common encoding. Identify and decode it.",
        "hint": "Visit /vuln/transmission and identify the encoding.",
        "points": 100,
        "order_index": 80,
        "env_key": "FLAG_ENCODED_TRANSMISSION",
        "fallback": "CTF{encoded_walkie_transmission}",
    },
    {
        "slug": "reversed-signal",
        "title": "Reversed Red Signal",
        "category": "Crypto",
        "difficulty": "Medium",
        "description": "The red signal is complete, but it is facing the wrong direction. Reverse it.",
        "hint": "Visit /vuln/reverse and reverse the recovered string.",
        "points": 100,
        "order_index": 90,
        "env_key": "FLAG_REVERSED_SIGNAL",
        "fallback": "CTF{reversed_vecna_signal}",
    },
    {
        "slug": "shadow-search",
        "title": "Hawkins Archive Search",
        "category": "Web Exploitation",
        "difficulty": "Medium",
        "description": "The Hawkins archive search reveals different records based on terms you query.",
        "hint": "Try searching for shadow, vault, protocol, or flag at /vuln/search?q=shadow.",
        "points": 125,
        "order_index": 100,
        "env_key": "FLAG_SHADOW_SEARCH",
        "fallback": "CTF{hawkins_archive_index}",
    },
    {
        "slug": "vault-injection",
        "title": "Lab Vault Breach",
        "category": "Web Exploitation",
        "difficulty": "Hard",
        "description": "A lab vault performs unsafe SQL lookups in an isolated training database.",
        "hint": "Try /vuln/vault-search?q=alpha, then think UNION-based extraction.",
        "points": 150,
        "order_index": 110,
        "env_key": "FLAG_VAULT_INJECTION",
        "fallback": "CTF{lab_vault_breach}",
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