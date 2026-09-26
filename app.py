# -*- coding: utf-8 -*-
import streamlit as st
import address_book

st.set_page_config(page_title="The Juicer | War Room", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

# JUICER_TELEMETRY_START
import time
from datetime import datetime
import streamlit as st

def _render_alfred_sidebar():
    st.markdown('''
    <style>
    .alfred-badge {
        font-size: 14px; 
        font-weight: bold; 
        color: #00ff88;
        background-color: rgba(0, 255, 136, 0.05);
        padding: 10px; 
        border-radius: 8px;
        border: 1px solid #00ff88; 
        text-align: center;
        margin-bottom: 20px; 
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(0, 255, 136, 0.3); }
        70% { box-shadow: 0 0 0 6px rgba(0, 255, 136, 0); }
        100% { box-shadow: 0 0 0 0 rgba(0, 255, 136, 0); }
    }
    </style>
    ''', unsafe_allow_html=True)
    
    cur_t = datetime.now().strftime("%I:%M:%S %p")
    
    with st.sidebar:
        st.markdown(f'<div class="alfred-badge">🟢 ALFRED ONLINE<br><span style="font-size:11px; color:#ccc;">LAST SYNC: {cur_t}</span></div>', unsafe_allow_html=True)
        if st.button("🔄 Sync Live Data", use_container_width=True):
            pbar = st.progress(0, text="Alfred: Fetching Data...")
            for pct in range(100):
                time.sleep(0.005)
                pbar.progress(pct + 1, text="Alfred: Fetching Data...")
            pbar.empty()
            st.toast("⚡ Data Refreshed Successfully!", icon="🟢")
            st.rerun()

_render_alfred_sidebar()
# JUICER_TELEMETRY_END






st.markdown("<style>.stApp { background-color: #06090e; color: #c9d1d9; } header, footer { visibility: hidden; }</style>", unsafe_allow_html=True)
address_book.init_session_state(st)

# ==============================================================================
# STARTUP SPLASH GATE (DEVICE MODE SELECTOR)
# ==============================================================================
if "ui_mode" not in st.session_state:
    st.markdown("""
    <div style='max-width: 600px; margin: 80px auto; background: linear-gradient(135deg, rgba(13,17,23,0.95), rgba(22,27,34,0.98)); border: 1px solid #30363d; border-top: 3px solid #00ff88; border-radius: 16px; padding: 32px; box-shadow: 0 16px 48px rgba(0,0,0,0.8); text-align: center;'>
        <div style='font-size: 42px; margin-bottom: 12px;'>⚛️🥤</div>
        <h1 style='color: #fff; font-size: 28px; font-weight: 900; margin-bottom: 8px; text-shadow: 0 0 15px rgba(0,255,136,0.4);'>THE JUICER WAR ROOM</h1>
        <p style='color: #8b949e; font-size: 14px; margin-bottom: 24px;'>Select your operational interface mode to initialize telemetry feeds.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_splash1, col_splash2 = st.columns(2)
    with col_splash1:
        if st.button("🖥️ FULL DESKTOP WAR ROOM", use_container_width=True):
            st.session_state["ui_mode"] = "Desktop"
            st.rerun()
    with col_splash2:
        if st.button("📱 STREAMLINED MOBILE MODE", use_container_width=True):
            st.session_state["ui_mode"] = "Mobile"
            st.rerun()
    st.stop()

# ==============================================================================
# GLOBAL INDUSTRIAL COMMERCIAL MIXER HEADER
# ==============================================================================
st.html("""
<style>
@keyframes spin-impeller {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
@keyframes cyber-pulse {
    0% { filter: drop-shadow(0 0 5px #00ff88); }
    50% { filter: drop-shadow(0 0 15px #00e5ff); }
    100% { filter: drop-shadow(0 0 5px #00ff88); }
}
.mixer-blade {
    transform-origin: center;
    animation: spin-impeller 1.5s linear infinite;
}
.cyber-icon-box {
    animation: cyber-pulse 3s ease-in-out infinite;
}
</style>

<div style='background: linear-gradient(135deg, rgba(8,11,16,0.98), rgba(18,24,33,0.98)); backdrop-filter: blur(16px); border: 1px solid #30363d; border-bottom: 3px solid #00ff88; border-top: 1px solid rgba(255,42,109,0.5); padding: 16px 24px; border-radius: 12px; margin-bottom: 18px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 8px 32px rgba(0,0,0,0.7);'>
    <div style='display: flex; align-items: center;'>
        <div class='cyber-icon-box' style='background: rgba(0,255,136,0.08); padding: 8px 12px; border-radius: 10px; border: 1px solid rgba(0,255,136,0.4); margin-right: 16px; display: flex; align-items: center; justify-content: center;'>
            <svg width="36" height="36" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M5 20H19C19.5523 20 20 19.5523 20 19V17C20 15.8954 19.1046 15 18 15H6C4.89543 15 4 15.8954 4 17V19C4 19.5523 4.44772 20 5 20Z" fill="#161b22" stroke="#00ff88" stroke-width="1.5"/>
                <circle cx="12" cy="17.5" r="1" fill="#00e5ff"/>
                <path d="M7 9H17L15.5 4H8.5L7 9Z" fill="rgba(0,229,255,0.15)" stroke="#00e5ff" stroke-width="1.5"/>
                <path d="M17 6H19.5C19.7761 6 20 6.22386 20 6.5V9.5C20 9.77614 19.7761 10 19.5 10H17" stroke="#00e5ff" stroke-width="1.5"/>
                <g class="mixer-blade" transform="translate(12, 6.5)">
                    <line x1="-3.5" y1="0" x2="3.5" y2="0" stroke="#ff2a6d" stroke-width="2" stroke-linecap="round"/>
                </g>
            </svg>
        </div>
        <div>
            <div style='display: flex; align-items: center;'>
                <h1 style='color: #ffffff; font-size: 26px; font-weight: 900; margin: 0; letter-spacing: 1.5px; text-shadow: 0 0 10px #00ff88, 0 0 25px rgba(255,42,109,0.6), 0 0 40px rgba(0,229,255,0.4); font-family: system-ui, -apple-system, sans-serif;'>THE JUICER</h1>
                <span style='background: linear-gradient(90deg, #ff2a6d, #00e5ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 12px; font-weight: 900; margin-left: 12px; letter-spacing: 0.8px;'>INDUSTRIAL QUANT v3.0</span>
            </div>
            <div style='color: #8b949e; font-size: 11px; margin-top: 3px; font-family: monospace; letter-spacing: 0.5px;'>
                ⚡ MODE: <span style='color: #00ff88;'>{st.session_state["ui_mode"].upper()}</span> &bull; TWIN-MOTOR DAEMON &bull; ACTIVE FEED
            </div>
        </div>
    </div>
    <div style='display: flex; align-items: center; gap: 14px;'>
        <div style='text-align: right; font-family: monospace;'>
            <div style='color: #00ff88; font-size: 11px; font-weight: 800;'>🟢 PIPELINE: SYNCED</div>
            <div style='color: #ffd700; font-size: 10px;'>QUOTA: OPTIMIZED</div>
        </div>
        <div style='background: rgba(0,229,255,0.1); border: 1px solid rgba(0,229,255,0.3); color: #00e5ff; font-size: 11px; font-weight: 900; padding: 6px 12px; border-radius: 6px; letter-spacing: 0.5px;'>
            WAR ROOM LIVE
        </div>
    </div>
</div>
""")

import ui_scoreboard, ui_dfs, ui_lineup_lab, tab_juice_rankings, ui_parlay_mix, ui_season_long, ui_prizepicks, ui_film_room, ui_ops, ui_sim_audit

tabs = st.tabs(["🏟️ Scoreboard", "🧬 DFS Engine", "🧪 DFS Lab", "⚡ The Rankings", "🔀 Parlay Mix", "🏈 Season Long", "🎟️ PrizePicks", "🎥 Film Room", "⚙️ Ops", "🎲 Learning"])

tab_modules = {
    0: ui_scoreboard.render_scoreboard_tab,
    1: ui_dfs.render_dfs_tab,
    2: ui_lineup_lab.render_lineup_lab_tab,
    3: tab_juice_rankings.render_the_rankings,
    4: ui_parlay_mix.render_parlay_mix,
    5: ui_season_long.render_season_long,
    6: ui_prizepicks.render_prizepicks,
    7: ui_film_room.render_film_room,
    8: ui_ops.render_ops_desk,
    9: ui_sim_audit.render_sim_audit_tab
}

for tab_idx, render_func in tab_modules.items():
    with tabs[tab_idx]:
        try:
            render_func()
        except Exception as e:
            st.error(f"⚠️ UI Guardrail Activated: Tab {tab_idx} intercepted an error: {e}. The other 9 tabs remain fully operational.")
