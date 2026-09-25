import sqlite3
import json
from datetime import datetime

DB_FILE = "action_grid.db"

def resolve_entity(player_name, cursor):
    cursor.execute("SELECT canonical_id, aliases FROM master_players")
    for row in cursor.fetchall():
        canonical_id, aliases_json = row[0], row[1]
        if aliases_json:
            aliases = json.loads(aliases_json)
            if player_name.lower() in [a.lower() for a in aliases]:
                return canonical_id
    return None

def fetch_live_odds():
    # Simulated live feed scraping current lines for tonight's Lions vs Bills matchup
    return [
        {"player": "Jahmyr Gibbs", "book": "DraftKings", "stat": "REC_YDS", "line": 29.5, "over_odds": -114, "under_odds": -106},
        {"player": "J. Gibbs", "book": "bet365", "stat": "REC_YDS", "line": 29.5, "over_odds": -114, "under_odds": -105},
        {"player": "Dalton Kincaid", "book": "Fanatics", "stat": "RECEPTIONS", "line": 4.5, "over_odds": 140, "under_odds": -160},
        {"player": "D. Kincaid", "book": "FanDuel", "stat": "ANYTIME_TD", "line": 0.5, "over_odds": 175, "under_odds": -200},
        {"player": "Amon-Ra St. Brown", "book": "FanDuel", "stat": "ANYTIME_TD", "line": 0.5, "over_odds": 110, "under_odds": -130},
        {"player": "Josh Allen", "book": "DraftKings", "stat": "ANYTIME_TD", "line": 0.5, "over_odds": -135, "under_odds": 110},
        {"player": "Jared Goff", "book": "Caesars", "stat": "PASS_COMP", "line": 23.5, "over_odds": -107, "under_odds": -107},
        {"player": "J. Goff", "book": "DraftKings", "stat": "PASS_COMP", "line": 23.5, "over_odds": 104, "under_odds": -120}
    ]

def ingest_odds():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    live_feed = fetch_live_odds()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    quotes_added = 0
    
    for item in live_feed:
        canonical_id = resolve_entity(item["player"], cursor)
        if canonical_id:
            cursor.execute("""
                INSERT INTO sportsbook_quotes 
                (canonical_id, player_name, sportsbook, stat_category, line, over_odds, under_odds, week, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (canonical_id, item["player"], item["book"], item["stat"], item["line"], 
                  item["over_odds"], item["under_odds"], 2, now))
            quotes_added += 1
            
    conn.commit()
    conn.close()
    
    print("=== CHUNK 2 COMPLETE: ODDS INGESTION LAYER ===")
    print(f"[SCRAPER] Processed {len(live_feed)} raw odds from external books.")
    print(f"[ENTITY RESOLUTION] Successfully normalized {quotes_added} props to canonical master IDs.")

if __name__ == "__main__":
    ingest_odds()
