import os
import re
import sqlite3
import subprocess

# Auto-detect real Desktop path (handles OneDrive)
user_home = os.path.expanduser("~")
onedrive_desktop = os.path.join(user_home, "OneDrive", "Desktop")
standard_desktop = os.path.join(user_home, "Desktop")

if os.path.exists(onedrive_desktop):
    desktop_dir = onedrive_desktop
elif os.path.exists(standard_desktop):
    desktop_dir = standard_desktop
else:
    desktop_dir = user_home

report_path = os.path.join(desktop_dir, "we fucked up again.txt")

lines = []
def log(msg=""):
    lines.append(msg)
    print(msg)

log("=" * 65)
log("  THE JUICER: SYSTEM CONTINUITY & WIRING AUDIT")
log("=" * 65)

# 1. DATABASE CHECK
log("\n[1] DATABASE TANK STATUS (action_grid.db)")
log("-" * 40)
db_path = "action_grid.db"
if not os.path.exists(db_path):
    log("[!] CRITICAL: action_grid.db not found.")
else:
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
        log(f"Tables Found: {', '.join(tables)}")

        if "slips" in tables:
            total_slips = cur.execute("SELECT COUNT(*) FROM slips").fetchone()[0]
            log(f"\n* slips table: {total_slips} total entries")
            if total_slips > 0:
                for p, c in cur.execute("SELECT platform, COUNT(*) FROM slips GROUP BY platform").fetchall():
                    log(f"    - Platform [{p}]: {c}")
                for s, c in cur.execute("SELECT status, COUNT(*) FROM slips GROUP BY status").fetchall():
                    log(f"    - Status [{s}]: {c}")
        else:
            log("[FLAGGED] 'slips' table missing.")

        if "dfs_rosters" in tables:
            total_dfs = cur.execute("SELECT COUNT(*) FROM dfs_rosters").fetchone()[0]
            log(f"\n* dfs_rosters table: {total_dfs} rosters saved")
        else:
            log("[FLAGGED] 'dfs_rosters' table missing.")

        conn.close()
    except Exception as e:
        log(f"Database error: {e}")

# 2. WIRING AUDIT: app.py vs ui_components.py
log("\n[2] CONTROL WIRING AUDIT")
log("-" * 40)

app_calls = []
if os.path.exists("app.py"):
    with open("app.py", "r", encoding="utf-8") as f:
        app_text = f.read()
    app_calls = re.findall(r"ui\.(render_[a-zA-Z0-9_]+)\(", app_text)

ui_defs = []
if os.path.exists("ui_components.py"):
    with open("ui_components.py", "r", encoding="utf-8") as f:
        for line in f:
            m = re.match(r"^def (render_[a-zA-Z0-9_]+)\(", line)
            if m:
                ui_defs.append(m.group(1))

log("Functions app.py is trying to call:")
for fn in app_calls:
    if fn in ui_defs:
        log(f"  ✅ ui.{fn}() -> WIRED AND FOUND")
    else:
        log(f"  ❌ ui.{fn}() -> SEVERED WIRE (Not defined in ui_components.py)")

log("\nFunctions ui_components.py is actually exporting:")
for fn in ui_defs:
    status = "CALLED BY APP" if fn in app_calls else "ORPHANED / UNUSED"
    log(f"  * {fn}() -> [{status}]")

# Write to Desktop
try:
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    log("\n" + "=" * 65)
    log(f"Report saved to Desktop:\n{report_path}")
    log("=" * 65)
except Exception as e:
    log(f"File save error: {e}")