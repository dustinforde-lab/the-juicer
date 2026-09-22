import sqlite3
import sys
from datetime import datetime, timezone

def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def _column_exists(conn: sqlite3.Connection, table: str, column: str) -> bool:
    cur = conn.execute(f"PRAGMA table_info({table})")
    return any(row[1] == column for row in cur.fetchall())

def _table_exists(conn: sqlite3.Connection, table: str) -> bool:
    cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
    return cur.fetchone() is not None

def _ensure_wal(conn: sqlite3.Connection) -> None:
    conn.execute("PRAGMA journal_mode=WAL")

def _create_slips_table(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS slips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT NOT NULL CHECK(platform IN ('PRIZEPICKS', 'UNDERDOG', 'SPORTSBOOK_PARLAY')),
            leg_count INTEGER NOT NULL CHECK(leg_count BETWEEN 2 AND 6),
            legs_json TEXT NOT NULL,
            implied_probability REAL,
            confidence_tier TEXT,
            status TEXT NOT NULL DEFAULT 'PENDING' CHECK(status IN ('PENDING', 'GRADED', 'EXPIRED')),
            legs_hit INTEGER,
            created_at TEXT NOT NULL,
            graded_at TEXT
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_slips_platform_status ON slips(platform, status)")

def _create_bet_grading_table(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS bet_grading (
            grading_id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL CHECK(source IN ('DFS', 'PARLAY', 'PICKEM')),
            reference_id INTEGER NOT NULL,
            player_name TEXT,
            stat_category TEXT,
            predicted_value REAL,
            actual_value REAL,
            hit_flag INTEGER CHECK(hit_flag IN (0, 1)),
            leg_count INTEGER,
            legs_hit INTEGER,
            week INTEGER,
            created_at TEXT NOT NULL,
            graded_at TEXT
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_bet_grading_source ON bet_grading(source, week)")

def _add_dfs_grading_columns(conn: sqlite3.Connection) -> None:
    if not _table_exists(conn, "dfs_classic_lineups"):
        return
    if not _column_exists(conn, "dfs_classic_lineups", "actual_pts"):
        conn.execute("ALTER TABLE dfs_classic_lineups ADD COLUMN actual_pts REAL")
    if not _column_exists(conn, "dfs_classic_lineups", "graded_at"):
        conn.execute("ALTER TABLE dfs_classic_lineups ADD COLUMN graded_at TEXT")

def run_migration(conn: sqlite3.Connection) -> None:
    _ensure_wal(conn)
    _create_slips_table(conn)
    _create_bet_grading_table(conn)
    _add_dfs_grading_columns(conn)
    conn.commit()

if __name__ == "__main__":
    db_path = "action_grid.db" if len(sys.argv) < 2 else sys.argv[1]
    conn = sqlite3.connect(db_path)
    try:
        run_migration(conn)
        print(f"✅ Migration successfully applied to {db_path} with WAL mode enabled.")
    finally:
        conn.close()