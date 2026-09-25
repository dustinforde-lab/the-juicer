"""
The Juicer - Donna Performance Ledger & Autonomous Control Schema
Tracks all simulated bets (DFS, Parlays, Pick'ems) and stages learning loop recommendations.
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

def init_donna_schema():
    with get_db() as conn:
        # 1. Bet Tracker: DFS, Parlays, PrizePicks/Underdog Slips
        conn.execute("""
            CREATE TABLE IF NOT EXISTS donna_bets_ledger (
                bet_id TEXT PRIMARY KEY,
                week_num INTEGER,
                category TEXT, -- 'DFS_CLASSIC_GPP', 'DFS_SHOWDOWN', 'PARLAY', 'PRIZEPICKS'
                wager_units REAL DEFAULT 1.0,
                projected_ev REAL,
                status TEXT DEFAULT 'PENDING', -- 'PENDING', 'WIN', 'LOSS', 'PUSH'
                payout_units REAL DEFAULT 0.0,
                selection_json TEXT,
                locked_at TIMESTAMP,
                settled_at TIMESTAMP
            )
        """)

        # 2. Learning Loop Proposed Multipliers (The God Mode Stage)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS donna_learning_proposals (
                proposal_id INTEGER PRIMARY KEY AUTOINCREMENT,
                week_num INTEGER,
                category TEXT,
                target_variable TEXT,  -- e.g. 'yardage_scalar', 'dome_wr_boost'
                current_value REAL,
                proposed_value REAL,
                rationale TEXT,
                status TEXT DEFAULT 'PENDING_APPROVAL', -- 'PENDING_APPROVAL', 'APPROVED', 'REJECTED'
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 3. Donna's Weekly Narrative Debriefs
        conn.execute("""
            CREATE TABLE IF NOT EXISTS donna_weekly_debriefs (
                week_num INTEGER PRIMARY KEY,
                record_summary TEXT, -- e.g. "12-4 DFS, +4.8u Parlays"
                net_units REAL,
                debrief_markdown TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        print("✅ [PASS] Donna Ledger & Learning Loop schema initialized.")

if __name__ == "__main__":
    init_donna_schema()