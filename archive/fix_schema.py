import sqlite3

db_path = "action_grid.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Inspect actual columns in theoretical_bets
cursor.execute("PRAGMA table_info(theoretical_bets);")
cols = [col[1] for col in cursor.fetchall()]
print(f"📋 Actual columns in `theoretical_bets`: {cols}")

# 2. Check the distinct weight classes (tiers)
if "weight_class" in cols:
    cursor.execute("SELECT DISTINCT weight_class FROM theoretical_bets;")
    tiers = cursor.fetchall()
    print(f"🎯 Active Tiers found: {tiers}")

conn.close()
print("✅ SCHEMA INSPECTED: Ready to update UI queries.")
