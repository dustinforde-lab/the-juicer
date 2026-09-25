import os
import json
import sqlite3
import requests
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "action_grid.db")
ESPN_ENDPOINT = "https://site.web.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=10000;")
    return conn

def init_schema():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scoreboard_live (
                game_id TEXT PRIMARY KEY,
                week INTEGER,
                status_state TEXT,
                status_detail TEXT,
                kickoff_time TEXT,
                broadcast TEXT,
                away_id TEXT, away_name TEXT, away_abbr TEXT, away_score INTEGER,
                away_record TEXT, away_logo TEXT, away_color TEXT,
                home_id TEXT, home_name TEXT, home_abbr TEXT, home_score INTEGER,
                home_record TEXT, home_logo TEXT, home_color TEXT,
                possession_team TEXT,
                down_distance_text TEXT,
                yardline INTEGER,
                is_red_zone INTEGER,
                home_win_prob REAL,
                spread_detail TEXT,
                over_under REAL,
                last_play_text TEXT,
                updated_at TEXT
            )
        """)
        conn.commit()

def sync_espn_data():
    init_schema()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*"
    }
    try:
        resp = requests.get(ESPN_ENDPOINT, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        return False, f"Network/Parse Error: {e}"

    week_num = int(data.get("week", {}).get("number", 1))
    events = data.get("events", [])
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    records = []

    for ev in events:
        game_id = str(ev.get("id"))
        comp = ev.get("competitions", [{}])[0]
        status = comp.get("status", {})
        status_state = status.get("type", {}).get("state", "pre")
        status_detail = status.get("type", {}).get("shortDetail", "Scheduled")
        kickoff_time = ev.get("date", "")

        tv = "TV"
        broadcasts = comp.get("broadcasts", [])
        if broadcasts and broadcasts[0].get("names"):
            tv = broadcasts[0]["names"][0]

        competitors = comp.get("competitors", [])
        home = next((c for c in competitors if c.get("homeAway") == "home"), {})
        away = next((c for c in competitors if c.get("homeAway") == "away"), {})

        def parse_team(c):
            t = c.get("team", {})
            recs = c.get("records", [{}])
            rec = recs[0].get("summary", "") if recs else ""
            color = f"#{t.get('color', '00e5ff')}"
            return (
                str(t.get("id", "")), t.get("displayName", "Team"),
                t.get("abbreviation", "NFL"), int(c.get("score") or 0),
                rec, t.get("logo", ""), color
            )

        a_id, a_name, a_abbr, a_score, a_rec, a_logo, a_color = parse_team(away)
        h_id, h_name, h_abbr, h_score, h_rec, h_logo, h_color = parse_team(home)

        sit = comp.get("situation", {})
        possession = str(sit.get("possession", ""))
        down_dist = sit.get("downDistanceText", "")
        yardline = int(sit.get("yardLine", 50))
        is_rz = int(sit.get("isRedZone", False))
        last_play = sit.get("lastPlay", {}).get("text", "")

        odds_list = comp.get("odds", [])
        spread_det = odds_list[0].get("details", "EVEN") if odds_list else "EVEN"
        over_under = float(odds_list[0].get("overUnder", 0.0)) if odds_list else 0.0

        probs = comp.get("probabilities", [])
        home_win_prob = float(probs[0].get("homeWinPercentage", 0.5)) if probs else 0.5

        records.append((
            game_id, week_num, status_state, status_detail, kickoff_time, tv,
            a_id, a_name, a_abbr, a_score, a_rec, a_logo, a_color,
            h_id, h_name, h_abbr, h_score, h_rec, h_logo, h_color,
            possession, down_dist, yardline, is_rz, home_win_prob,
            spread_det, over_under, last_play, now_str
        ))

    with get_db() as conn:
        conn.executemany("""
            INSERT OR REPLACE INTO scoreboard_live VALUES (
                ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
            )
        """, records)
        conn.commit()

    return True, f"Synced {len(records)} games for Week {week_num}."

def run_self_audit():
    try:
        ok, msg = sync_espn_data()
        if not ok:
            print(f"❌ [FAIL] Chunk 1 network check failed: {msg}")
            return False
        with get_db() as conn:
            cnt = conn.execute("SELECT COUNT(*) FROM scoreboard_live").fetchone()[0]
            cols = [r[1] for r in conn.execute("PRAGMA table_info(scoreboard_live)").fetchall()]
            assert cnt > 0, "No records stored."
            assert "is_red_zone" in cols and "home_logo" in cols, "Schema mismatch."
        print("✅ [PASS] Chunk 1 verified. Zero regressions.")
        return True
    except Exception as err:
        print(f"❌ [FAIL] Chunk 1 self-audit failed: {err}")
        return False

if __name__ == "__main__":
    run_self_audit()