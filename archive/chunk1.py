import sqlite3, sys, datetime

print("🚦 [LOGISTICS CONTROL] Deploying Traffic Management Tier...")
DB_PATH = "action_grid.db"

def init_traffic_control():
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    cur = conn.cursor()
    # Turn on the Traffic Light (Write-Ahead Logging) so trucks don't crash
    cur.execute("PRAGMA journal_mode=WAL;")
    wal_mode = cur.fetchone()[0]
    cur.execute("PRAGMA busy_timeout=5000;")
    
    # Build the garage for our logistics team
    cur.execute("""CREATE TABLE IF NOT EXISTS logistics_control (id INTEGER PRIMARY KEY, component TEXT UNIQUE, status TEXT, active_locks INTEGER, last_heartbeat TIMESTAMP)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS enterprise_hierarchy (tier TEXT, title TEXT UNIQUE, reports_to TEXT, headcount INTEGER, status TEXT)""")
    
    # Hire the Traffic Manager and his 2 Assistants
    now = datetime.datetime.now().isoformat()
    staff = [
        ("LOGISTICS", "Traffic Manager", "Donna", 1, "ONLINE"),
        ("LOGISTICS", "Lane Marshall (Assistant 1)", "Traffic Manager", 1, "ONLINE"),
        ("LOGISTICS", "Radar Scout (Assistant 2)", "Traffic Manager", 1, "ONLINE")
    ]
    
    for t, title, r, c, s in staff:
        cur.execute("INSERT OR REPLACE INTO enterprise_hierarchy (tier, title, reports_to, headcount, status) VALUES (?, ?, ?, ?, ?)", (t, title, r, c, s))
        
    cur.execute("INSERT OR REPLACE INTO logistics_control (component, status, active_locks, last_heartbeat) VALUES ('WAL_GATEWAY', 'OPERATIONAL', 0, ?)", (now,))
    conn.commit()
    conn.close()
    return wal_mode

def run_chunk1_audit(wal_mode):
    print("\n🔍 RUNNING CHUNK 1 SELF-CHECK & AUDIT...")
    errors = []
    
    # Check 1: Is the traffic light actually on?
    if str(wal_mode).upper() != "WAL": errors.append(f"WAL Mode failed: {wal_mode}")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        
        # Check 2: Is the garage damaged?
        cur.execute("PRAGMA integrity_check;")
        if cur.fetchone()[0] != "ok": errors.append("Database integrity failure.")
        
        # Check 3: Did all 3 employees show up for work?
        cur.execute("SELECT count(*) FROM enterprise_hierarchy WHERE tier='LOGISTICS';")
        if cur.fetchone()[0] != 3: errors.append("Roster headcount mismatch. Missing employees.")
        conn.close()
    except Exception as e:
        errors.append(f"Audit exception: {e}")
        
    # Final Report Card
    if errors:
        print("❌ AUDIT FAILED:")
        for err in errors: print(f"  -> {err}")
        sys.exit(1)
    else:
        print("✅ [PASS] Concurrency: Traffic lights (WAL mode) activated.")
        print("✅ [PASS] Integrity: Database structural scan is clean.")
        print("✅ [PASS] Roster: Traffic Manager & 2 Assistants safely registered.")
        print("🎯 CHUNK 1 INTEGRITY VERIFIED. READY FOR CHUNK 2.")

if __name__ == "__main__":
    wal = init_traffic_control()
    run_chunk1_audit(wal)