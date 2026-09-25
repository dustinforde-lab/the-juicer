import sqlite3
import datetime

db_path = "action_grid.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Drop and recreate to ensure the table has the full 3-column schema
cursor.execute("DROP TABLE IF EXISTS completed_teams_blacklist;")
cursor.execute("""
    CREATE TABLE completed_teams_blacklist (
        team_symbol TEXT PRIMARY KEY,
        game_status TEXT,
        finalized_at TEXT
    )
""")

# Register Lions (DET) and Bills (BUF) as the finalized test triggers
now = str(datetime.datetime.now())
cursor.execute("INSERT INTO completed_teams_blacklist (team_symbol, game_status, finalized_at) VALUES ('DET', 'FINAL', ?)", (now,))
cursor.execute("INSERT INTO completed_teams_blacklist (team_symbol, game_status, finalized_at) VALUES ('BUF', 'FINAL', ?)", (now,))
conn.commit()

# Verify counts
cursor.execute("SELECT COUNT(*) FROM completed_teams_blacklist;")
blacklist_count = cursor.fetchone()[0]

cursor.execute("SELECT team_symbol, game_status FROM completed_teams_blacklist;")
teams = cursor.fetchall()

conn.close()

print(f"✅ PIPELINE VERIFIED: {blacklist_count} teams blacklisted -> {teams}")
