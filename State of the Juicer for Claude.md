# ⚡ STATE OF THE JUICER FOR CLAUDE
**System Time:** 2026-09-24 21:03:38
**Project:** The Juicer (Autonomous Quant Engine & Fantasy Football War Room)

## 1. Role Directive & AI Synergy Protocol
You are stepping in as the Co-Architect of this application. Gemini has built the foundational plumbing, the live API daemons, and the UI layout guardrails. Your objective is to build upon this without breaking the established architecture. 
**If Gemini needs to resume work after you, we operate on the exact same strict rulebook.**

## 2. Gemini's Preferred Style & Architecture Rules
Do not deviate from these structural decisions:
* **The "No Patching" Rule:** We do not write wrapper files or piecemeal hotfixes. If a module needs an update, you must rewrite the *entire* file (e.g., ui_dfs.py) so there is a single, clean source of truth.
* **The State Bus (Zero Cross-Imports):** UI files (ui_*.py) are strictly forbidden from importing each other. All shared data, Evaluator 3.0 calculations, and SQLite queries are centralized in data_service.py. 
* **Isolated Execution:** pp.py is our root file. It loops through all 10 UI modules and wraps each in a localized 	ry/except block. If your code crashes Tab 3, the other 9 tabs must remain fully operational.

## 3. UI/UX Aesthetics (Do Not Sterilize the App)
* **No Raw Dataframes:** Do not use st.dataframe() for primary dashboards. We use custom HTML/CSS cards.
* **Dark Glassmorphism:** Primary containers use ackground: rgba(13,17,23,0.85); backdrop-filter: blur(10px); border: 1px solid #30363d;.
* **Neon Accents:** Enforce positional color coding (QB: #00e5ff, RB: #ff2a6d, WR: #00ff88, TE: #ffd700, K: #ff9f43).
* **Horizontal Capsule Pills:** All lineups, parlays, and prop slips must be rendered as side-by-side pill divs with overflow-x: auto; to allow horizontal scrolling on massive 10-leg tickets.

## 4. Hardcoded Platform Compliance Math
Any ticket generator you write must obey these physical laws:
* **DraftKings Showdown:** ,000 cap. Exactly 6 players (1 CPT at 1.5x salary, 5 FLEX).
* **DraftKings Classic:** Must contain players from at least 2 different NFL games.
* **PrizePicks:** Slips must be 2 to 6 legs. *Crucial Guardrail:* Slips must contain players from at least TWO different teams. Single-team slips are illegal.
* **Slate Flush:** If the "Sunday Classic" slate is toggled, any players from games that have already started (e.g., Thursday Night Football) must be filtered out of the master dataframe before rendering.

## 5. Background Daemon
scheduler_daemon.py runs 24/7 on a cloud server. It hammers ESPN every 60 seconds (free) and selectively pulses The Odds API based on a day-of-week schedule to protect a 500/month call quota. It writes freshness timestamps to ction_grid.db.
