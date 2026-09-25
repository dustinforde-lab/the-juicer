import sqlite3
import os

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "action_grid.db")
with sqlite3.connect(db_path) as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS placed_bets_ledger (
            ticket_id TEXT PRIMARY KEY,
            source_tab TEXT,
            platform TEXT,
            ticket_type TEXT,
            legs_json TEXT,
            placed_odds TEXT,
            fair_prob REAL,
            stake_units REAL DEFAULT 1.0,
            placed_timestamp TEXT,
            closing_odds TEXT DEFAULT NULL,
            clv_alpha REAL DEFAULT NULL,
            status TEXT DEFAULT 'PENDING',
            settled_result TEXT DEFAULT NULL,
            settled_timestamp TEXT DEFAULT NULL
        )
    """)
    conn.commit()
print("✅ Database verified: placed_bets_ledger schema active.")
