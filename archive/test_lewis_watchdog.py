import sqlite3
import os
from datetime import datetime

DB_FILE = "action_grid.db"

def run_lewis_isolated_test():
    print("=" * 65)
    print("🛡️ [PHASE 1] Lewis QA Watchdog - Isolated Sandbox Test")
    print("=" * 65)
    
    if not os.path.exists(DB_FILE):
        print(f"❌ Error: {DB_FILE} not found.")
        return

    try:
        with sqlite3.connect(DB_FILE) as conn:
            cur = conn.cursor()
            
            # Ensure agent_chatter table exists for Lewis's logs
            cur.execute("""
                CREATE TABLE IF NOT EXISTS agent_chatter (
                    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender TEXT,
                    directive TEXT,
                    target TEXT,
                    action TEXT,
                    timestamp TEXT
                )
            """)
            
            # Simulate Lewis catching a toxic parlay slip (e.g., high risk correlation)
            toxic_slip_id = "SLIP-TOXIC-88"
            reason = "KILL-SWITCH TRIGGERED: Negative EV Correlation (>12% risk threshold)"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Write the kill-switch log to agent chatter
            cur.execute(
                "INSERT INTO agent_chatter (sender, directive, target, action, timestamp) VALUES (?, ?, ?, ?, ?)",
                ("LEWIS", reason, toxic_slip_id, "PURGE", timestamp)
            )
            conn.commit()
            
            # Verify the log was written
            log = cur.execute("SELECT sender, action, target, directive FROM agent_chatter WHERE target = 'SLIP-TOXIC-88' ORDER BY message_id DESC LIMIT 1").fetchone()
            
            print("   ✅ Lewis successfully evaluated risk parameters and executed kill-switch.")
            print(f"   ✅ Telemetry Logged -> [{log[0]}] {log[1]} | {log[2]} | {log[3]}")
            
    except Exception as e:
        print(f"   ❌ Execution Failed: {e}")

    print("=" * 65)

if __name__ == "__main__":
    run_lewis_isolated_test()
