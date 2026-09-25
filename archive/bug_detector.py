import sqlite3, json, os

print("\n" + "="*65)
print(" 🔍 DEEP DIAGNOSTIC & DATA INTEGRITY INSPECTOR")
print("="*65)

# 1. Inspect Database Schema and Raw Rows
try:
    with sqlite3.connect("action_grid.db") as conn:
        print("\n[1] Inspecting 'dfs_rosters' columns & sample data:")
        dfs_sample = conn.execute("SELECT * FROM dfs_rosters LIMIT 1").fetchone()
        dfs_cols = [description[0] for description in conn.execute("SELECT * FROM dfs_rosters").description]
        print(f"  Columns: {dfs_cols}")
        print(f"  Sample Row: {dfs_sample}")

        print("\n[2] Inspecting 'slips' columns & sample legs_json:")
        slip_sample = conn.execute("SELECT platform, leg_count, legs_json FROM slips LIMIT 3").fetchall()
        for s in slip_sample:
            print(f"  Platform: {s[0]} | Legs: {s[1]} | Raw JSON: {s[2]}")

except Exception as e:
    print(f"  ❌ DB Inspection Error: {e}")

# 2. Check for syntax errors in UI files
print("\n[3] Compiling Python files to check for syntax bugs:")
for script in ["app.py", "ui_components.py", "ui_addresses.py"]:
    if os.path.exists(script):
        try:
            with open(script, "r", encoding="utf-8") as f:
                compile(f.read(), script, 'exec')
            print(f"  🟢 {script} -> Syntax OK")
        except Exception as e:
            print(f"  ❌ SYNTAX ERROR in {script}: {e}")
    else:
        print(f"  ⚪ {script} not found.")

print("\n" + "="*65)
print(" DIAGNOSTIC COMPLETE.")
print("="*65 + "\n")