import sqlite3

db_path = "action_grid.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Ensure mock player pool table exists for testing
cursor.execute("CREATE TABLE IF NOT EXISTS player_pool (player_name TEXT, team TEXT)")
cursor.execute("DELETE FROM player_pool")
cursor.execute("INSERT INTO player_pool VALUES ('Josh Allen', 'BUF')")
cursor.execute("INSERT INTO player_pool VALUES ('Jared Goff', 'DET')")
cursor.execute("INSERT INTO player_pool VALUES ('Patrick Mahomes', 'KC')")
conn.commit()

# 2. Query used by Mike & Donna incorporating Lewis's blacklist filter
query = """
    SELECT player_name, team FROM player_pool 
    WHERE team NOT IN (SELECT team_symbol FROM completed_teams_blacklist)
"""

try:
    cursor.execute(query)
    active_players = cursor.fetchall()
    print(f"✅ Active players available for Mike & Donna: {active_players}")
    
    # 3. Built-in verification check
    teams_present = [p[1] for p in active_players]
    assert 'BUF' not in teams_present and 'DET' not in teams_present, "Error: Blacklisted team found in active pool!"
    print("🛡️ VERIFIED: Lewis successfully blocked Lions and Bills from Mike & Donna's pool!")
except Exception as e:
    print(f"❌ Filter test failed: {e}")
finally:
    conn.close()
