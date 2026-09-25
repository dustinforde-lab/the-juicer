# THE JUICER // COMPLETE SYSTEM ARCHITECTURE BLUEPRINT
**Snapshot Taken:** 2026-09-18 19:21:15
**Target File for System Recovery:** `MASTER_RECOVERY_SNAPSHOT_DO_NOT_DELETE.json`

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
If any file or database table breaks, run `python restore_from_snapshot.py` to restore all scripts and SQLite tables directly from `MASTER_RECOVERY_SNAPSHOT_DO_NOT_DELETE.json`.
