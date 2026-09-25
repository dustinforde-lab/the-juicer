import sqlite3
import pandas as pd
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "action_grid.db")

def initialize_action_grid():
    """Ensure the core tables exist for the Master Plan."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS dfs_projections (
                Player TEXT PRIMARY KEY,
                Pos TEXT,
                Team TEXT,
                Opp TEXT,
                Salary REAL,
                PassYds REAL DEFAULT 0,
                PassTD REAL DEFAULT 0,
                RushYds REAL DEFAULT 0,
                RushTD REAL DEFAULT 0,
                Rec REAL DEFAULT 0,
                RecYds REAL DEFAULT 0,
                RecTD REAL DEFAULT 0,
                Updated_At TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS vegas_lines (
                Game_ID TEXT PRIMARY KEY,
                Home TEXT,
                Away TEXT,
                Spread REAL,
                Over_Under REAL,
                Weather_Alert TEXT,
                Updated_At TEXT
            )
        """)
        print("✅ action_grid.db initialized with DFS and Vegas tables.")

def ingest_draftkings_csv(csv_path="DKSalaries.csv"):
    """Loads the DraftKings salary CSV into the DFS pool."""
    if not os.path.exists(csv_path):
        print(f"⚠️ {csv_path} not found. Drop the DKSalaries.csv file in the folder to sync salaries.")
        return
        
    try:
        df = pd.read_csv(csv_path)
        
        # Clean DK CSV headers (Name, Position, TeamAbbrev, Salary) for our DB
        mapping = {"Name": "Player", "Position": "Pos", "TeamAbbrev": "Team", "Salary": "Salary"}
        
        # Only keep columns that exist in the mapping to avoid errors
        available_cols = [c for c in df.columns if c in mapping.keys()]
        df = df[available_cols].rename(columns=mapping)
        
        df["Updated_At"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Merge into SQLite safely using an upsert pattern
        with sqlite3.connect(DB_PATH) as conn:
            df.to_sql("dfs_projections_temp", conn, if_exists="replace", index=False)
            
            # Upsert logic to keep Mike's stats but update salaries and teams
            conn.execute("""
                INSERT INTO dfs_projections (Player, Pos, Team, Salary, Updated_At)
                SELECT Player, Pos, Team, Salary, Updated_At FROM dfs_projections_temp
                ON CONFLICT(Player) DO UPDATE SET 
                    Salary = excluded.Salary,
                    Team = excluded.Team,
                    Updated_At = excluded.Updated_At
            """)
            conn.execute("DROP TABLE dfs_projections_temp")
            print(f"✅ DraftKings salaries successfully ingested and merged from {csv_path}.")
            
    except Exception as e:
        print(f"🚨 Ingestion Error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Mike Donna Ingestion Pipeline...")
    initialize_action_grid()
    ingest_draftkings_csv()
