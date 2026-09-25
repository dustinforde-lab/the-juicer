"""
The Juicer - Dynamic Quota Budgeter & Prop Steam Engine
Max-efficiency utilization targeting ~490 calls/month with a 10-call safety floor.
Tracks line changes, juice deltas, and sharp steam.
"""
import os
import sys
import requests
import sqlite3
import calendar
from datetime import datetime, date

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "action_grid.db")

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=10000;")
    conn.row_factory = sqlite3.Row
    return conn

def resolve_odds_api_key():
    toml_paths = [
        os.path.join(os.path.dirname(__file__), ".streamlit", "secrets.toml"),
        os.path.join(os.path.dirname(__file__), "secrets.toml"),
        os.path.expanduser("~/.streamlit/secrets.toml")
    ]
    for tp in toml_paths:
        if os.path.exists(tp):
            try:
                with open(tp, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("#") or not line:
                            continue
                        if any(term in line.upper() for term in ["ODDS", "API_KEY"]):
                            if "=" in line:
                                return line.split("=", 1)[1].strip().strip("\"'")
            except Exception:
                pass
    return os.environ.get("ODDS_API_KEY")

def calculate_daily_call_allowance(remaining_calls=495):
    """Dynamically calculates calls allowed today based on remaining calendar days."""
    today = date.today()
    _, last_day = calendar.monthrange(today.year, today.month)
    days_left = max(1, (last_day - today.day) + 1)
    
    # Safe reserve of 10 calls strictly untouched
    usable_pool = max(0, remaining_calls - 10)
    baseline_per_day = usable_pool / days_left

    # Check if games are scheduled today in scoreboard_live
    today_games = 0
    with get_db() as conn:
        try:
            today_str = today.strftime("%Y-%m-%d")
            row = conn.execute("SELECT COUNT(*) FROM scoreboard_live WHERE kickoff_time LIKE ?", (f"%{today_str}%",)).fetchone()
            if row:
                today_games = row[0]
        except Exception:
            pass

    # If gameday (Thursday, Sunday, Monday, or Holiday), allocate 2.5x weight
    if today_games > 0:
        budget_today = int(baseline_per_day * 1.8)
    else:
        budget_today = int(baseline_per_day * 0.7)

    return max(2, min(budget_today, usable_pool)), days_left, today_games

def record_prop_tick(conn, player_name, team, opp, game_id, stat_type, line_val, over_odds, under_odds, source):
    prop_id = f"{player_name}_{stat_type}_{source}".replace(" ", "_").upper()
    
    # Check prior line to detect line movement / steam
    prev = conn.execute("SELECT line_value, over_odds FROM market_player_props WHERE prop_id=?", (prop_id,)).fetchone()
    
    # Update latest snapshot
    conn.execute("""
        INSERT INTO market_player_props (prop_id, player_name, team, opp, game_id, stat_type, line_value, over_odds, under_odds, source, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(prop_id) DO UPDATE SET
            line_value=excluded.line_value,
            over_odds=excluded.over_odds,
            under_odds=excluded.under_odds,
            updated_at=CURRENT_TIMESTAMP
    """, (prop_id, player_name, team, opp, game_id, stat_type, line_val, over_odds, under_odds, source))

    # Log tick in history
    conn.execute("""
        INSERT INTO market_props_history (player_name, stat_type, line_value, over_odds, under_odds, source)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (player_name, stat_type, line_val, over_odds, under_odds, source))

    if prev:
        delta_line = round(line_val - prev["line_value"], 2)
        if abs(delta_line) >= 1.5:
            direction = "📈 STEAM OVER" if delta_line > 0 else "📉 STEAM UNDER"
            print(f"  [{direction}] {player_name} ({stat_type}): {prev['line_value']} -> {line_val} ({delta_line:+} yds) via {source}")

def run_self_audit():
    key = resolve_odds_api_key()
    assert key is not None, "API Key could not be resolved from TOML."
    allowance, days_left, games_today = calculate_daily_call_allowance(497)
    print(f"✅ [PASS] Dynamic Quota Engine: {days_left} days left in month. Today's Budget: {allowance} calls (Gameday active: {games_today > 0}).")
    return True

if __name__ == "__main__":
    run_self_audit()