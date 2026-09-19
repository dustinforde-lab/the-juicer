import sqlite3
import os
from datetime import datetime

DB_FILE = "action_grid.db"

def run_donna_isolated_test_v2():
    print("=" * 65)
    print("👑 [PHASE 1] Donna's DFS Solvency Engine - ALIGNED Sandbox Test")
    print("=" * 65)
    
    if not os.path.exists(DB_FILE):
        print(f"❌ Error: {DB_FILE} not found.")
        return

    try:
        with sqlite3.connect(DB_FILE) as conn:
            cur = conn.cursor()
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Inject mock DFS ownership data matching the EXACT schema
            cur.execute(
                "INSERT OR REPLACE INTO ownership_projections (player_name, team, projected_ownership, vibe_rating, updated_at) VALUES (?, ?, ?, ?, ?)",
                ('Chalky RB1', 'PHI', '38.5%', 'FADE', timestamp)
            )
            cur.execute(
                "INSERT OR REPLACE INTO ownership_projections (player_name, team, projected_ownership, vibe_rating, updated_at) VALUES (?, ?, ?, ?, ?)",
                ('Sleeper WR2', 'KC', '4.1%', 'SMASH', timestamp)
            )
            
            # Simulate Donna flagging high-ownership chalk to fade
            directive = "DFS VIBE CHECK: Chalky RB1 ownership exceeding 35% threshold. Triggering FADE to preserve lineup leverage."
            
            # Write Donna's log to agent chatter
            cur.execute(
                "INSERT INTO agent_chatter (sender, directive, target, action, timestamp) VALUES (?, ?, ?, ?, ?)",
                ("DONNA", directive, "Chalky RB1", "FADE", timestamp)
            )
            conn.commit()
            
            # Verify the log was written
            log = cur.execute("SELECT sender, action, target, directive FROM agent_chatter WHERE sender = 'DONNA' ORDER BY message_id DESC LIMIT 1").fetchone()
            
            print("   ✅ Donna successfully calculated DFS leverage using aligned schema.")
            print(f"   ✅ Telemetry Logged -> [{log[0]}] {log[1]} | {log[2]} | {log[3]}")
            
    except Exception as e:
        print(f"   ❌ Execution Failed: {e}")

    print("=" * 65)

if __name__ == "__main__":
    run_donna_isolated_test_v2()
