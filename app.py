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
    page_title="The Juicer - Pro Syndicate War Room",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DB_PATH = getattr(config, 'DB_PATH', 'action_grid.db')

# Optional & Guarded Background Scheduler Setup
@st.cache_resource
def init_syndicate_scheduler():
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
        return False

init_syndicate_scheduler()

# Apply Custom CSS & Elite Aesthetics
if hasattr(ui, 'inject_elite_aesthetic'):
    ui.inject_elite_aesthetic()

# Render Multi-Book & Accountability Tickers
if hasattr(ui, 'render_accountability_tickers'):
    ui.render_accountability_tickers()

# Master Command Slate Header & Controls (Matching Screenshots)
col_title, col_slate = st.columns([0.6, 0.4])
with col_title:
    st.markdown("<h1 style='text-align: center; color: #ff3366; font-weight: 900; letter-spacing: 2px; margin: 0;'>THE JUICER</h1>", unsafe_allow_html=True)
with col_slate:
    selected_slate = st.selectbox(
        "MASTER COMMAND SLATE:",
        ["Sunday Main Slate (Classic 9-Man)", "Thursday Night Showdown", "Monday Night Football SGP", "Full Slate DFS Pool"],
        key="master_command_slate_dropdown"
    )

st.markdown("---")

# Full 9-Tab War Room Architecture mapped to native ui_components functions
try:
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
        if hasattr(ui, 'render_vegas_wall'):
            ui.render_vegas_wall()
        else:
            st.info("Scoreboard feed initializing...")

    with tabs[1]:
        if hasattr(ui, 'render_dfs_engine'):
            ui.render_dfs_engine()
        elif hasattr(ui, 'render_dfs'):
            ui.render_dfs()

    with tabs[2]:
        if hasattr(ui, 'render_donna_matrix'):
            ui.render_donna_matrix()
        else:
            st.info("Donna's leverage matrix loading...")

    with tabs[3]:
        if hasattr(ui, 'render_real_parlay_matrix'):
            ui.render_real_parlay_matrix()
        else:
            st.info("Parlay matrix loading...")

    with tabs[4]:
        if hasattr(ui, 'render_season_long'):
            ui.render_season_long()
        else:
            st.info("Season-long rosters loading...")

    with tabs[5]:
        if hasattr(ui, 'render_prizepicks_underdog'):
            ui.render_prizepicks_underdog()
        elif hasattr(ui, 'render_pickem_slips'):
            ui.render_pickem_slips()

    with tabs[6]:
        if hasattr(ui, 'render_film_room'):
            ui.render_film_room()
        else:
            st.info("Film room telemetry loading...")

    with tabs[7]:
        if hasattr(ui, 'render_ops_center'):
            ui.render_ops_center()
        elif hasattr(ui, 'render_telemetry'):
            ui.render_telemetry()

    with tabs[8]:
        if hasattr(ui, 'render_learning_loop'):
            ui.render_learning_loop()
        elif hasattr(ui, 'render_learning_panel'):
            ui.render_learning_panel()

except Exception as e:
    st.error(f"⚠️ War Room Render Exception: {e}")
    import traceback
    st.code(traceback.format_exc())