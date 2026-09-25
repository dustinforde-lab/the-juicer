with open("app.py", "r", encoding="utf-8") as f:
    code = f.read()

mfl_job = """
    # MFL Roster Sync (Runs every 4 hours)
    import mfl_sync
    sched.register_job("mfl_roster_sync", mfl_sync.run_mfl_sync, interval_seconds=14400, run_at_start=True)
"""

if "mfl_roster_sync" not in code and "sched.start()" in code:
    code = code.replace("sched.start()", mfl_job + "\n    sched.start()")
    with open("app.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("✅ MFL Sync added to background scheduler.")