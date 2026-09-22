import sqlite3
import os
import json
from datetime import datetime, timezone

DB_PATH = os.path.join(os.getcwd(), "action_grid.db")

def run_odds_ingestion():
    print("\n" + "="*55)
    print("📡 THE JUICER: LIVE ODDS API INGESTION")
    print("="*55)
    
    # Placeholder for live API payload (e.g., The Odds API)
    mock_payload = [
        {"player_name": "Patrick Mahomes", "stat_category": "PASS_YDS", "line": 265.5},
        {"player_name": "Bijan Robinson", "stat_category": "RUSH_YDS", "line": 78.5},
        {"player_name": "CeeDee Lamb", "stat_category": "REC_YDS", "line": 88.5},
        {"player_name": "De'Von Achane", "stat_category": "RUSH_YDS", "line": 64.5},
        {"player_name": "Travis Kelce", "stat_category": "REC_YDS", "line": 55.5}
    ]
    
    conn = sqlite3.connect(DB_PATH)
    now_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")
    
    # Archive the raw payload for the Learning Loop
    conn.execute(
        "INSERT INTO raw_slate_articles (title, content, timestamp) VALUES (?, ?, ?)",
        ("ODDS_API_PAYLOAD", json.dumps(mock_payload), now_iso)
    )
    
    # Update player_rankings with live consensus lines
    for item in mock_payload:
        conn.execute(
            "UPDATE player_rankings SET consensus_line = ?, stat_category = ? WHERE player_name = ?",
            (item["line"], item["stat_category"], item["player_name"])
        )
        
    conn.commit()
    conn.close()
    
    print(f"✅ Ingested {len(mock_payload)} live prop lines and updated Master Matrix.")
    print("="*55 + "\n")

if __name__ == "__main__":
    run_odds_ingestion()