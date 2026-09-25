# The Juicer - Gemini Rebuild Handoff

## Goal
Rebuild the Streamlit application from the attached source files and database while preserving the visible War Room dashboard, its tabs, and the SQLite-backed data model. The rebuilt app must start reliably without background threads preventing the UI from loading.

## Current project
- Root: `C:\Users\chuck\the-juicer`
- Entry point: `app.py`
- Database: `action_grid.db`
- Dependencies: `requirements.txt`
- Main UI modules: `ui_addresses.py`, `ui_components.py`, `ui_film_room.py`
- Runtime support: `config.py`, `db_migration.py`, `scheduler.py`, `learning_loop.py`, `mfl_sync.py`
- Backup entrypoint: `app_master_backup.py`
- UI backup: `ui_components_master_backup.py`

## Intended visible product
A Streamlit War Room with these views:
1. Vegas scoreboard
2. DFS optimizer / 9-man lineups
3. Player rankings and Donna leverage
4. Multi-book parlay matrix
5. Season-long fantasy rosters
6. PrizePicks and Underdog slips
7. Film Room / telemetry
8. Ops Center
9. Learning Loop

The visual direction is a dark dashboard with cyan, green, and magenta accents. Keep the UI functional first; avoid starting background jobs during page import unless they are guarded and recoverable.

## Database evidence
The current `action_grid.db` is approximately 1 MB and contains tables including:
- `player_rankings`
- `dfs_lineups` with 200 rows
- `dfs_rosters` with 200 rows
- `dfs_classic_lineups`
- `theoretical_bets`
- `slips`
- `agent_chatter`
- `system_telemetry`
- `correlation_weights`
- `bet_grading`
- `completed_teams_blacklist`
- `master_players`
- `sportsbook_quotes`
- `raw_slate_articles`
- `hospital_ward`
- `stadium_weather`
- `sharp_market_lines`

Treat the database as a data source. Do not drop or rebuild production tables on app startup.

## Confirmed runtime blockers in current app.py
1. `app.py` registers `learning_loop.recalibrate`, but `learning_loop.py` defines `recalculate_weights` and does not define `recalibrate`.
2. `app.py` passes `thread_safe_log_fn` directly into `JobScheduler`. In `scheduler.py`, `thread_safe_log_fn(db_path)` is a factory and must first be called with `DB_PATH`.
3. The scheduler should be optional. If a sync job fails, the Streamlit page must still render and show a visible status message.
4. `ui_addresses.py` contains tab renderers but does not expose an obvious `run_router()` or `main()` in the supplied source. The fallback path in `app.py` should therefore be the reliable router.
5. Several historical scripts mutate or drop database tables. Do not execute migration, repair, seed, purge, tracer, or reset scripts automatically during Streamlit import.
6. The repository contains multiple incompatible generations of UI and schema. Choose one canonical schema and add compatibility readers rather than mixing old table names and column names.

## Recommended first repair
Use a safe scheduler setup similar to:

```python
log_fn = thread_safe_log_fn(DB_PATH)
sched = JobScheduler(log_fn=log_fn)
sched.register_job(
    "bayesian_recalibration",
    learning_loop.recalculate_weights,
    interval_seconds=86400,
    run_at_start=False,
)
```

Wrap scheduler startup in a feature flag or a guarded function. The page should render even if scheduler startup fails.

## Rebuild status
The Streamlit entrypoint has now been rebuilt in `app.py`. The previous entrypoint is preserved as `app_before_full_rebuild_20260921.py`.

- Database migrations remain additive and are guarded.
- Background scheduling is opt-in with `JUICER_ENABLE_SCHEDULER=1`.
- The scheduler uses the database-bound logger factory correctly.
- The learning job uses the available `learning_loop.recalculate_weights` function.
- Each dashboard tab has an independent error boundary.
- The rebuilt app compiled successfully and returned HTTP 200 on an isolated Streamlit port.

## Recommended rebuild sequence
1. Make `app.py` a thin Streamlit router.
2. Add a read-only database service with one connection per operation.
3. Normalize schema reads for `dfs_lineups`/`dfs_rosters`, `theoretical_bets`/`slips`, and the two `agent_chatter` layouts.
4. Reuse the working render functions from the clean UI backup where possible.
5. Disable all destructive seed, purge, and reset scripts from startup.
6. Add unique Streamlit widget keys.
7. Add a health panel showing database path, table availability, row counts, and scheduler state.
8. Run `python -m py_compile` on all production modules.
9. Run Streamlit with a temporary copy of the database before deploying.

## Important security action
`oauth2.json` was included in the project material and contains live-looking OAuth credentials and tokens. Revoke or rotate those credentials immediately, remove the file from any upload or repository, and replace it with environment variables or Streamlit secrets. Never send that file to Gemini.

## Useful validation commands
```powershell
Set-Location C:\Users\chuck\the-juicer
python -m py_compile app.py config.py scheduler.py db_migration.py learning_loop.py mfl_sync.py ui_addresses.py ui_components.py
streamlit run app.py
```

## Constraints for the rebuild
- Preserve the current database; make a backup before migrations.
- Do not invent live odds or claim that simulated data is live.
- Keep API keys out of source code.
- Make network feeds optional with cached or empty states.
- A UI failure in one tab must not crash the whole app.
