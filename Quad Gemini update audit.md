# ⚡ QUAD GEMINI UPDATE AUDIT (FOR CLAUDE)
**Date:** September 24, 2026
**Target Architecture:** The Juicer Autonomous Quantitative Betting & DFS Engine

## 1. System Health & Incident Post-Mortem
* **Tab 4 Parlay Crash Root Cause:** `ValueError: Sample larger than population`. In `ui_parlay_mix.py`, tickets with 10 legs called `random.sample(pool, 10)` against a fallback test pool containing only 8 items. Guardrails in `app.py` successfully caught the exception and kept the other 9 tabs operational.
* **Empty DFS & Rankings Tab Root Cause:** SQLite database (`action_grid.db`) tables `dfs_projections` and `vegas_lines` were unpopulated, forcing fallback to 2-3 hardcoded players.
* **Architecture Integrity:** Zero cross-tab imports remain intact. All UI tabs query `data_service.py` exclusively.

## 2. Secrets & API Configuration
Keys reside in `.streamlit/secrets.toml`:
* `THE_ODDS_API_KEY`: Quota-budgeted prop and spread ingestion.
* `SLEEPER_API_KEY`: Optional auth or fallback to open player endpoints.
* `MFL_API_KEY` / `MFL_LEAGUE_ID`: MyFantasyLeague franchise and keeper sync for Straight Cash.
* `ESPN_ENDPOINT`: Open scoreboard telemetry (free, 60s pulse).

## 3. Data Pipeline & Database Schema (`action_grid.db`)
* `dfs_projections`: `(Rank, Player, Pos, Team, Opp, Salary, Mike_PPR, Value, Sim_Ceiling, Sim_Floor, Donna_Tier, Injury)`
* `vegas_lines`: `(game_id, home, away, spread, over_under, updated_at)`
* `system_status`: `(id, last_espn_sync, last_odds_sync, api_calls_used)`
* `pick_grades`: `(id, player, projected, actual, delta, hit, graded_at)`

## 4. UI/UX Rules for Next Claude Upgrade
1. **Never use raw tables (`st.dataframe`):** Use dark-mode glassmorphic HTML cards with positional neon accents.
2. **Defensive Sampling:** In procedural generators, always clamp sample sizes with `min(requested_legs, len(pool))` to guarantee math safety.
3. **No Direct Requests in UI:** UI files must never execute `requests.get()`; all network operations belong in `data_service.py` or `scheduler_daemon.py`.
