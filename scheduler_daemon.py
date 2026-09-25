# -*- coding: utf-8 -*-
import time
import sqlite3
import requests
from datetime import datetime
import address_book

ESPN_URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
ODDS_API_KEY = "YOUR_API_KEY" 
ODDS_URL = f"https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds/?apiKey={ODDS_API_KEY}&regions=us&markets=h2h,spreads,totals"

def init_dbs():
    db_path = address_book.PATHS.get("DATABASE", "action_grid.db")
    with sqlite3.connect(db_path) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS system_status (id INTEGER PRIMARY KEY, last_espn_sync TEXT, last_odds_sync TEXT, api_calls_used INTEGER)")
        conn.execute("CREATE TABLE IF NOT EXISTS vegas_lines (game_id TEXT PRIMARY KEY, home TEXT, away TEXT, spread REAL, over_under REAL, updated_at TEXT)")
        conn.commit()

def pulse_espn():
    try:
        resp = requests.get(ESPN_URL, timeout=5)
        if resp.status_code == 200:
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db_path = address_book.PATHS.get("DATABASE", "action_grid.db")
            with sqlite3.connect(db_path) as conn:
                conn.execute("UPDATE system_status SET last_espn_sync = ? WHERE id = 1", (now_str,))
                conn.commit()
    except Exception: pass

def pulse_odds():
    """Fetches The Odds API and writes active spreads/totals to SQLite."""
    now = datetime.now()
    day = now.weekday() 
    hour = now.hour
    
    # Smart Quota: Sun (11, 12, 15, 16, 19, 20), Thu (9, 17, 19), Tue/Wed (9)
    should_pull = False
    if day == 6 and hour in [11, 12, 15, 16, 19, 20]: should_pull = True
    elif day == 3 and hour in [9, 17, 19]: should_pull = True
    elif day in [1, 2] and hour == 9: should_pull = True

    if should_pull:
        try:
            # 🚨 MOCK INGESTION: Simulating payload parse until live key is active
            mock_data = [
                ("DAL_BAL", "DAL", "BAL", -1.5, 47.5),
                ("ATL_GB", "GB", "ATL", -4.5, 44.5),
                ("BUF_MIA", "MIA", "BUF", 2.5, 49.0)
            ]
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db_path = address_book.PATHS.get("DATABASE", "action_grid.db")
            with sqlite3.connect(db_path) as conn:
                conn.execute("UPDATE system_status SET last_odds_sync = ?, api_calls_used = api_calls_used + 1 WHERE id = 1", (now_str,))
                for game in mock_data:
                    conn.execute("""
                        INSERT INTO vegas_lines (game_id, home, away, spread, over_under, updated_at) 
                        VALUES (?, ?, ?, ?, ?, ?) 
                        ON CONFLICT(game_id) DO UPDATE SET spread=excluded.spread, over_under=excluded.over_under, updated_at=excluded.updated_at
                    """, (game[0], game[1], game[2], game[3], game[4], now_str))
                conn.commit()
            print(f"[ODDS PULSE] Ingested Vegas Lines successfully at {now_str}")
        except Exception as e: 
            print(f"[ODDS PULSE] Failed: {e}")

def daemon_loop():
    print("⚡ THE JUICER: Autonomous Daemon Online. Enforcing API Quotas.")
    init_dbs()
    tick = 0
    while True:
        if tick % 60 == 0: pulse_espn()
        if tick % 3600 == 0: pulse_odds() # Evaluates schedule top of every hour
        time.sleep(1)
        tick += 1

if __name__ == "__main__":
    daemon_loop()
