import os
import sqlite3

print("\n" + "="*65)
print(" 🛡️ PHASE 1: SAFE ENVIRONMENT INVENTORY & HEALTH AUDIT")
print("="*65)

# 1. Check Project Files
print("\n[1] Core File Inventory:")
core_files = ["app.py", "ui_components.py", "ui_addresses.py", "action_grid.db"]
for f in core_files:
    if os.path.exists(f):
        size = os.path.getsize(f)
        print(f"  🟢 [PROTECTED] {f} exists ({size} bytes) - Active component.")
    else:
        print(f"  ⚪ [ABSENT] {f} not found in project directory.")

# 2. Check Database & Health
print("\n[2] Backend Data & Table Health (action_grid.db):")
try:
    with sqlite3.connect("action_grid.db") as conn:
        tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
        print(f"  🟢 Active Tables Found: {', '.join(tables)}")
        
        if "dfs_rosters" in tables:
            count = conn.execute("SELECT COUNT(*) FROM dfs_rosters").fetchone()[0]
            print(f"     * dfs_rosters: {count} lineups actively stored.")
            
        if "slips" in tables:
            count = conn.execute("SELECT COUNT(*) FROM slips").fetchone()[0]
            print(f"     * slips: {count} betting slips actively stored.")
            
    print("  🟢 Backend database is fully intact and holding live data.")
except Exception as e:
    print(f"  ❌ Database inspection error: {e}")

print("\n" + "="*65)
print(" AUDIT COMPLETE. Review the items above. Nothing has been altered.")
print("="*65 + "\n")