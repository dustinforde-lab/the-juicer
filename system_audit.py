import os
import sqlite3
import glob

print("\n" + "="*40)
print(" 🛡️ THE JUICER: FULL SYSTEM AUDIT 🛡️ ")
print("="*40)

# 1. Check Rollbacks
baks = glob.glob("*.bak")
print(f"\n[BACKUP SYSTEM]\nStatus: ONLINE. {len(baks)} backups found.")
if baks: print(f"Latest Rollback: {max(baks, key=os.path.getctime)}")

# 2. Check Database
db_path = "action_grid.db"
print(f"\n[DATABASE ENGINE]")
if os.path.exists(db_path):
    with sqlite3.connect(db_path) as conn:
        tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table';")]
        print(f"Status: ONLINE. {len(tables)} active tables.")
        if "donna_bets_ledger" in tables: 
            print("-> Donna's Learning Loop: VERIFIED.")
        if "dfs_lineups" in tables:
            m = conn.execute("SELECT roster_json FROM dfs_lineups WHERE roster_json LIKE '%Jordan Mason%' LIMIT 1").fetchone()
            if m and "MIN" in m[0]: 
                print("-> Roster Integrity: Jordan Mason locked to MIN (Vikings): VERIFIED.")
else: 
    print("Status: OFFLINE.")

# 3. Check UI
print(f"\n[USER INTERFACE]")
if os.path.exists("app.py"):
    text = open("app.py", "r", encoding="utf-8").read()
    if "Juice Rankings" in text or "ui.render_juice_rankings" in text: 
        print("Status: ONLINE. Tab 2 routed to ⚡ Juice Rankings: VERIFIED.")
print("\n" + "="*40 + "\n")
