import sqlite3
import os

DB_PATH = os.path.join(os.getcwd(), "action_grid.db")

def upgrade_schema():
    print("\n" + "="*55)
    print("🗄️ THE JUICER: SCHEMA UPGRADE (PROJECTIONS)")
    print("="*55)
    
    conn = sqlite3.connect(DB_PATH)
    cols = [
        ("floor_fp", "REAL DEFAULT 0.0"),
        ("median_fp", "REAL DEFAULT 0.0"),
        ("ceiling_fp", "REAL DEFAULT 0.0"),
        ("matchup_multiplier", "REAL DEFAULT 1.0"),
        ("news_flag", "TEXT DEFAULT NULL")
    ]
    
    for col, dtype in cols:
        try:
            conn.execute(f"ALTER TABLE player_rankings ADD COLUMN {col} {dtype}")
            print(f"  ✓ Added column: {col}")
        except sqlite3.OperationalError:
            print(f"  - Column {col} already exists.")
            
    conn.commit()
    conn.close()
    print("✅ Schema upgrade complete.\n")

if __name__ == "__main__":
    upgrade_schema()