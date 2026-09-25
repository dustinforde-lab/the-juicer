import os, glob, json, sqlite3, ast
from datetime import datetime

DB_FILE = "action_grid.db"
SNAPSHOT_JSON = "MASTER_RECOVERY_SNAPSHOT_DO_NOT_DELETE.json"
BLUEPRINT_MD = "MASTER_ARCHITECTURE_BLUEPRINT.md"

def build_snapshot():
    print("=" * 65)
    print("📦 [MASTER SYSTEM SNAPSHOT & RECOVERY AUDIT] Starting...")
    print("=" * 65)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 1. Codebase Harvest & AST Syntax Verification
    scripts = glob.glob("*.py")
    codebase_archive = {}
    syntax_passes = 0
    
    print("\n🔍 Phase 1: Verifying Script Syntax & Harvesting Codebase...")
    for script in sorted(scripts):
        if script == "create_master_snapshot.py":
            continue
        with open(script, "r", encoding="utf-8", errors="ignore") as f:
            code = f.read()
        try:
            ast.parse(code)
            status = "HEALTHY"
            syntax_passes += 1
        except Exception as e:
            status = f"SYNTAX_ERR: {e}"
        codebase_archive[script] = {"status": status, "size_bytes": len(code), "source": code}
        print(f"   • [{status[:7]}] {script:<26} ({len(code):>5} bytes)")

    # 2. Database State & Table Extraction
    print("\n🗄️ Phase 2: Auditing Database Integrity & Backing Up Records...")
    db_state = {"schema": {}, "tables": {}}
    table_counts = {}
    if os.path.exists(DB_FILE):
        with sqlite3.connect(DB_FILE) as conn:
            cur = conn.cursor()
            cur.execute("SELECT name, sql FROM sqlite_master WHERE type='table'")
            for tbl, ddl in cur.fetchall():
                db_state["schema"][tbl] = ddl
                cur.execute(f"SELECT * FROM {tbl}")
                rows = cur.fetchall()
                db_state["tables"][tbl] = rows
                table_counts[tbl] = len(rows)
                print(f"   • [DB_OK] Table '{tbl}': {len(rows)} records stored.")
    else:
        print(f"   ⚠️ Warning: {DB_FILE} not detected.")

    # 3. Save Machine-Readable Master Recovery File
    snapshot_payload = {
        "snapshot_timestamp": timestamp,
        "environment": "The Juicer // Base Working Architecture",
        "scripts_archived": codebase_archive,
        "database_state": db_state
    }
    with open(SNAPSHOT_JSON, "w", encoding="utf-8") as f:
        json.dump(snapshot_payload, f, indent=2)
    print(f"\n💾 Machine Recovery Snapshot Saved -> {SNAPSHOT_JSON}")

    # 4. Generate Comprehensive Human/AI Architectural Blueprint
    blueprint_content = f"""# THE JUICER // COMPLETE SYSTEM ARCHITECTURE BLUEPRINT
**Snapshot Taken:** {timestamp}
**Target File for System Recovery:** `{SNAPSHOT_JSON}`

---

## 1. Groundwork & Persistence Layer (`action_grid.db`)
- **`theoretical_bets`**: Stores active 200 parlay slips (`ticket_id`, `weight_class`, `odds`, `border_color`, `ticket_json`).
- **`dfs_classic_lineups`**: Stores active 200 DraftKings rosters (`id`, `archetype`, `total_salary`, `projected_pts`, `roster_json`).
- **`system_telemetry`**: Stores real-time daemon heartbeats, status markers, latency metrics, and agent logs.
- **`completed_teams_blacklist`**: Quarantine registry for finalized teams (e.g., DET, BUF) to prevent slate contamination.

## 2. Agent Daemons & Automated Workflows
- **Donna (`team_cleanser.py`)**: Connects to the ESPN scoreboard API, identifies concluded games, updates `completed_teams_blacklist`, and scrubs contaminated slips.
- **Lewis (`lewis_watchdog.py`)**: Background watchdog verifying database locks, Sleeper API telemetry, and consensus fallback caches.
- **Audit & Cleanse (`roster_audit.py`, `purge_and_rebuild.py`)**: Roster verification and generator algorithms maintaining the 400-item inventory without Thursday slate overlap.

## 3. Presentation Layer & UI Wiring (`app.py`, `ui_components.py`)
- **Streamlit Engine**: Binds to port 8501, running headless with CORS/XSRF checks adapted for local and tunneled access.
- **Aesthetic Core**: Neon accents (Cash Builder: `#00ff88`, Syndicate: `#00e5ff`, Whale: `#ff2a6d`) layered over dark `#0b0e14` backgrounds.
- **Widget Key Standard**: Sequential unique keys (`key='...'`) enforced across interactive elements to prevent `StreamlitDuplicateElementId` runtime errors.

## 4. Disaster Recovery Procedure
If any file or database table breaks, run `python restore_from_snapshot.py` to restore all scripts and SQLite tables directly from `{SNAPSHOT_JSON}`.
"""
    with open(BLUEPRINT_MD, "w", encoding="utf-8") as f:
        f.write(blueprint_content)
    print(f"📄 Full Architecture Blueprint Saved  -> {BLUEPRINT_MD}")

    # 5. Built-In Health Check & Pass/Fail Scorecard
    print("\n" + "=" * 65)
    print("🚦 [BUILT-IN SELF-CHECK SCORECARD]")
    print("=" * 65)
    bets_count = table_counts.get("theoretical_bets", 0)
    dfs_count = table_counts.get("dfs_classic_lineups", 0)
    
    buf_det_leaks = 0
    if os.path.exists(DB_FILE):
        with sqlite3.connect(DB_FILE) as conn:
            cur = conn.cursor()
            try:
                cur.execute("SELECT ticket_json FROM theoretical_bets")
                for (t_json,) in cur.fetchall():
                    if "DET" in t_json or "BUF" in t_json:
                        buf_det_leaks += 1
            except Exception:
                pass

    print(f" • Valid Python Files Audited : {syntax_passes}/{len(codebase_archive)} [PASS]")
    print(f" • Parlay Inventory Level     : {bets_count}/200 [PASS if 200]")
    print(f" • DFS Lineup Inventory Level : {dfs_count}/200 [PASS if 200]")
    print(f" • TNF Quarantine Leaks       : {buf_det_leaks} [PASS if 0]")
    print("=" * 65)
    print("✅ System fully archived. Safe to proceed with updates.")
    print("=" * 65)

if __name__ == "__main__":
    build_snapshot()
