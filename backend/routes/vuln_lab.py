import base64
import json
import os
import sqlite3

from flask import Blueprint, Response, jsonify, request


vuln_lab_bp = Blueprint("vuln_lab", __name__)


def flag(name, fallback):
    return os.getenv(name, fallback)


@vuln_lab_bp.route("/vuln/client-lab")
def client_lab():
    console_flag = flag("FLAG_CONSOLE_WHISPER", "CTF{static_speaks_first}")
    attr_flag = flag("FLAG_HIDDEN_ATTRIBUTE", "CTF{lab_tags_never_lie}")
    storage_flag = flag("FLAG_LOCAL_STORAGE_LEAK", "CTF{memory_survives_the_breach}")
    html = f"""
    <!doctype html>
    <html>
      <head><title>Hawkins Client Lab</title></head>
      <body style="background:#07070a;color:#f5f5f7;font-family:monospace;padding:32px">
        <h1>Hawkins Client Lab</h1>
        <p>The client remembers fragments from the Hawkins incident.</p>
        <section data-shadow-fragment="{attr_flag}">
          <p>Visible intel: no confirmed flag in this text.</p>
        </section>
        <script>
          console.log("Channel static fragment: {console_flag}");
          localStorage.setItem("shadow_protocol_fragment", "{storage_flag}");
        </script>
      </body>
    </html>
    """
    return Response(html, mimetype="text/html")


@vuln_lab_bp.route("/robots.txt")
@vuln_lab_bp.route("/vuln/robots.txt")
def robots_txt():
    content = f"""User-agent: *
Disallow: /vuln/ghost-signal
Disallow: /vuln/vault-search

# Gate signal recovered: {flag('FLAG_ROBOTS_GHOST', 'CTF{crawlers_avoid_the_gate}')}
"""
    return Response(content, mimetype="text/plain")


@vuln_lab_bp.route("/humans.txt")
@vuln_lab_bp.route("/vuln/humans.txt")
def humans_txt():
    content = f"""Hawkins Lab incident notes:
- Operator Redacted
- Signal Archivist
- Lab Systems Watcher

Human-readable lab note: {flag('FLAG_FORGOTTEN_HUMANS', 'CTF{humans_left_the_note}')}
"""
    return Response(content, mimetype="text/plain")


@vuln_lab_bp.route("/vuln/header")
def header_echo():
    response = jsonify({"message": "The body is quiet. The signal is above it."})
    response.headers["X-Shadow-Flag"] = flag("FLAG_HEADER_ECHO", "CTF{headers_echo_from_below}")
    return response


@vuln_lab_bp.route("/vuln/transmission")
def encoded_transmission():
    encoded = base64.b64encode(flag("FLAG_ENCODED_TRANSMISSION", "CTF{walkie_payload_decoded}").encode()).decode()
    return jsonify({
        "classification": "encoded-walkie-transmission",
        "encoding": "base64",
        "payload": encoded,
    })


@vuln_lab_bp.route("/vuln/reverse")
def reversed_signal():
    return jsonify({
        "classification": "reversed-red-signal",
        "payload": flag("FLAG_REVERSED_SIGNAL", "CTF{vecna_signal_reversed}")[::-1],
    })


@vuln_lab_bp.route("/vuln/search", methods=["GET", "POST"])
def shadow_search():
    query = request.values.get("q", "").lower()
    records = {
        "shadow": "Hawkins activity confirmed near the old relay.",
        "vault": "Vault records are indexed under restricted protocol terms.",
        "protocol": "Incident fragments detected. Try querying for the obvious target.",
        "flag": flag("FLAG_SHADOW_SEARCH", "CTF{archive_knows_the_word}"),
    }
    matches = [value for key, value in records.items() if query and query in key]
    return jsonify({"query": query, "results": matches or ["No matching intel."]})


def build_vault_database():
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE vault_records (id INTEGER, title TEXT, body TEXT)")
    cursor.execute("CREATE TABLE secret_flags (id INTEGER, flag TEXT, note TEXT)")
    cursor.executemany(
        "INSERT INTO vault_records VALUES (?, ?, ?)",
        [
            (1, "alpha", "Relay map unavailable."),
            (2, "bravo", "Transmission checksum invalid."),
            (3, "charlie", "Archive index corrupted."),
        ],
    )
    cursor.execute(
        "INSERT INTO secret_flags VALUES (1, ?, 'vault-injection')",
        (flag("FLAG_VAULT_INJECTION", "CTF{vault_trusts_the_wrong_input}"),),
    )
    connection.commit()
    return connection


@vuln_lab_bp.route("/vuln/vault-search", methods=["GET", "POST"])
def vault_search():
    query = request.values.get("q", "")
    sql = f"SELECT id, title, body FROM vault_records WHERE title LIKE '%{query}%'"
    connection = build_vault_database()

    try:
        rows = connection.execute(sql).fetchall()
        results = [dict(row) for row in rows]
        return jsonify({
            "query": query,
            "sql_preview": sql,
            "results": results or [{"message": "No vault records matched."}],
            "hint": "The lab vault uses unsafe string-built SQL against an isolated training database.",
        })
    except sqlite3.Error as error:
        return jsonify({
            "query": query,
            "sql_preview": sql,
            "error": str(error),
            "hint": "The SELECT returns three columns: id, title, body.",
        }), 400
    finally:
        connection.close()


@vuln_lab_bp.route("/vuln/vault", methods=["GET", "POST"])
def vault_legacy_hint():
    return jsonify({
        "message": "Lab vault lookup moved to /vuln/vault-search?q=alpha",
        "hint": "Try a UNION-style payload when searching the isolated vault database.",
    })

@vuln_lab_bp.route("/vuln/cookie")
def hawkins_cookie():
    response = jsonify({
        "message": "A small lab token was stored by the response.",
        "check": "Inspect response cookies or browser storage for the signal.",
    })
    response.set_cookie(
        "hawkins_cookie_signal",
        flag("FLAG_HAWKINS_COOKIE_SIGNAL", "CTF{cookie_from_the_lab}"),
        httponly=False,
        samesite="Lax",
    )
    return response


@vuln_lab_bp.route("/vuln/frequency")
def frequency_channel():
    channel = request.args.get("channel", "")
    if channel == "11":
        return jsonify({
            "channel": channel,
            "status": "locked-on",
            "signal": flag("FLAG_CHANNEL_ELEVEN_FREQUENCY", "CTF{eleven_found_the_frequency}"),
        })

    return jsonify({
        "channel": channel or "unset",
        "status": "static",
        "message": "No stable signal on this channel.",
    })


@vuln_lab_bp.route("/vuln/debug")
def debug_lab():
    mode = request.args.get("mode", "").lower()
    if mode == "true":
        return jsonify({
            "debug": True,
            "lab_status": "diagnostic mode enabled",
            "debug_fragment": flag("FLAG_DEBUG_LAB_LEAK", "CTF{debug_mode_broke_containment}"),
        })

    return jsonify({
        "debug": False,
        "lab_status": "normal",
        "message": "Diagnostics are quiet.",
    })

@vuln_lab_bp.route("/vuln/lab-record")
def lab_record_drift():
    record_id = request.args.get("id", "1")
    records = {
        "1": {
            "record_id": 1,
            "owner": "field-team",
            "classification": "public",
            "summary": "Radio interference logged near the tree line.",
        },
        "2": {
            "record_id": 2,
            "owner": "maintenance",
            "classification": "public",
            "summary": "Power fluctuations observed in the west corridor.",
        },
        "3": {
            "record_id": 3,
            "owner": "archive-desk",
            "classification": "public",
            "summary": "Paper badge audit scheduled after midnight.",
        },
        "11": {
            "record_id": 11,
            "owner": "restricted-lab",
            "classification": "restricted",
            "summary": "Gate phrase recovered from unauthorized record access.",
            "gate_phrase": "close-the-gate",
            "flag": flag("FLAG_LAB_RECORD_DRIFT", "CTF{records_should_check_owners}"),
        },
    }

    return jsonify({
        "requested_id": record_id,
        "record": records.get(record_id, {
            "error": "record not found",
            "available_public_examples": [1, 2, 3],
        }),
        "training_note": "This isolated lab demonstrates object-level authorization drift.",
    })


@vuln_lab_bp.route("/vuln/archive")
def archive_slip():
    requested_file = request.args.get("file", "welcome.txt")
    archive_files = {
        "welcome.txt": "Hawkins Archive: public terminal online. Try reading named records from the index.",
        "radio-log.txt": "Radio Log: channel checks moved to the control room.",
        "incident-report.txt": "Incident Report: a restricted gate note was filed outside the public folder.",
        "../restricted/gate-note.txt": (
            "Restricted Gate Note\n"
            "archive_keyword=mirkwood\n"
            f"flag={flag('FLAG_ARCHIVE_SLIP', 'CTF{archives_should_not_trust_paths}')}"
        ),
    }

    return Response(
        archive_files.get(
            requested_file,
            "Archive miss. Public files: welcome.txt, radio-log.txt, incident-report.txt",
        ),
        mimetype="text/plain",
    )


def encode_badge_payload(payload):
    raw = json.dumps(payload, separators=(",", ":")).encode()
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def decode_badge_payload(token):
    padded = token + "=" * (-len(token) % 4)
    decoded = base64.urlsafe_b64decode(padded.encode()).decode()
    return json.loads(decoded)


@vuln_lab_bp.route("/vuln/badge")
def paper_badge():
    starter_payload = {"name": "rookie", "role": "guest", "zone": "public"}
    token = request.args.get("token", "")

    if not token:
        return jsonify({
            "message": "Badge scanner online. The sample badge is encoded, not encrypted.",
            "sample_payload": starter_payload,
            "sample_token": encode_badge_payload(starter_payload),
            "hint": "Decode the token, inspect the JSON fields, then re-encode a stronger badge.",
        })

    try:
        badge = decode_badge_payload(token)
    except Exception:
        return jsonify({
            "error": "badge token could not be decoded as url-safe base64 JSON",
        }), 400

    role = str(badge.get("role", "")).lower()
    zone = str(badge.get("zone", "")).lower()
    if role == "chief" and zone in {"restricted", "gate"}:
        return jsonify({
            "status": "accepted",
            "badge": badge,
            "final_gate_role": "chief",
            "flag": flag("FLAG_PAPER_BADGE", "CTF{encoded_badges_are_not_auth}"),
        })

    return jsonify({
        "status": "denied",
        "badge": badge,
        "message": "Guest paper badges cannot enter the restricted wing.",
    }), 403


@vuln_lab_bp.route("/vuln/control", methods=["GET", "POST", "PUT"])
def control_room_method():
    if request.method == "GET":
        return jsonify({
            "method": "GET",
            "status": "read-only",
            "message": "Control room is online, but observation alone will not move the gate.",
        })

    if request.method == "POST":
        return jsonify({
            "method": "POST",
            "status": "operator-checkpoint",
            "message": "A stronger maintenance method is required for the sealed control.",
            "channel_clue": "The final gate channel is a single digit seen after full method control.",
        })

    return jsonify({
        "method": "PUT",
        "status": "control-updated",
        "final_gate_channel": "7",
        "flag": flag("FLAG_CONTROL_ROOM_METHOD", "CTF{methods_change_the_message}"),
    })


@vuln_lab_bp.route("/vuln/api/clearance", methods=["GET", "POST"])
def clearance_override():
    if request.method == "GET":
        return jsonify({
            "message": "POST a JSON clearance request to the training API.",
            "example": {"name": "operator", "clearance": "visitor", "sector": "public"},
            "hint": "APIs sometimes read fields the interface never shows.",
        })

    payload = request.get_json(silent=True) or {}
    clearance = str(payload.get("clearance", "")).lower()
    sector = str(payload.get("sector", "")).lower()
    override = payload.get("override") is True

    if clearance in {"admin", "director"} and sector == "restricted" and override:
        return jsonify({
            "status": "override accepted",
            "gate_phrase": "close-the-gate",
            "flag": flag("FLAG_CLEARANCE_OVERRIDE", "CTF{hidden_fields_open_doors}"),
        })

    return jsonify({
        "status": "denied",
        "received": payload,
        "message": "Clearance request lacks restricted override authority.",
    }), 403


def caesar_shift(text, amount):
    shifted = []
    for char in text:
        if "a" <= char <= "z":
            shifted.append(chr((ord(char) - ord("a") + amount) % 26 + ord("a")))
        elif "A" <= char <= "Z":
            shifted.append(chr((ord(char) - ord("A") + amount) % 26 + ord("A")))
        else:
            shifted.append(char)
    return "".join(shifted)


@vuln_lab_bp.route("/vuln/shifted-broadcast")
def shifted_broadcast():
    plain = (
        "Rotation note: channel seven matters for the final gate. "
        f"Flag: {flag('FLAG_SHIFTED_BROADCAST', 'CTF{rotation_reveals_the_broadcast}')}"
    )
    return jsonify({
        "classification": "shifted-broadcast",
        "cipher": "caesar",
        "shift": 13,
        "payload": caesar_shift(plain, 13),
        "hint": "A common rotation can make this readable again.",
    })


@vuln_lab_bp.route("/vuln/final-gate", methods=["GET", "POST"])
def final_gate():
    payload = request.get_json(silent=True) if request.method == "POST" else None
    source = payload or request.values

    submitted = {
        "channel": str(source.get("channel", "")).strip().lower(),
        "keyword": str(source.get("keyword", "")).strip().lower(),
        "role": str(source.get("role", "")).strip().lower(),
        "phrase": str(source.get("phrase", "")).strip().lower(),
    }
    expected = {
        "channel": "7",
        "keyword": "mirkwood",
        "role": "chief",
        "phrase": "close-the-gate",
    }

    missing = [key for key, value in submitted.items() if not value]
    incorrect = [key for key, value in submitted.items() if value and value != expected[key]]

    if submitted == expected:
        return jsonify({
            "status": "gate sealed",
            "message": "All four keys aligned. The Shadow Protocol is contained.",
            "flag": flag("FLAG_FINAL_GATE", "CTF{four_keys_close_the_shadow_gate}"),
        })

    return jsonify({
        "status": "gate unstable",
        "received": submitted,
        "missing_fields": missing,
        "incorrect_fields": incorrect,
        "needs": ["channel", "keyword", "role", "phrase"],
        "hint": "The final lock combines clues from records, archive notes, badge data, and control signals.",
    }), 400

