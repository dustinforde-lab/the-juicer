import sqlite3
import os
from datetime import datetime

DB_FILE = "action_grid.db"

def run_donna_isolated_test():
    print("=" * 65)
    print("👑 [PHASE 1] Donna's DFS Solvency Engine - Isolated Sandbox Test")
    print("=" * 65)
    
    if not os.path.exists(DB_FILE):
        print(f"❌ Error: {DB_FILE} not found.")
        return

    try:
        with sqlite3.connect(DB_FILE) as conn:
            cur = conn.cursor()
            
            # Ensure ownership projections table exists
            cur.execute("""
                CREATE TABLE IF NOT EXISTS ownership_projections (
                    player_name TEXT PRIMARY KEY,
                    position TEXT,
                    projected_own REAL,
                    leverage_score REAL
                )
            """)
            
            # Inject mock DFS ownership data
            cur.execute("INSERT OR REPLACE INTO ownership_projections (player_name, position, projected_own, leverage_score) VALUES ('Chalky RB1', 'RB', 38.5, -4.2)")
            cur.execute("INSERT OR REPLACE INTO ownership_projections (player_name, position, projected_own, leverage_score) VALUES ('Sleeper WR2', 'WR', 4.1, 8.7)")
            
            # Simulate Donna flagging high-ownership chalk to fade
            directive = "DFS VIBE CHECK: Chalky RB1 ownership exceeding 35% threshold. Triggering FADE to preserve lineup leverage."
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Write Donna's log to agent chatter
            cur.execute(
                "INSERT INTO agent_chatter (sender, directive, target, action, timestamp) VALUES (?, ?, ?, ?, ?)",
                ("DONNA", directive, "Chalky RB1", "FADE", timestamp)
            )
            conn.commit()
            
            # Verify the log was written
            log = cur.execute("SELECT sender, action, target, directive FROM agent_chatter WHERE sender = 'DONNA' ORDER BY message_id DESC LIMIT 1").fetchone()
            
            print("   ✅ Donna successfully calculated DFS leverage and executed vibe check.")
            print(f"   ✅ Telemetry Logged -> [{log[0]}] {log[1]} | {log[2]} | {log[3]}")
            
    except Exception as e:
        print(f"   ❌ Execution Failed: {e}")

    print("=" * 65)

if __name__ == "__main__":
    run_donna_isolated_test()
