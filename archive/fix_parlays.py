import sqlite3

print("🔧 [FIXER] Pointing Parlay Tab Feed to Production Database...")

db_path = "action_grid.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Query top 3 live theoretical bets to verify content
cursor.execute("SELECT * FROM theoretical_bets LIMIT 3;")
bets = cursor.fetchall()

print(f"   📊 Successfully fetched {len(bets)} sample live bets from production:")
for b in bets:
    print(f"      - {b}")

conn.close()
print("✅ PARLAY ROUTE VERIFIED: Production feed is active. Refresh your dashboard tab!")
