import sqlite3, pandas as pd, streamlit as st
import ui_components as ui

DB_FILE, SIM_FILE, KEEPER_FILE = "action_grid.db", "dfs_sim_curve.json", "keepers.csv"
st.set_page_config(page_title="The Juicer - Master War Room", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0b0914; color: #f0f2f6; }
    .juicer-header { text-align: center; margin-bottom: 4px; display: flex; flex-direction: column; align-items: center; }
    .blender-svg { width: 58px; height: 58px; margin-bottom: 0px; }
    .blender-blade { animation: spin-blade 1.0s linear infinite; transform-origin: 50px 70px; }
    @keyframes spin-blade { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    .liquid-wave { animation: liquid-color 2.5s ease-in-out infinite alternate; }
    @keyframes liquid-color { 0% { fill: #ff2a6d; filter: drop-shadow(0 0 10px #ff2a6d); } 50% { fill: #00e5ff; filter: drop-shadow(0 0 12px #00e5ff); } 100% { fill: #00ff88; filter: drop-shadow(0 0 10px #00ff88); } }
    .juicer-title { font-size: 2.2rem; font-weight: 900; letter-spacing: 5px; color: #fff; text-shadow: 0 0 20px #ff2a6d; margin: 0; }
    .ticker-wrap { width: 100%; overflow: hidden; white-space: nowrap; padding: 3px 0; margin-bottom: 3px; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.5px; border-radius: 4px; }
    .ticker-move { display: inline-block; animation: ticker-kf 30s linear infinite; }
    @keyframes ticker-kf { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-50%, 0, 0); } }
    .tick-1 { background: #071e16; border-top: 1px solid #00ff8855; border-bottom: 1px solid #00ff8855; color: #00ff88; }
    .tick-2 { background: #061826; border-top: 1px solid #00e5ff55; border-bottom: 1px solid #00e5ff55; color: #00e5ff; }
    .tick-3 { background: #240816; border-top: 1px solid #ff2a6d55; border-bottom: 1px solid #ff2a6d55; color: #ff2a6d; margin-bottom: 10px; }
    .credit-badge { background: #1e1333; border: 1px solid #00e5ff; color: #00e5ff; border-radius: 14px; padding: 2px 10px; font-size: 0.72rem; margin-left: 8px; }
    div[data-baseweb="tab-list"] { justify-content: center; gap: 8px; }
    button[data-baseweb="tab"][aria-selected="true"] { background-color: #ff2a6d; color: white !important; font-weight: bold; }
</style>

<div class="juicer-header">
    <svg class="blender-svg" viewBox="0 0 100 100">
        <polygon points="30,18 70,18 63,73 37,73" fill="#130f24" stroke="#00e5ff" stroke-width="2.5" />
        <polygon points="32,32 68,32 62,72 38,72" class="liquid-wave" opacity="0.85" />
        <rect x="34" y="74" width="32" height="15" fill="#2a224a" stroke="#ff2a6d" stroke-width="2" rx="3" />
        <g class="blender-blade">
            <line x1="42" y1="70" x2="58" y2="70" stroke="#fff" stroke-width="2.5" stroke-linecap="round" />
            <line x1="50" y1="62" x2="50" y2="78" stroke="#fff" stroke-width="2.5" stroke-linecap="round" />
        </g>
    </svg>
    <div class="juicer-title">THE JUICER</div>
</div>
""", unsafe_allow_html=True)

c_left, c_right = st.columns([2, 1])
with c_right:
    master_slate = st.selectbox("🌐 MASTER COMMAND SLATE:", ["Prime-Time Showdowns (TNF/MNF)", "Sunday Main Slate (Classic 9-Man)", "Full Week Multi-Slate View"])

# RESTORED 3-TIER TICKER SYSTEM
st.markdown("""
<style>
    .ticker-wrap { width: 100%; overflow: hidden; white-space: nowrap; padding: 3px 0; margin-bottom: 3px; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.5px; border-radius: 4px; }
    .ticker-move { display: inline-block; animation: ticker-kf 30s linear infinite; }
    @keyframes ticker-kf { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-50%, 0, 0); } }
    .tick-1 { background: #071e16; border-top: 1px solid #00ff8855; border-bottom: 1px solid #00ff8855; color: #00ff88; }
    .tick-2 { background: #061826; border-top: 1px solid #00e5ff55; border-bottom: 1px solid #00e5ff55; color: #00e5ff; }
    .tick-3 { background: #240816; border-top: 1px solid #ff2a6d55; border-bottom: 1px solid #ff2a6d55; color: #ff2a6d; }
    .tick-4 { background: #1c102a; border-top: 1px solid #bb88ff55; border-bottom: 1px solid #bb88ff55; color: #bb88ff; margin-bottom: 10px; }
</style>
<div class="ticker-wrap tick-1">
    <div class="ticker-move">
        🏈 [MULTI-BOOK AUDIT] DK, FD, MGM, CZR Live &nbsp;&nbsp;●&nbsp;&nbsp; 🦁 DET @ BUF FINALIZED & PURGED &nbsp;&nbsp;●&nbsp;&nbsp; ⚡ PRIZEPICKS & UNDERDOG PROPS ACTIVE &nbsp;&nbsp;●&nbsp;&nbsp; 🏈 [MULTI-BOOK AUDIT] Live
    </div>
</div>
<div class="ticker-wrap tick-2">
    <div class="ticker-move">
        📊 [SHARP MARKET FEED] Line Movement Detected: DAL -2.5 to -3.0 &nbsp;&nbsp;●&nbsp;&nbsp; Total ticking up in DEN vs WAS &nbsp;&nbsp;●&nbsp;&nbsp; 📊 [SHARP MARKET FEED] Active
    </div>
</div>
<div class="ticker-wrap tick-3">
    <div class="ticker-move">
        🚨 [PRIORITY SYNDICATE ALERT] Henderson's AI Bankroll Up +42.4% &nbsp;&nbsp;●&nbsp;&nbsp; 200 Clean Sunday Parlays Locked &nbsp;&nbsp;●&nbsp;&nbsp; 🚨 [PRIORITY ALERT] Live
    </div>
</div>
<div class="ticker-wrap tick-4">
    <div class="ticker-move">
        🤖 [LEWIS WATCHDOG & SLEEPER FEED] Watchdog Daemon: NORMAL &nbsp;&nbsp;●&nbsp;&nbsp; Wastewater Redundancy: STANDBY READY &nbsp;&nbsp;●&nbsp;&nbsp; Intern Brigade: ACTIVE &nbsp;&nbsp;●&nbsp;&nbsp; 🤖 [LEWIS SYNC] Live
    </div>
</div>
""", unsafe_allow_html=True)

def q_db(q):
    try:
        with sqlite3.connect(DB_FILE) as conn: return pd.read_sql_query(q, conn)
    except Exception: return pd.DataFrame()

ui.render_telemetry(q_db)

t1, t2, t3, t4, t5, t6 = st.tabs(["🏆 Vegas Scoreboard", "👑 DFS Optimizer", "📊 Classy Rankings", "🎯 Parlay Matrix", "🏈 Season-Long Fantasy", "⚡ PrizePicks & Underdog"])

with t1:
    ui.render_vegas_wall()
with t2:
    ui.render_dfs(q_db, SIM_FILE)
with t3:
    ui.render_rankings_syndicate(q_db)
with t4:
    ui.render_parlays(q_db)
with t5:
    ui.render_season_long(KEEPER_FILE)
with t6:
    ui.render_prizepicks_underdog()
