import os
import sqlite3
import json

print("\n" + "="*65)
print(" 🔍 DEEP-SCANNING WORKSPACE FOR STRAY DATABASES & SEED HOOKS")
print("="*65)

# 1. Locate all database files in the workspace
db_files = []
for root, dirs, files in os.walk("."):
    if ".git" in root or "venv" in root:
        continue
    for file in files:
        if file.endswith(".db"):
            db_path = os.path.join(root, file)
            db_files.append(db_path)

print(f"  📊 Found database files: {db_files}")

# 2. Purge tracers from EVERY found database instance
for db in db_files:
    try:
        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()
            tables = [t[0] for t in cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
            
            if "dfs_rosters" in tables:
                cursor.execute("DELETE FROM dfs_rosters WHERE qb LIKE '%TRACER%' OR qb LIKE '%TEST%' OR projected_score = 1000.0")
            if "slips" in tables:
                cursor.execute("DELETE FROM slips WHERE legs_json LIKE '%TRACER%' OR legs_json LIKE '%TEST%'")
            conn.commit()
            print(f"  🧹 Cleaned all tracer/test records from: {db}")
    except Exception as e:
        print(f"  ⚠️ Could not clean {db}: {e}")

# 3. Scan app.py for startup seeding loops that re-add tracers
app_path = "app.py"
if os.path.exists(app_path):
    with open(app_path, "r", encoding="utf-8") as f:
        app_code = f.read()
    if "1000.0" in app_code or "TRACER" in app_code:
        print("  ⚠️ Found hardcoded seed or tracer references inside app.py!")
    else:
        print("  🟢 app.py checked: No hardcoded tracer seeds detected in main router.")

print("\n" + "="*65)
print(" ✅ DEEP CLEAN COMPLETE. STARTING STREAMLIT FRESH.")
print("="*65 + "\n")