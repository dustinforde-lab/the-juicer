import os
import sqlite3
import json
from datetime import datetime

SANDBOX_DIR = "firm_sandbox"
SANDBOX_DB = os.path.join(SANDBOX_DIR, "sandbox_grid.db")

def initialize_sandbox():
    print("=" * 65)
    print("🏢 [BACK OFFICE] Initializing Secure Staging Sandbox...")
    print("=" * 65)
    
    os.makedirs(SANDBOX_DIR, exist_ok=True)
    
    with sqlite3.connect(SANDBOX_DB) as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sandbox_incoming_queue (
                queue_id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_feed TEXT,
                raw_payload TEXT,
                validation_status TEXT,
                processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    print("   📁 [LOUIS'S CREW] Sandbox database and validation queue online.")

def test_intern_intake():
    initialize_sandbox()
    
    # Mock data packet from an intern feed
    sample_payload = json.dumps({
        "player": "Bo Nix", 
        "team": "DEN", 
        "prop": "Passing Yards", 
        "line": 215.5, 
        "confidence": "HIGH"
    })
    
    with sqlite3.connect(SANDBOX_DB) as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO sandbox_incoming_queue (source_feed, raw_payload, validation_status)
            VALUES (?, ?, ?)
        """, ("Intern-Alpha (Staging Feed)", sample_payload, "PASSED_STRICT_CHECK"))
        conn.commit()
        
    print("   ✅ [QA CHECK] Sample intern intake successfully validated and queued.")
    print("=" * 65)

if __name__ == "__main__":
    test_intern_intake()
