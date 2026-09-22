import sqlite3
import os
import json
import requests
from datetime import datetime, timezone

DB_PATH = os.path.join(os.getcwd(), "action_grid.db")


def get_secret(name):
    value = os.getenv(name)
    if value:
        return value
    try:
        import streamlit as st
        value = st.secrets.get(name, "")
        if value:
            return value
        return st.secrets.get("api_keys", {}).get(name.lower(), "")
    except Exception:
        return ""

def run_odds_ingestion():
    print("\n" + "="*55)
    print("📡 THE JUICER: LIVE ODDS API INGESTION")
    print("="*55)
    
    api_key = get_secret("ODDS_API_KEY")
    markets = {
        "player_pass_yds": "PASS_YDS",
        "player_rush_yds": "RUSH_YDS",
        "player_reception_yds": "REC_YDS",
        "player_pass_tds": "PASS_TDS",
        "player_rush_tds": "RUSH_TDS",
        "player_reception_tds": "REC_TDS",
    }
    payload = []
    mode = "FALLBACK"
    if api_key:
        try:
            response = requests.get(
                "https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds",
                params={
                    "apiKey": api_key,
                    "regions": "us",
                    "markets": ",".join(markets),
                    "oddsFormat": "american",
                },
                timeout=15,
            )
            response.raise_for_status()
            for event in response.json():
                for bookmaker in event.get("bookmakers", []):
                    for market in bookmaker.get("markets", []):
                        category = markets.get(market.get("key"))
                        if not category:
                            continue
                        for outcome in market.get("outcomes", []):
                            if outcome.get("name") != "Over" or outcome.get("point") is None:
                                continue
                            payload.append({
                                "player_name": outcome.get("description"),
                                "stat_category": category,
                                "line": float(outcome["point"]),
                                "bookmaker": bookmaker.get("title", "Unknown"),
                            })
            mode = "LIVE API" if payload else "FALLBACK"
        except (requests.RequestException, ValueError):
            payload = []

    if not payload:
        payload = [
            {"player_name": "Patrick Mahomes", "stat_category": "PASS_YDS", "line": 265.5},
            {"player_name": "Bijan Robinson", "stat_category": "RUSH_YDS", "line": 78.5},
            {"player_name": "CeeDee Lamb", "stat_category": "REC_YDS", "line": 88.5},
            {"player_name": "De'Von Achane", "stat_category": "RUSH_YDS", "line": 64.5},
            {"player_name": "Travis Kelce", "stat_category": "REC_YDS", "line": 55.5},
        ]
    
    conn = sqlite3.connect(DB_PATH)
    now_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")
    
    # Archive the raw payload for the Learning Loop
    conn.execute(
        "INSERT INTO raw_slate_articles (title, content, timestamp) VALUES (?, ?, ?)",
        ("ODDS_API_PAYLOAD", json.dumps(payload), now_iso)
    )
    
    # Update player_rankings with live consensus lines
    for item in payload:
        conn.execute(
            "UPDATE player_rankings SET consensus_line = ?, stat_category = ? WHERE player_name = ?",
            (item["line"], item["stat_category"], item["player_name"])
        )
        
    conn.commit()
    conn.close()
    
    print(f"✅ Line lookup complete: {len(payload)} lines from {mode}.")
    print("="*55 + "\n")

if __name__ == "__main__":
    run_odds_ingestion()