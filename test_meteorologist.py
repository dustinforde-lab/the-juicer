import sqlite3
import os
from datetime import datetime

DB_FILE = "action_grid.db"

def run_meteorologist_isolated_test():
    print("=" * 65)
    print("🌩️ [PHASE 1] The Meteorologist - Isolated Sandbox Test")
    print("=" * 65)
    
    if not os.path.exists(DB_FILE):
        print(f"❌ Error: {DB_FILE} not found.")
        return

    try:
        with sqlite3.connect(DB_FILE) as conn:
            cur = conn.cursor()
            
            # Simulate fetching adverse weather for a specific game slate
            target_game = "BUF vs MIA"
            weather_condition = "20mph Sustained Winds + Sleet"
            directive = f"WEATHER SHOCK: {weather_condition}. Downgrading passing correlation 15%, upgrading rushing volume."
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Write the weather shock log to agent chatter
            cur.execute(
                "INSERT INTO agent_chatter (sender, directive, target, action, timestamp) VALUES (?, ?, ?, ?, ?)",
                ("METEOROLOGIST", directive, target_game, "ADJUST", timestamp)
            )
            conn.commit()
            
            # Verify the log was written
            log = cur.execute("SELECT sender, action, target, directive FROM agent_chatter WHERE sender = 'METEOROLOGIST' ORDER BY message_id DESC LIMIT 1").fetchone()
            
            print("   ✅ The Meteorologist successfully evaluated stadium conditions.")
            print(f"   ✅ Telemetry Logged -> [{log[0]}] {log[1]} | {log[2]} | {log[3]}")
            
    except Exception as e:
        print(f"   ❌ Execution Failed: {e}")

    print("=" * 65)

if __name__ == "__main__":
    run_meteorologist_isolated_test()
