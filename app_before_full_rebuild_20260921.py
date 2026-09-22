import streamlit as st
import sqlite3
import pandas as pd
import config
import ui_addresses
import ui_components as ui
from scheduler import JobScheduler, thread_safe_log_fn
import learning_loop
import os

st.set_page_config(
    page_title="The Juicer - Pro Syndicate Engine",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DB_PATH = getattr(config, 'DB_PATH', 'action_grid.db')

# Optional & Guarded Background Scheduler Setup (Per Handoff Spec)
@st.cache_resource
def init_optional_syndicate_scheduler():
    try:
        log_fn = thread_safe_log_fn(DB_PATH)
        sched = JobScheduler(log_fn=log_fn)
        if hasattr(learning_loop, 'recalibrate_weights'):
            sched.register_job(
                "bayesian_recalibration",
                learning_loop.recalibrate_weights,
                interval_seconds=86400,
                run_at_start=False,
            )
        sched.start()
        return True
    except Exception as e:
        print(f"Scheduler initialization notice (UI remains fully operational): {e}")
        return False

init_optional_syndicate_scheduler()

# Master UI Routing & Modular Component Fallback
try:
    if hasattr(ui_addresses, 'run_router'):
        ui_addresses.run_router()
    elif hasattr(ui, 'main'):
        ui.main()
    elif hasattr(ui, 'render_war_room'):
        ui.render_war_room()
    else:
        # Robust multi-tab fallback matching the 9 War Room views
        if hasattr(ui, 'inject_elite_aesthetic'):
            ui.inject_elite_aesthetic()
        if hasattr(ui, 'render_accountability_tickers'):
            ui.render_accountability_tickers()
            
        tabs = st.tabs([
            "🏆 Scoreboard", 
            "👑 DFS Engine", 
            "📊 Donna's Leverage", 
            "🎯 Parlay Matrix", 
            "🏈 Season-Long", 
            "⚡ PrizePicks", 
            "🎥 Film Room", 
            "⚙️ Ops Center", 
            "🤖 Learning Loop"
        ])
        
        with tabs[0]: 
            if hasattr(ui, 'render_vegas_wall'): ui.render_vegas_wall()
        with tabs[1]: 
            if hasattr(ui, 'render_dfs_engine'): ui.render_dfs_engine()
        with tabs[2]: 
            if hasattr(ui, 'render_donna_matrix'): ui.render_donna_matrix()
        with tabs[3]: 
            if hasattr(ui, 'render_real_parlay_matrix'): ui.render_real_parlay_matrix()
        with tabs[4]: 
            if hasattr(ui, 'render_season_long'): ui.render_season_long()
        with tabs[5]: 
            if hasattr(ui, 'render_prizepicks_underdog'): ui.render_prizepicks_underdog()
        with tabs[6]: 
            if hasattr(ui, 'render_film_room'): ui.render_film_room()
        with tabs[7]: 
            if hasattr(ui, 'render_ops_center'): ui.render_ops_center()
        with tabs[8]: 
            if hasattr(ui, 'render_learning_loop'): ui.render_learning_loop()
            elif hasattr(ui, 'render_learning_panel'): ui.render_learning_panel()

except Exception as e:
    st.error(f"⚠️ War Room Render Exception: {e}")
    import traceback
    st.code(traceback.format_exc())