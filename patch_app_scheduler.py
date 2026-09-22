with open("app.py", "r", encoding="utf-8") as f:
    code = f.read()

scheduler_setup = """
# --- AUTONOMOUS SCHEDULER SINGLETON (ROADMAP #55-64) ---
from scheduler import JobScheduler, thread_safe_log_fn
import db_migration

@st.cache_resource
def get_global_scheduler():
    conn = sqlite3.connect("action_grid.db", check_same_thread=False)
    db_migration.run_migration(conn)
    conn.close()
    
    sched = JobScheduler(log_fn=thread_safe_log_fn("action_grid.db"))
    # Register routine health check
    sched.register_job("system_heartbeat", lambda: None, interval_seconds=120, run_at_start=True)
    sched.start()
    return sched

global_scheduler = get_global_scheduler()
"""

if "get_global_scheduler" not in code:
    insertion_point = "st.set_page_config("
    if insertion_point in code:
        parts = code.split(insertion_point, 1)
        new_code = parts[0] + scheduler_setup + "\n" + insertion_point + parts[1]
        with open("app.py", "w", encoding="utf-8") as f:
            f.write(new_code)
        print("✅ Scheduler singleton cleanly integrated into app.py.")