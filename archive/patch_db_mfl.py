import sqlite3
import os

DB_PATH = os.path.join(os.getcwd(), "action_grid.db")

def upgrade_schema_mfl():
    print("\n" + "="*55)
    print("🗄️ THE JUICER: SCHEMA UPGRADE (MFL SYNC)")
    print("="*55)
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS season_long_rosters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            franchise_id TEXT,
            franchise_name TEXT,
            player_name TEXT,
            pos TEXT,
            status TEXT,
            last_updated TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("✅ Schema upgrade for season-long rosters complete.\n")

if __name__ == "__main__":
    upgrade_schema_mfl()