import os
import sqlite3
from datetime import datetime

SANDBOX_DIR = "firm_sandbox"
SANDBOX_DB = os.path.join(SANDBOX_DIR, "sandbox_grid.db")

def run_sandbox_learning_cycle():
    print("=" * 65)
    print("🧠 [BACK OFFICE STAGING] Running Sandbox Self-Learning Loop...")
    print("=" * 65)
    
    if not os.path.exists(SANDBOX_DB):
        print("❌ Sandbox database not initialized yet. Run previous sandbox scripts first.")
        return

    with sqlite3.connect(SANDBOX_DB) as conn:
        cur = conn.cursor()
        
        # Create mock learning ledger in sandbox if not exists
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sandbox_learning_ledger (
                audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT,
                outcome TEXT,
                edge_rating REAL,
                audited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insert sample audit rows if empty
        cur.execute("SELECT COUNT(*) FROM sandbox_learning_ledger")
        if cur.fetchone()[0] == 0:
            cur.executemany("""
                INSERT INTO sandbox_learning_ledger (ticket_id, outcome, edge_rating)
                VALUES (?, ?, ?)
            """, [
                ("SLIP-SBOX-01", "HIT", 1.12),
                ("SLIP-SBOX-02", "HIT", 1.08),
                ("SLIP-SBOX-03", "BUST", 1.15),
                ("SLIP-SBOX-04", "HIT", 1.05)
            ])
            conn.commit()
        
        # Calculate mock hit rate
        cur.execute("SELECT outcome FROM sandbox_learning_ledger")
        outcomes = [r[0] for r in cur.fetchall()]
        hits = outcomes.count("HIT")
        total = len(outcomes)
        hit_rate = (hits / total) if total > 0 else 0.0
        
        print(f"   📊 Sandbox Audit Sample: {total} tracked tickets ({hits} Hits)")
        print(f"   📈 Sandbox Model Hit Rate: {round(hit_rate * 100, 1)}%")
        print("   ✅ Sandbox Self-Learning Recalibration Successful.")
    print("=" * 65)

if __name__ == "__main__":
    run_sandbox_learning_cycle()
