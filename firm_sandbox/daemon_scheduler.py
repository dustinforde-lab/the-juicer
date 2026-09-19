import os
import sqlite3
import random
import time
from datetime import datetime

SANDBOX_DIR = "firm_sandbox"
SANDBOX_DB = os.path.join(SANDBOX_DIR, "sandbox_grid.db")

def run_sandbox_scheduler_cycle():
    print("=" * 65)
    print("⚙️ [BACK OFFICE STAGING] Running Sandbox Daemon Scheduler...")
    print("=" * 65)
    
    if not os.path.exists(SANDBOX_DB):
        print("❌ Sandbox database not initialized yet. Run intern_validator.py first.")
        return

    with sqlite3.connect(SANDBOX_DB) as conn:
        cur = conn.cursor()
        
        # Ensure sandbox telemetry table exists
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sandbox_telemetry (
                node_name TEXT,
                status TEXT,
                last_ping TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Simulate an intern worker fetch with anti-ban jitter
        worker_id = "Intern-Beta (Staging Shield)"
        jitter = round(random.uniform(0.1, 0.4), 2)
        time.sleep(jitter)
        
        cur.execute("""
            INSERT INTO sandbox_telemetry (node_name, status)
            VALUES (?, ?)
        """, (worker_id, f"HEALTHY // JITTER: {jitter}s // ZERO BANS"))
        
        conn.commit()
        
        # Pull queue count
        cur.execute("SELECT COUNT(*) FROM sandbox_incoming_queue")
        q_count = cur.fetchone()[0]
        
        print(f"   🔄 Staging Worker: {worker_id}")
        print(f"   ⏱️ Applied Anti-Ban Jitter: {jitter}s")
        print(f"   📊 Sandbox Queue Status: {q_count} payloads successfully indexed.")
        print("   ✅ Sandbox Scheduler Cycle Complete.")
    print("=" * 65)

if __name__ == "__main__":
    run_sandbox_scheduler_cycle()
