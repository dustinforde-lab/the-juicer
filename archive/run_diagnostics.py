import os
import sys
import sqlite3
import importlib

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DB_FILE = "action_grid.db"
CRITICAL_FILES = [
    "app.py", 
    "ui_components.py", 
    "syndicate_orchestrator.py", 
    "juicer_daemon.py",
    "live_medic_poller.py",
    "live_donna_poller.py",
    "upgrade_auto_refill.py",
    "discord_notifier.py",
    "pages/1_🎬_The_Film_Room.py"
]

PACKAGES = ["streamlit", "pandas", "numpy", "matplotlib"]

def run_diagnostics():
    print("=" * 65)
    print("🔧 [SYSTEM DIAGNOSTIC] Initiating Full Mainframe Sweep...")
    print("=" * 65 + "\n")
    
    issues = 0

    # 1. Environment Check
    print("1️⃣ ENVIRONMENT & DEPENDENCIES:")
    print(f"   • Python Version: {sys.version.split()[0]}")
    for pkg in PACKAGES:
        try:
            importlib.import_module(pkg)
            print(f"   ✅ {pkg} installed")
        except ImportError:
            print(f"   ❌ {pkg} is MISSING. (Run: python -m pip install {pkg})")
            issues += 1
    print("")

    # 2. File System Check
    print("2️⃣ CORE ARCHITECTURE:")
    for file in CRITICAL_FILES:
        # Handle the pages directory cross-platform
        filepath = os.path.join(*file.split('/'))
        if os.path.exists(filepath):
            print(f"   ✅ {file} located")
        else:
            print(f"   ❌ {file} is MISSING.")
            issues += 1
    print("")

    # 3. Database Integrity Check
    print("3️⃣ DATABASE & INVENTORY INTEGRITY:")
    if not os.path.exists(DB_FILE):
        print(f"   ❌ {DB_FILE} is MISSING. Run orchestrator to build.")
        issues += 1
    else:
        try:
            with sqlite3.connect(DB_FILE) as conn:
                cur = conn.cursor()
                
                # Check tables
                tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
                required_tables = ["theoretical_bets", "hospital_ward", "agent_chatter", "correlation_weights"]
                for t in required_tables:
                    if t in tables:
                        print(f"   ✅ Table '{t}' verified")
                    else:
                        print(f"   ❌ Table '{t}' is MISSING.")
                        issues += 1
                
                # Check slip count
                if "theoretical_bets" in tables:
                    count = cur.execute("SELECT COUNT(*) FROM theoretical_bets").fetchone()[0]
                    if count == 200:
                        print(f"   ✅ Inventory strictly balanced (200/200 slips)")
                    else:
                        print(f"   ⚠️ Inventory imbalance detected: {count}/200 slips.")
                        issues += 1
                        
        except Exception as e:
            print(f"   ❌ Database corrupted or locked: {e}")
            issues += 1

    print("\n" + "=" * 65)
    if issues == 0:
        print("🟢 ALL SYSTEMS NOMINAL: The Juicer is fully operational.")
    else:
        print(f"🔴 DIAGNOSTIC FAILED: Detected {issues} critical issue(s) in the pipeline.")
    print("=" * 65)

if __name__ == "__main__":
    run_diagnostics()
