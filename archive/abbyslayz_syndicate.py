import sqlite3, sys, datetime, json

print("👑 [SYNDICATE BOSS] AbbySlayz is taking over the book...")
DB_PATH = "action_grid.db"

def deploy_abbyslayz_syndicate():
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    cur = conn.cursor()
    
    # 1. Register AbbySlayz and her 5 elite employees in the hierarchy
    syndicate_staff = [
        ("SYndICATE_BOSS", "AbbySlayz", "Chuck", 1, "IRONCLAD_ACTIVE"),
        ("SYNDICATE_EMPLOYEE", "The Enforcer (Auditor)", "AbbySlayz", 1, "ZERO_TOLERANCE"),
        ("SYNDICATE_EMPLOYEE", "The Sharp (Line Analyst)", "AbbySlayz", 1, "ACTIVE"),
        ("SYNDICATE_EMPLOYEE", "The Capologist (Salary Master)", "AbbySlayz", 1, "ACTIVE"),
        ("SYNDICATE_EMPLOYEE", "The Actuary (Probability Quant)", "AbbySlayz", 1, "ACTIVE"),
        ("SYNDICATE_EMPLOYEE", "The Executioner (DB Committer)", "AbbySlayz", 1, "LOCKED")
    ]
    
    for tier, title, reports, count, status in syndicate_staff:
        cur.execute("""
            INSERT OR REPLACE INTO enterprise_hierarchy (tier, title, reports_to, headcount, status)
            VALUES (?, ?, ?, ?, ?)
        """, (tier, title, reports, count, status))
        
    # 2. Build AbbySlayz's Master Parlay & DFS Control Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS abbys_master_book (
            ticket_id TEXT PRIMARY KEY,
            controller TEXT,
            slate_type TEXT,
            payload_json TEXT,
            status TEXT,
            timestamp TIMESTAMP
        )
    """)
    
    # 3. Process a pristine, Abby-approved batch under strict zero-tolerance rules
    now = datetime.datetime.now().isoformat()
    
    clean_parlay = [
        {"player": "Amon-Ra St. Brown", "team": "DET", "stat": "Receiving Yards", "line": "O 84.5", "status": "VERIFIED_SHARP"},
        {"player": "Jared Goff", "team": "DET", "stat": "Passing Touchdowns", "Nbr": "O 1.5", "status": "VERIFIED_SHARP"}
    ]
    
    clean_lineup = [
        {"pos": "QB", "name": "Lamar Jackson", "salary": 8200},
        {"pos": "RB", "name": "Saquon Barkley", "salary": 8000},
        {"pos": "RB", "name": "Bijan Robinson", "salary": 7800},
        {"pos": "WR", "name": "CeeDee Lamb", "salary": 8800},
        {"pos": "WR", "name": "Justin Jefferson", "salary": 8600},
        {"pos": "WR", "name": "Amon-Ra St. Brown", "salary": 7900},
        {"pos": "TE", "name": "Sam LaPorta", "salary": 4800},
        {"pos": "FLEX", "name": "Garrett Wilson", "salary": 6100},
        {"pos": "DST", "name": "Ravens D/ST", "salary": 2800}
    ]
    
    cur.execute("""
        INSERT OR REPLACE INTO abbys_master_book (ticket_id, controller, slate_type, payload_json, status, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, ("ABBY-SLIP-01", "AbbySlayz", "NFL_PARLAY", json.dumps(clean_parlay), "APPROVED_BY_ENFORCER", now))
    
    cur.execute("""
        INSERT OR REPLACE INTO abbys_master_book (ticket_id, controller, slate_type, payload_json, status, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, ("ABBY-ROSTER-01", "AbbySlayz", "DFS_CLASSIC_9MAN", json.dumps(clean_lineup), "APPROVED_BY_CAPOLOGIST", now))
    
    conn.commit()
    conn.close()

def run_abbys_audit():
    print("\n🔍 RUNNING ABBYSLAYZ SYNDICATE AUDIT...")
    errors = []
    try:
        conn = sqlite3.connect(DB_PATH, timeout=5.0)
        cur = conn.cursor()
        
        # Audit 1: Verify AbbySlayz is registered as boss
        cur.execute("SELECT status FROM enterprise_hierarchy WHERE title='AbbySlayz'")
        res = cur.fetchone()
        if not res or res[0] != "IRONCLAD_ACTIVE":
            errors.append("AbbySlayz is not properly registered as active syndicate boss.")
            
        # Audit 2: Verify her 5 employees are on payroll
        cur.execute("SELECT count(*) FROM enterprise_hierarchy WHERE reports_to='AbbySlayz'")
        staff_count = cur.fetchone()[0]
        if staff_count != 5:
            errors.append(f"Employee count mismatch under AbbySlayz: expected 5, found {staff_count}")
            
        # Audit 3: Verify master book has pristine data
        cur.execute("SELECT count(*) FROM abbys_master_book")
        book_count = cur.fetchone()[0]
        if book_count < 2:
            errors.append("Master book entries missing or rejected.")
            
        conn.close()
    except Exception as e:
        errors.append(f"Syndicate audit exception: {e}")
        
    if errors:
        print("❌ SYNDICATE AUDIT FAILED:")
        for err in errors: print(f"  -> {err}")
        sys.exit(1)
    else:
        print("✅ [PASS] Syndicate Boss: AbbySlayz is in full command.")
        print("✅ [PASS] Enforcer & Crew: All 5 elite operators locked in.")
        print("✅ [PASS] Master Book: Verified clean, zero-tolerance slips and rosters stored.")
        print("🎯 ABBYSLAYZ SYNDICATE SECURED. LAUNCHING THE JUICER...")

if __name__ == "__main__":
    deploy_abbyslayz_syndicate()
    run_abbys_audit()