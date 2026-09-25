import sqlite3
import os
from datetime import datetime, timezone

DB_PATH = os.path.join(os.getcwd(), "action_grid.db")

# MFL API Configuration (Update with your specific League ID)
MFL_YEAR = "2026"
LEAGUE_ID = "12345"  # Replace with your 5-digit MFL League ID

def run_mfl_sync():
    print("\n" + "="*55)
    print("🏈 THE JUICER: MYFANTASYLEAGUE.COM SYNC")
    print("="*55)
    
    # Mocking the MFL JSON response for the Straight Cash franchise
    # In production, use: url = f"https://www46.myfantasyleague.com/{MFL_YEAR}/export?TYPE=rosters&L={LEAGUE_ID}&JSON=1"
    mock_mfl_data = [
        {"franchise": "Straight Cash", "player_name": "Lamar Jackson", "pos": "QB", "status": "ROSTER"},
        {"franchise": "Straight Cash", "player_name": "Bijan Robinson", "pos": "RB", "status": "ROSTER"},
        {"franchise": "Straight Cash", "player_name": "CeeDee Lamb", "pos": "WR", "status": "ROSTER"},
        {"franchise": "Waiver Wire", "player_name": "Kayshon Boutte", "pos": "WR", "status": "FREE_AGENT"},
        {"franchise": "Waiver Wire", "player_name": "Denzel Boston", "pos": "WR", "status": "FREE_AGENT"}
    ]
    
    conn = sqlite3.connect(DB_PATH)
    now_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")
    
    conn.execute("DELETE FROM season_long_rosters")
    
    updates = []
    for item in mock_mfl_data:
        updates.append((
            "0001" if item["franchise"] == "Straight Cash" else "0000",
            item["franchise"],
            item["player_name"],
            item["pos"],
            item["status"],
            now_iso
        ))
        
    conn.executemany("""
        INSERT INTO season_long_rosters (franchise_id, franchise_name, player_name, pos, status, last_updated)
        VALUES (?, ?, ?, ?, ?, ?)
    """, updates)
    
    conn.commit()
    conn.close()
    
    print(f"✅ Successfully synced {len(mock_mfl_data)} players from MFL.")
    print("="*55 + "\n")

if __name__ == "__main__":
    run_mfl_sync()