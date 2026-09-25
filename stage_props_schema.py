"""
The Juicer - Market Player Props & Steam Tracking Schema
Stores current consensus lines and historical ticks to capture line drift and sharp movement.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "action_grid.db")

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=10000;")
    conn.row_factory = sqlite3.Row
    return conn

def init_props_schema():
    with get_db() as conn:
        # Table 1: Latest snapshot for fast consensus math
        conn.execute("""
            CREATE TABLE IF NOT EXISTS market_player_props (
                prop_id TEXT PRIMARY KEY,
                player_name TEXT,
                team TEXT,
                opp TEXT,
                game_id TEXT,
                stat_type TEXT,
                line_value REAL,
                over_odds INTEGER,
                under_odds INTEGER,
                source TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Table 2: Historical ticks to track line movement and steam
        conn.execute("""
            CREATE TABLE IF NOT EXISTS market_props_history (
                tick_id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT,
                stat_type TEXT,
                line_value REAL,
                over_odds INTEGER,
                under_odds INTEGER,
                source TEXT,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Indexes for fast lookup by Mike
        conn.execute("CREATE INDEX IF NOT EXISTS idx_props_player ON market_player_props(player_name, stat_type)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_hist_player ON market_props_history(player_name, stat_type, recorded_at)")
        conn.commit()
        print("✅ [PASS] market_player_props & history tables successfully initialized.")

if __name__ == "__main__":
    init_props_schema()