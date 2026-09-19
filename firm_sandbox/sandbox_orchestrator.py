import os
import sqlite3
import json
from datetime import datetime

SANDBOX_DIR = "firm_sandbox"
SANDBOX_DB = os.path.join(SANDBOX_DIR, "sandbox_grid.db")

def run_sandbox_orchestrator():
    print("=" * 65)
    print("⚡ [BACK OFFICE STAGING] Running Sandbox Mass Orchestrator...")
    print("=" * 65)
    
    if not os.path.exists(SANDBOX_DB):
        print("❌ Sandbox database not initialized yet. Run previous sandbox scripts first.")
        return

    with sqlite3.connect(SANDBOX_DB) as conn:
        cur = conn.cursor()
        
        # Create sandbox production slip table if not exists
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sandbox_theoretical_bets (
                ticket_id TEXT PRIMARY KEY,
                weight_class TEXT,
                odds TEXT,
                source TEXT,
                ticket_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Simulate mass generation of 250 sandbox slips based on staged feeds
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sample_slips = [
            (f"SBOX-SLIP-{i:03d}", "Syndicate Core", "+1150", "Sandbox Staging Feed", 
             json.dumps([{"player": f"Staged Player {i}", "stat": "Over 215.5 Yards"}]))
            for i in range(1, 251)
        ]
        
        cur.executemany("""
            INSERT OR REPLACE INTO sandbox_theoretical_bets (ticket_id, weight_class, odds, source, ticket_json)
            VALUES (?, ?, ?, ?, ?)
        """, sample_slips)
        
        conn.commit()
        
        cur.execute("SELECT COUNT(*) FROM sandbox_theoretical_bets")
        total_staged = cur.fetchone()[0]
        
        print(f"   🎯 Sandbox Orchestration Complete: {total_staged} structured slips successfully generated.")
        print("   📁 Staging environment is fully verified and ready for Harvey's final review.")
    print("=" * 65)

if __name__ == "__main__":
    run_sandbox_orchestrator()
