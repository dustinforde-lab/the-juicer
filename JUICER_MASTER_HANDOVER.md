# ⚡ THE JUICER: MASTER AI HANDOVER & SYSTEM ARCHITECTURE
**Date:** September 24, 2026
**Role Directive:** You are the Lead Architect for "The Juicer," a professional-grade, autonomous quantitative fantasy football and sports betting command center. Resume development exactly from this state.

## 🔴 CRITICAL RULES OF ENGAGEMENT
1. **DO NOT DELETE OR CLEAN UP LEGACY CODE YET.** Your primary objective is to upgrade files and build new features. If you see redundant code, deprecated wrapper shims, or messy logic, **do not remove it**. Log it in cleanup_flag_ledger.md. We will execute a localized cleanup phase only after the application is confirmed stable.
2. **STRICT GUARDRAILS:** Zero cross-tab imports. UI modules (ui_*.py) must NEVER import other UI modules. All shared logic, Evaluator 3.0 math, and database queries must be routed through the central data_service.py and ddress_book.py.
3. **NO RAW DATAFRAMES IN THE UI:** All data must be rendered using custom HTML/CSS dark-mode glassmorphism. Use the established "Horizontal Capsule Pill" layout for all lineups, parlays, and prop slips.

## 🧠 SYSTEM ARCHITECTURE & PLUMBING
### 1. Database (ction_grid.db)
Central SQLite hub containing:
* dfs_projections: Ranked player pool, Mike's xFP, ceiling/floor sims, and Value ratios.
* egas_lines: Real-time spreads, totals, and implied team totals.
* system_status: Tracks last_espn_sync and last_odds_sync timestamps.

### 2. The 24/7 Scheduler Daemon (scheduler_daemon.py)
A headless background worker meant to run continuously on Streamlit Cloud/Railway. 
* **ESPN Scoreboard API:** Free JSON endpoint (site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard). Polled every 60 seconds during active game windows for clock, score, down-and-distance, and red zone.
* **The Odds API (500 Quota Limit):** Strictly budgeted. 1x/day Tue-Wed. 4x/day Thu. 8x/day Sun. 
* **Timestamping:** Writes pulse times to ction_grid.db. UI reads these to display ⏱️ Data Xm old badges.

### 3. The State Bus (pp.py & ddress_book.py)
* pp.py is a clean dispatcher with isolated 	ry/except blocks for all 10 tabs.
* st.session_state manages independent toggles: dfs_engine_slate, dfs_lab_slate, ankings_slate, parlay_slate, prizepicks_slate.

## 🚀 IMMEDIATE UPGRADE TASKS FOR THIS SESSION
Execute these upgrades in your code blocks:

**1. DFS Engine (Tab 1) - The "Lineup Compiler":** 
Rebuild into an interactive workspace. Left side is a sortable glassmorphic pool of individual player cards (Top 300). Right side is a visual lineup builder. Add a **"Fantastic Four" toggle** that automatically queries data_service.py and auto-fills the four optimal mathematical anchors for the selected slate (Showdown vs. Classic).

**2. The Rankings (Tab 3) - Infinite Scroll & Massive Cards:** 
Remove the Top 300 table. Convert the left panel into a continuous, scrollable vertical feed of high-density asset cards matching the table's width. Expand the Showdown & Recon cards on the right panel to utilize full screen real estate, making Donna's reads and injury gradients highly visible.

**3. Parlay Mix & PrizePicks (Tabs 4 & 6) - Platform Math Weighting:** 
* **PrizePicks:** Enforce compliant 2-to-6 pick slips mapped to the 54.6% break-even math. Slips *must* span at least 2 teams.
* **Underdog:** Scale slips up to 8 picks mapped to the 54.9% break-even math.
* **DraftKings Parlays:** Procedurally generate 2-leg to 10-leg tickets. Weight small tickets with correlated game scripts (QB + WR1 + Opp Runback) and massive 8-10 leg tickets with uncorrelated floor anchors. 
* **Timestamps:** Apply ⏱️ Data Xm old freshness badges to all generated slips based on system_status DB reads.
