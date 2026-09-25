import sqlite3
import os
import json
from datetime import datetime

DB_FILE = "action_grid.db"

def run_recipe_book_isolated_test():
    print("=" * 65)
    print("📖 [PHASE 1 - MOD 7] The Recipe Book - Correlation Engine")
    print("=" * 65)
    
    if not os.path.exists(DB_FILE):
        print(f"❌ Error: {DB_FILE} not found.")
        return

    try:
        with sqlite3.connect(DB_FILE) as conn:
            cur = conn.cursor()
            
            # Ensure the table exists to hold our built correlation tickets
            cur.execute("""
                CREATE TABLE IF NOT EXISTS theoretical_bets (
                    ticket_id TEXT PRIMARY KEY,
                    weight_class TEXT,
                    odds TEXT,
                    color TEXT,
                    ticket_json TEXT,
                    sportsbook TEXT,
                    timestamp TEXT
                )
            """)
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Simulate The Recipe Book building a high-correlation Eagles stack
            legs = [
                {"player": "Jalen Hurts", "team": "PHI", "stat": "245.5 Pass Yards", "odds": "-115"},
                {"player": "A.J. Brown", "team": "PHI", "stat": "82.5 Rec Yds", "odds": "-115"}
            ]
            
            ticket_json = json.dumps(legs)
            ticket_id = "DK-STACK-PHI-01"
            
            # Insert the built parlay into the database
            cur.execute(
                "INSERT OR REPLACE INTO theoretical_bets (ticket_id, weight_class, odds, color, ticket_json, sportsbook, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (ticket_id, "2-LEG CORRELATION", "+260", "#00ff88", ticket_json, "DraftKings", timestamp)
            )
            
            # Broadcast the stack creation to the Film Room telemetry
            directive = f"CORRELATION BUILT: Jalen Hurts + A.J. Brown Stack. Locked +260 on DraftKings at {timestamp}."
            
            cur.execute(
                "INSERT INTO agent_chatter (sender, directive, target, action, timestamp) VALUES (?, ?, ?, ?, ?)",
                ("RECIPE BOOK", directive, "PHI Stack", "STACK_BUILT", timestamp)
            )
            conn.commit()
            
            # Verify the log was written
            log = cur.execute("SELECT sender, action, target, directive FROM agent_chatter WHERE sender = 'RECIPE BOOK' ORDER BY message_id DESC LIMIT 1").fetchone()
            
            print("   ✅ The Recipe Book successfully built a +EV correlated stack.")
            print(f"   ✅ Telemetry Logged -> [{log[0]}] {log[1]} | {log[2]} | {log[3]}")
            
    except Exception as e:
        print(f"   ❌ Execution Failed: {e}")

    print("=" * 65)

if __name__ == "__main__":
    run_recipe_book_isolated_test()
