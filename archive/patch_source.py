import sqlite3

db_path = "action_grid.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check existing columns in theoretical_bets
cursor.execute("PRAGMA table_info(theoretical_bets);")
cols = [col[1] for col in cursor.fetchall()]

# Add 'source' column if missing
if "source" not in cols:
    print("🔧 Adding missing 'source' column to `theoretical_bets`...")
    cursor.execute("ALTER TABLE theoretical_bets ADD COLUMN source TEXT DEFAULT 'DraftKings';")
    conn.commit()

# Ensure all rows have a valid source for the matrix filters
cursor.execute("UPDATE theoretical_bets SET source = 'DraftKings' WHERE source IS NULL OR source = '';")
conn.commit()

cursor.execute("SELECT COUNT(*) FROM theoretical_bets;")
count = cursor.fetchone()[0]
conn.close()

print(f"✅ PATCH COMPLETE: Added 'source' column. {count} live slips ready for the Parlay Matrix UI!")
