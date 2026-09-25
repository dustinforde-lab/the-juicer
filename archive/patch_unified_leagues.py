import sqlite3
import os

DB_PATH = os.path.join(os.getcwd(), "action_grid.db")

def upgrade_unified_schema():
    conn = sqlite3.connect(DB_PATH)
    # Rebuild season_long_rosters to cleanly support multi-league Yahoo + MFL
    conn.execute("DROP TABLE IF EXISTS season_long_rosters")
    conn.execute("""
        CREATE TABLE season_long_rosters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT NOT NULL CHECK(platform IN ('YAHOO', 'MFL')),
            league_id TEXT NOT NULL,
            league_name TEXT NOT NULL,
            team_id TEXT NOT NULL,
            team_name TEXT NOT NULL,
            player_name TEXT NOT NULL,
            pos TEXT,
            status TEXT NOT NULL CHECK(status IN ('ROSTER', 'BENCH', 'IR', 'FREE_AGENT')),
            last_updated TEXT NOT NULL
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_season_rosters_lookup ON season_long_rosters(platform, league_id, team_id)")
    conn.commit()
    conn.close()
    print("✅ Unified schema applied: Multi-league Yahoo & MFL support ready.")

if __name__ == "__main__":
    upgrade_unified_schema()