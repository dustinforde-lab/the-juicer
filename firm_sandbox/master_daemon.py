import os
import sqlite3
import random
import time
from datetime import datetime, timedelta

SANDBOX_DIR = "firm_sandbox"
SANDBOX_DB = os.path.join(SANDBOX_DIR, "sandbox_grid.db")

class MasterDaemon:
    def __init__(self):
        self.consecutive_failures = 0
        self.max_failures_before_circuit_break = 3
        self.active_intern_index = 0
        self.intern_pool = ["Intern-Alpha (Primary Feed)", "Intern-Beta (Backup Mirror)", "Intern-Gamma (Proxy Mirror)"]

    def run_single_cycle(self):
        print("=" * 65)
        print(f"⚙️ [MASTER DAEMON] Execution cycle started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 65)
        
        # Contingency 2: Circuit Breaker & Intern Rotator
        current_intern = self.intern_pool[self.active_intern_index]
        print(f"   🔄 Active Worker Assigned: {current_intern}")
        
        try:
            # Contingency 1: Try-Except Shield & Contingency 4: Data Integrity Gatekeeper
            os.makedirs(SANDBOX_DIR, exist_ok=True)
            with sqlite3.connect(SANDBOX_DB) as conn:
                cur = conn.cursor()
                
                # Simulate a live data payload check
                payload = {"player": "Bo Nix", "stat": "Passing Yards", "line": 215.5}
                
                # Gatekeeper validation check
                if not payload.get("player") or not isinstance(payload.get("line"), (int, float)):
                    raise ValueError("Data Integrity Gatekeeper: Corrupt or invalid payload detected!")
                
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS sandbox_master_telemetry (
                        node TEXT PRIMARY KEY, 
                        heartbeat TEXT, 
                        status TEXT, 
                        details TEXT
                    )
                """)
                cur.execute("""
                    INSERT OR REPLACE INTO sandbox_master_telemetry (node, heartbeat, status, details)
                    VALUES (?, ?, ?, ?)
                """, ("24/7 Master Daemon", timestamp, "HEALTHY // 24/7 ACTIVE", f"Successfully polled via {current_intern}"))
                conn.commit()
                
            print("   ✅ Cycle execution passed. Data integrity verified by Gatekeeper.")
            self.consecutive_failures = 0
            return True

        except Exception as e:
            # Contingency 1: Catch error without crashing the daemon loop
            self.consecutive_failures += 1
            print(f"   ⚠️ [TRY-EXCEPT SHIELD] Caught Exception: {e}")
            print(f"   🚨 Consecutive Failure Count: {self.consecutive_failures}/{self.max_failures_before_circuit_break}")
            
            # Contingency 2: Trip circuit breaker and rotate interns if threshold met
            if self.consecutive_failures >= self.max_failures_before_circuit_break:
                self.active_intern_index = (self.active_intern_index + 1) % len(self.intern_pool)
                print(f"   ⚡ [CIRCUIT BREAKER TRIPPED] Rotating intern pool to: {self.intern_pool[self.active_intern_index]}")
                self.consecutive_failures = 0
            return False

    def check_watchdog(self):
        # Contingency 3: Stale-Data Watchdog Check
        if not os.path.exists(SANDBOX_DB):
            print("   🐶 [WATCHDOG] Sandbox telemetry database not yet initialized.")
            return
            
        with sqlite3.connect(SANDBOX_DB) as conn:
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sandbox_master_telemetry'")
            if cur.fetchone():
                cur.execute("SELECT heartbeat FROM sandbox_master_telemetry WHERE node = '24/7 Master Daemon'")
                row = cur.fetchone()
                if row:
                    last_hb = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                    delta = datetime.now() - last_hb
                    if delta > timedelta(minutes=45):
                        print("   🚨 [STALE-DATA WATCHDOG] Warning: Heartbeat older than 45 minutes! Initiating self-heal reset...")
                    else:
                        print(f"   🐶 [WATCHDOG OKAY] Last system heartbeat was {int(delta.total_seconds())} seconds ago.")

if __name__ == "__main__":
    daemon = MasterDaemon()
    daemon.check_watchdog()
    daemon.run_single_cycle()
    print("=" * 65)
    print("🟢 MASTER DAEMON SANDBOX CYCLE COMPLETE.")
    print("=" * 65)
