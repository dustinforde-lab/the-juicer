import urllib.request
import json
import sqlite3
import sys
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DB_FILE = "action_grid.db"
# Source: Real RotoGrinders NFL ownership feed
DFS_ENDPOINT = "https://roto-static.com/public/sports-feeder/nfl/projected-ownership/json/nfl-projected-ownership.json"

def perform_live_vibe_check():
    print("=" * 65)
    print("📉 [PHASE 4: STEP 1] Executing Live DFS Vibe Check (Donna's Poller)...")
    print("=" * 65)
    
    now_ts = datetime.now().strftime("%Y-%m-%d %I:%M %p ET")
    processed_ownership = []
    chatter_msgs = []
    
    # Roster limit for testing. Can be increased to 100+ later.
    PROCESSING_LIMIT = 20

    try:
        req = urllib.request.Request(
            DFS_ENDPOINT, 
            headers={"User-Agent": "Mozilla/5.0 (Juicer Syndicator)"}
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            if response.status == 200:
                raw_data = json.loads(response.read().decode("utf-8"))
                players_list = raw_data.get("rows", [])
                
                print(f"   [CONNECTED] Recieved {len(players_list)} NFL player projections.")
                
                # Analyze the top owned players
                count = 0
                for p in players_list:
                    if count >= PROCESSING_LIMIT: break
                    
                    p_name = p.get("name", "Unknown")
                    team = p.get("team", "")
                    own_pct = float(p.get("ownership", 0.0))
                    
                    if own_pct == 0: continue
                    
                    # Define the Vibe based on numerical thresholds
                    vibe = "MEGA CHALK" if own_pct >= 25 else ("HEAVY CHALK" if own_pct >= 18 else ("CHALK" if own_pct >= 12 else ("CONTRARIAN" if own_pct >= 6 else "LEVERAGE PLAY")))
                    
                    processed_ownership.append((p_name, team, f"{own_pct:.1f}%", vibe, now_ts))
                    
                    # Log critical warnings for the Main War Room UI Ticker (8501)
                    if vibe in ["MEGA CHALK", "HEAVY CHALK"]:
                        chatter_msgs.append(("Donna (DFS)", f"OWNERSHIP WARNING: {own_pct:.1f}%", p_name, "AVOID IN GPP", now_ts))
                    
                    print(f"   • [LIVE OWNERSHIP] {p_name} ({team}) -> {own_pct:.1f}% ({vibe})")
                    count += 1
                    
    except Exception as e:
        print(f"   [OFFLINE] Using last cached Donna projections ({e}).")
        return

    # Update Database
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        
        # Build Vibe Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ownership_projections (
                player_name TEXT PRIMARY KEY,
                team TEXT,
                projected_ownership TEXT,
                vibe_rating TEXT,
                updated_at TEXT
            )
        """)
        
        # Bulk Insert
        if processed_ownership:
            cur.execute("DELETE FROM ownership_projections")
            cur.executemany("INSERT INTO ownership_projections VALUES (?, ?, ?, ?, ?)", processed_ownership)
            
        # Dispatch to the Ticker (8501)
        if chatter_msgs:
            cur.executemany("INSERT INTO agent_chatter (sender, directive, target, action, timestamp) VALUES (?, ?, ?, ?, ?)", chatter_msgs)
            
        conn.commit()
        print(f"   ✅ [SYNC OK] Donna's War Room synced. Live vibe check complete.")

if __name__ == "__main__":
    perform_live_vibe_check()
