import sqlite3

print("🧹 [PURGE] Cleaning sandbox artifacts from production `theoretical_bets`...")
db_path = "action_grid.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Count before purge
cursor.execute("SELECT COUNT(*) FROM theoretical_bets;")
before_count = cursor.fetchone()[0]

# Remove sandbox tickets and placeholder staged players
cursor.execute("DELETE FROM theoretical_bets WHERE ticket_id LIKE 'SBOX%' OR ticket_json LIKE '%Staged Player%';")
conn.commit()

# Count after purge
cursor.execute("SELECT COUNT(*) FROM theoretical_bets;")
after_count = cursor.fetchone()[0]

print(f"   📊 Removed {before_count - after_count} sandbox artifacts.")
print(f"   ✨ Cleaned production table now holds {after_count} verified live betting slips.")

conn.close()
print("✅ PARLAY CLEANUP COMPLETE: Refresh your Streamlit dashboard tab to see the live props!")
