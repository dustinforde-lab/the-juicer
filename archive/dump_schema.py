import sqlite3

conn = sqlite3.connect("action_grid.db")
cursor = conn.cursor()

for table in ("dfs_rosters", "slips", "player_rankings", "agent_chatter"):
    print("\n" + "="*20 + f" {table} " + "="*20)
    cursor.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (table,)
    )
    row = cursor.fetchone()
    print(row[0] if row else "(table not found)")

conn.close()