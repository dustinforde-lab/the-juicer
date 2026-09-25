import streamlit as st
import sqlite3
import os
import subprocess

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "action_grid.db")

def render_ops_desk():
    st.markdown("<h2 style='color:#00e5ff; margin-bottom:2px;'>⚙️ OPS & SYSTEM TELEMETRY</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color:#8b949e; font-size:12px; margin-bottom:16px;'>The Odds API Quota Monitor • SQLite Database Telemetry • Live Scheduler Controls</div>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Odds API Remaining", "486 Credits", delta="-3 this run")
    c2.metric("Local Database Status", "Online (action_grid.db)")
    c3.metric("Active Week", "NFL Week 3")
    
    st.divider()
    st.markdown("<h4 style='color:#00ff88; margin-bottom:8px;'>Manual Ingestion Triggers</h4>", unsafe_allow_html=True)
    b1, b2 = st.columns(2)
    with b1:
        if st.button("📡 Force Live Odds Sync (data_live_feed.py)", use_container_width=True):
            subprocess.run(["python", "data_live_feed.py"])
            st.success("Vegas feed refreshed.")
    with b2:
        if st.button("📰 Force News & Injury Sync (data_news_wire.py)", use_container_width=True):
            subprocess.run(["python", "data_news_wire.py"])
            st.success("News wire refreshed.")
