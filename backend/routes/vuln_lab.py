import base64
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
