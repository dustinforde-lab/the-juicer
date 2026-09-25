import sqlite3
import os

DB_FILE = "action_grid.db"

print("=" * 65)
print("🔍 Checking existing database schema for theoretical_bets...")
print("=" * 65)

if not os.path.exists(DB_FILE):
    print("❌ Error: action_grid.db not found.")
else:
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        columns = cur.execute("PRAGMA table_info(theoretical_bets)").fetchall()
        
        if columns:
            print("   ✅ Table found. Columns are:")
            for col in columns:
                print(f"      - {col[1]} ({col[2]})")
        else:
            print("   ⚠️ Table exists but has no columns, or table does not exist.")
            
print("=" * 65)
