import sqlite3
import os
from datetime import datetime

DB_FILE = "action_grid.db"

def run_juice_press_isolated_test():
    print("=" * 65)
    print("🗜️ [PHASE 1 - MOD 6] The Juice Press - Odds & Timestamp Engine")
    print("=" * 65)
    
    if not os.path.exists(DB_FILE):
        print(f"❌ Error: {DB_FILE} not found.")
        return

    try:
        with sqlite3.connect(DB_FILE) as conn:
            cur = conn.cursor()
            
            # Ensure the odds ledger exists for DraftKings/FanDuel tracking
            cur.execute("""
                CREATE TABLE IF NOT EXISTS live_odds_feed (
                    market_id TEXT PRIMARY KEY,
                    sportsbook TEXT,
                    prop_target TEXT,
                    line REAL,
                    odds TEXT,
                    timestamp TEXT
                )
            """)
            
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Inject strictly timestamped odds for DraftKings and FanDuel
            cur.execute(
                "INSERT OR REPLACE INTO live_odds_feed (market_id, sportsbook, prop_target, line, odds, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                ("DK-PHI-01", "DraftKings", "A.J. Brown Rec Yds", 82.5, "-115", current_time)
            )
            cur.execute(
                "INSERT OR REPLACE INTO live_odds_feed (market_id, sportsbook, prop_target, line, odds, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                ("FD-PHI-01", "FanDuel", "A.J. Brown Rec Yds", 85.5, "-110", current_time)
            )
            
            # The Juice Press calculates the edge and logs it to the Film Room
            directive = f"LINE SHOP: DraftKings (82.5 @ -115) beats FanDuel (85.5 @ -110). Timestamp locked: {current_time}."
            
            cur.execute(
                "INSERT INTO agent_chatter (sender, directive, target, action, timestamp) VALUES (?, ?, ?, ?, ?)",
                ("JUICE PRESS", directive, "A.J. Brown", "ODDS_LOCKED", current_time)
            )
            conn.commit()
            
            # Verify the log was written
            log = cur.execute("SELECT sender, action, target, directive FROM agent_chatter WHERE sender = 'JUICE PRESS' ORDER BY message_id DESC LIMIT 1").fetchone()
            
            print("   ✅ The Juice Press successfully stamped DraftKings/FanDuel odds.")
            print(f"   ✅ Telemetry Logged -> [{log[0]}] {log[1]} | {log[2]} | {log[3]}")
            
    except Exception as e:
        print(f"   ❌ Execution Failed: {e}")

    print("=" * 65)

if __name__ == "__main__":
    run_juice_press_isolated_test()
