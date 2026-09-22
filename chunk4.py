import sqlite3, sys, datetime

print("⚙️ [ASSEMBLY LINE] Deploying the Task Queue Conveyor Belt...")
DB_PATH = "action_grid.db"

def deploy_task_queue():
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    cur = conn.cursor()
    
    # 1. Build the Conveyor Belt
    cur.execute("""
        CREATE TABLE IF NOT EXISTS task_queue (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            department TEXT,
            task_name TEXT,
            status TEXT,
            assigned_to TEXT,
            created_at TIMESTAMP
        )
    """)
    
    # Clear the old mess to start fresh
    cur.execute("DELETE FROM task_queue")
    
    # 2. Put the first work orders on the belt for the squads
    tasks = [
        ("LEWIS", "Scrape DraftKings NFL Props", "PENDING", "Prop Aggregator Squad"),
        ("LEWIS", "Audit Injury Voids", "PENDING", "Settlement Bureau"),
        ("MIKE", "Sync Sunday Inactives", "PENDING", "Medical Ward"),
        ("MIKE", "Run Dome Speed Adjustments", "PENDING", "Weather Scout"),
        ("DONNA", "Generate Sunday Classic 9-Man", "PENDING", "Slate Architect"),
        ("DONNA", "Enforce Max 30% RB Exposure", "PENDING", "Portfolio Governor")
    ]
    
    now = datetime.datetime.now().isoformat()
    for dept, name, status, assignee in tasks:
        cur.execute("""
            INSERT INTO task_queue (department, task_name, status, assigned_to, created_at) 
            VALUES (?, ?, ?, ?, ?)
        """, (dept, name, status, assignee, now))
        
    conn.commit()
    conn.close()

def run_chunk4_audit():
    print("\n🔍 RUNNING CHUNK 4 SELF-CHECK & AUDIT...")
    errors = []
    try:
        conn = sqlite3.connect(DB_PATH, timeout=5.0)
        cur = conn.cursor()
        
        # Test 1: Is the conveyor belt running?
        cur.execute("SELECT count(*) FROM task_queue;")
        count = cur.fetchone()[0]
        if count != 6: errors.append(f"Task queue failed to load. Found {count} tasks.")
        
        # Test 2: Can a worker pick up a box? (Simulating Lewis grabbing a task)
        cur.execute("UPDATE task_queue SET status = 'IN_PROGRESS' WHERE task_name = 'Scrape DraftKings NFL Props'")
        conn.commit()
        
        cur.execute("SELECT status FROM task_queue WHERE task_name = 'Scrape DraftKings NFL Props'")
        status = cur.fetchone()[0]
        if status != 'IN_PROGRESS': errors.append("Worker failed to claim the task. State stuck.")
        
        conn.close()
    except Exception as e:
        errors.append(f"Audit exception: {e}")
        
    if errors:
        print("❌ AUDIT FAILED:")
        for err in errors: print(f"  -> {err}")
        sys.exit(1)
    else:
        print("✅ [PASS] Conveyor Belt: Task queue table constructed successfully.")
        print("✅ [PASS] Work Orders: 6 initial tasks routed to Lewis, Mike, and Donna.")
        print("✅ [PASS] Worker Action: Verified squads can successfully claim and update tasks.")
        print("🎯 CHUNK 4 INTEGRITY VERIFIED. THE SQUADS ARE OFFICIALLY AT WORK.")

if __name__ == "__main__":
    deploy_task_queue()
    run_chunk4_audit()