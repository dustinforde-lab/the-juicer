import sys
import sqlite3
from datetime import datetime

# Enforce UTF-8 handling for Windows stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DB_FILE = "action_grid.db"

LIVE_INJURY_FEED = [
    {"player": "CeeDee Lamb", "team": "DAL", "status": "Questionable", "note": "Ankle - DNP Friday"},
    {"player": "Brock Purdy", "team": "SF", "status": "Out", "note": "Concussion Protocol"},
    {"player": "Travis Kelce", "team": "KC", "status": "Doubtful", "note": "Hamstring Tightness"}
]

def deploy_the_medic():
    print("=" * 65)
    print("[MEDIC] [UPGRADE CHUNK 5] Deploying 'The Medic' Injury Feed...")
    print("=" * 65)
    
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS hospital_ward (
                player_name TEXT PRIMARY KEY,
                team TEXT,
                status TEXT,
                medical_note TEXT,
                updated_at TEXT
            )
        """)
        
        cur.execute("DELETE FROM hospital_ward")
        now_ts = datetime.now().strftime("%Y-%m-%d %I:%M %p ET")
        
        for inj in LIVE_INJURY_FEED:
            cur.execute("""
                INSERT INTO hospital_ward VALUES (?, ?, ?, ?, ?)
            """, (inj["player"], inj["team"], inj["status"], inj["note"], now_ts))
            print(f"   * [MEDIC ALERT] {inj['player']} ({inj['team']}) -> {inj['status']}")
            
        conn.commit()

def run_self_test():
    print("\n[SELF-CHECK GATE] Verifying Hospital Ward Database...")
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        rows = cur.execute("SELECT * FROM hospital_ward").fetchall()
        assert len(rows) == len(LIVE_INJURY_FEED), "Integrity Failure: Injury data did not save."
    print("ALL GATES PASSED: Hospital Ward table built and populated successfully.\n")

if __name__ == "__main__":
    deploy_the_medic()
    run_self_test()
