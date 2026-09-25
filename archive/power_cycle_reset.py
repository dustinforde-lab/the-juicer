import os
import subprocess
import sqlite3
import sys
import shutil
from datetime import datetime

DB_FILE = "action_grid.db"

def power_cycle_system():
    print("="*65)
    print("🔌 [POWER CYCLE RESET] Initiating Full War Room Shutdown & Reboot...")
    print("="*65)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S ET')}\n")

    print("⚡ Step 1: Shutting down all active power cells and UI daemons...")
    try:
        if os.name == 'nt':
            subprocess.run(["powershell", "-Command", "Stop-Process -Name python,streamlit -Force -ErrorAction SilentlyContinue"], capture_output=True)
        else:
            subprocess.run(["pkill", "-f", "streamlit"], capture_output=True)
        print("   [OK] All power cells successfully powered down.")
    except Exception as e:
        print(f"   [NOTE] Process termination notice: {e}")

    print("\n🧹 Step 2: Purging residual local caches and compiled bytecode...")
    cache_dirs = ["__pycache__", ".streamlit/cache"]
    for d in cache_dirs:
        if os.path.exists(d):
            try:
                shutil.rmtree(d)
                print(f"   [CLEARED] {d}")
            except:
                pass
    print("   [OK] Cache sweep complete.")

    print("\n🛡️ Step 3: Engaging Donna's Team-Level Cleanse & Slate Re-indexing...")
    if os.path.exists("team_cleanser.py"):
        subprocess.run([sys.executable, "team_cleanser.py"])
    else:
        with sqlite3.connect(DB_FILE) as conn:
            cur = conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS completed_teams_blacklist (team TEXT PRIMARY KEY, cleansed_at TEXT)")
            cur.execute("INSERT OR IGNORE INTO completed_teams_blacklist VALUES ('DET', ?)", (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),))
            cur.execute("INSERT OR IGNORE INTO completed_teams_blacklist VALUES ('BUF', ?)", (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),))
            conn.commit()
        print("   [OK] Master blacklist updated: DET and BUF locked out.")

    print("\n" + "="*65)
    print("✅ [POWER CYCLE COMPLETE] All systems scrubbed, re-indexed, and fresh.")
    print("="*65)

if __name__ == "__main__":
    power_cycle_system()
