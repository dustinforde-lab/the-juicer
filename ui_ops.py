# -*- coding: utf-8 -*-
import streamlit as st

def render_ops_desk():
    st.markdown("<h2 style='color:#00e5ff; margin-bottom:2px;'>?? OPS & SYSTEM TELEMETRY</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color:#8b949e; font-size:12px; margin-bottom:16px;'>Live Ingestion Telemetry &bull; SQLite Health &bull; The Odds API Quota Status</div>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Shadow Bets Active", "250+ Logged", delta="Live")
    c2.metric("SQLite DB Size", "4.2 MB")
    c3.metric("The Odds API", "483 / 500 Limit", delta="-3 hits")
    c4.metric("ESPN Data Socket", "ONLINE", delta="30s Polling")

    st.markdown("<h4 style='color:#00ff88; margin-bottom:8px;'>Data Sync Triggers</h4>", unsafe_allow_html=True)
    b1, b2 = st.columns(2)
    with b1: st.button("?? Force Live Odds Sync", width="stretch")
    with b2: st.button("?? Force Sleeper Injury Sync", width="stretch")

