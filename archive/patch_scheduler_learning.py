with open("app.py", "r", encoding="utf-8") as f:
    code = f.read()

learning_job = """
    # Bayesian Learning Loop (Roadmap #100)
    import learning_loop
    sched.register_job("bayesian_recalibration", learning_loop.recalibrate, interval_seconds=86400, run_at_start=True)
"""

if "bayesian_recalibration" not in code and "sched.start()" in code:
    code = code.replace("sched.start()", learning_job + "\n    sched.start()")
    with open("app.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("✅ Learning Loop added to background scheduler.")
else:
    print("⚠️ Scheduler already configured or target not found.")