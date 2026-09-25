import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "action_grid.db")

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def build_card_html(game):
    st_state = str(game["status_state"])
    st_detail = str(game["status_detail"])
    is_rz = int(game["is_red_zone"] or 0) == 1
    tv = str(game["broadcast"] or "TV")

    a_name = str(game["away_name"])
    a_rec = str(game["away_record"])
    a_score = str(game["away_score"]) if st_state in ["in", "post"] else "-"
    a_logo = str(game["away_logo"])
    a_color = str(game["away_color"] or "#00e5ff")

    h_name = str(game["home_name"])
    h_rec = str(game["home_record"])
    h_score = str(game["home_score"]) if st_state in ["in", "post"] else "-"
    h_logo = str(game["home_logo"])
    h_color = str(game["home_color"] or "#ff2a6d")

    home_prob = float(game["home_win_prob"] or 0.5) * 100
    away_prob = 100.0 - home_prob

    badge = f"<span class='sb-badge-live'>LIVE {st_detail}</span>" if st_state == "in" else (f"<span class='sb-badge-final'>{st_detail}</span>" if st_state == "post" else f"<span class='sb-badge-pre'>{st_detail}</span>")
    rz_class = "red-zone" if (is_rz and st_state == "in") else ""
    situation = str(game["down_distance_text"]) if st_state == "in" else ("Kickoff: " + str(game["kickoff_time"])[-8:-3] if game["kickoff_time"] else "Pregame")
    last_play = str(game["last_play_text"] or "")
    last_play_div = f"<div class='sb-last-play'><b>Last Play:</b> {last_play}</div>" if last_play and st_state == "in" else ""

    # Zero newlines or indentations inside HTML tags
    return (
        f"<div class='sb-card {rz_class}'>"
        f"<div class='sb-hdr'>{badge}<span style='color:#8b949e;'>TV: <b style='color:#cad3df;'>{tv}</b></span></div>"
        f"<div class='sb-matchup'>"
        f"<div class='sb-team'><img src='{a_logo}' class='sb-logo' onerror=\"this.style.display='none'\"><div class='sb-team-meta'><b>{a_name}</b><span>{a_rec}</span></div></div>"
        f"<div class='sb-score-center'><div class='sb-score-val'>{a_score} - {h_score}</div><div style='font-size:11px; color:#8b949e; margin-top:2px;'>{situation}</div></div>"
        f"<div class='sb-team home'><div class='sb-team-meta'><b>{h_name}</b><span>{h_rec}</span></div><img src='{h_logo}' class='sb-logo' onerror=\"this.style.display='none'\"></div>"
        f"</div>"
        f"<div class='sb-prob-bar'><div class='sb-prob-fill' style='width:{away_prob}%; background:{a_color};'></div><div class='sb-prob-fill' style='width:{home_prob}%; background:{h_color};'></div></div>"
        f"<div class='sb-telemetry'>"
        f"<div class='sb-tel-item'><span>SPREAD</span><b>{game['spread_detail'] or 'EVEN'}</b></div>"
        f"<div class='sb-tel-item'><span>TOTAL</span><b>O/U {game['over_under'] or 'N/A'}</b></div>"
        f"<div class='sb-tel-item'><span>WIN PROB</span><b>{home_prob:.0f}% {game['home_abbr']}</b></div>"
        f"</div>"
        f"{last_play_div}"
        f"</div>"
    )

def run_self_audit():
    sample = {
        "game_id": "t1", "status_state": "in", "status_detail": "Q2", "is_red_zone": 0, "broadcast": "FOX",
        "away_name": "Lions", "away_record": "2-0", "away_score": 14, "away_logo": "", "away_color": "#0076b6",
        "home_name": "Packers", "home_record": "1-1", "home_score": 10, "home_logo": "", "home_color": "#203731",
        "home_win_prob": 0.45, "down_distance_text": "2nd & 5", "kickoff_time": "", "spread_detail": "DET -2.5",
        "over_under": 48.5, "home_abbr": "GB", "last_play_text": "Pass complete"
    }
    assert "<div class='sb-card" in build_card_html(sample)
    print("✅ [PASS] Clean cards verified.")
    return True

if __name__ == "__main__":
    run_self_audit()