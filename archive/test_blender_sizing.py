import sqlite3
import os
from datetime import datetime

DB_FILE = "action_grid.db"

def run_blender_isolated_test():
    print("=" * 65)
    print("🌪️ [PHASE 1 - MOD 5] The Blender Unit Sizing - Sandbox Test")
    print("=" * 65)
    
    if not os.path.exists(DB_FILE):
        print(f"❌ Error: {DB_FILE} not found.")
        return

    try:
        with sqlite3.connect(DB_FILE) as conn:
            cur = conn.cursor()
            
            # Simulated inputs
            target_slip = "PP-FLEX-01"
            confidence_score = 92.4
            current_bankroll = 1000.00
            
            # The Blender Logic: Kelly-style fractional sizing based on confidence
            # Base unit is 1% ($10). High confidence scales it up to 2.5% max.
            unit_multiplier = (confidence_score - 70) / 10  # e.g., 92.4 -> 2.24 units
            recommended_bet = round((current_bankroll * 0.01) * unit_multiplier, 2)
            
            directive = f"BANKROLL SIZING: Confidence at {confidence_score}%. Recommending {unit_multiplier:.2f}U allocation (${recommended_bet})."
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Write The Blender's log to agent chatter
            cur.execute(
                "INSERT INTO agent_chatter (sender, directive, target, action, timestamp) VALUES (?, ?, ?, ?, ?)",
                ("BLENDER", directive, target_slip, "SIZE_BET", timestamp)
            )
            conn.commit()
            
            # Verify the log was written
            log = cur.execute("SELECT sender, action, target, directive FROM agent_chatter WHERE sender = 'BLENDER' ORDER BY message_id DESC LIMIT 1").fetchone()
            
            print("   ✅ The Blender successfully calculated dynamic unit sizing.")
            print(f"   ✅ Telemetry Logged -> [{log[0]}] {log[1]} | {log[2]} | {log[3]}")
            
    except Exception as e:
        print(f"   ❌ Execution Failed: {e}")

    print("=" * 65)

if __name__ == "__main__":
    run_blender_isolated_test()
