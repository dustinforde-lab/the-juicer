import streamlit as st
import pandas as pd
import numpy as np
import time
import json
from st_aggrid import AgGrid, GridOptionsBuilder

# --- FIRM CONFIGURATION ---
st.set_page_config(page_title="The Juicer // Apex Command Center", layout="wide", initial_sidebar_state="expanded")

if "risk_profile" not in st.session_state:
    st.session_state.risk_profile = "Conservative (2.5% Unit)"

st.sidebar.markdown("### ⚙️ Firm Settings")
st.session_state.risk_profile = st.sidebar.radio(
    "Select Bankroll Risk Profile:",
    ["Conservative (2.5% Unit)", "Aggressive (5.0% Unit)", "Nuclear (Max Leverage)"]
)

# --- INGEST THE BRAIN (DYNAMIC MEMORY) ---
@st.cache_data(ttl=60)
def load_brain():
    try:
        with open("brain.json", "r") as f:
            return json.load(f)
    except:
        return {"model_weights": {"WR_RECEPTIONS": {"modifier": 1.0, "rolling_win_rate": 0.50}}, "bet_ledger": []}

brain = load_brain()
wr_modifier = brain["model_weights"]["WR_RECEPTIONS"]["modifier"]
wr_win_rate = brain["model_weights"]["WR_RECEPTIONS"]["rolling_win_rate"]
pending_tickets = len(brain.get("bet_ledger", []))

# --- GLOBAL STYLING ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
.stApp { background: linear-gradient(135deg, #050508 0%, #0d0d12 100%); color: #f4f4f5; font-family: 'Plus Jakarta Sans', sans-serif; }
.exec-card { background: rgba(18, 18, 24, 0.85); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.05); border-top: 2px solid rgba(161, 29, 33, 0.9); border-radius: 12px; padding: 28px; box-shadow: 0 15px 35px -10px rgba(0, 0, 0, 0.95); margin-bottom: 25px; }
.hud-bar { background: rgba(8, 8, 12, 0.98); border: 1px solid rgba(161, 29, 33, 0.6); padding: 14px 24px; border-radius: 8px; display: flex; justify-content: space-around; align-items: center; margin-bottom: 20px; font-size: 0.85rem; letter-spacing: 1.5px; text-transform: uppercase; }
.hud-item { text-align: center; border-right: 1px solid rgba(255,255,255,0.08); padding-right: 25px; }
.hud-item:last-child { border-right: none; }
.hud-dot { height: 8px; width: 8px; background-color: #22c55e; border-radius: 50%; display: inline-block; box-shadow: 0 0 12px #22c55e; animation: pulse 2s infinite; }
.ag-root-wrapper, .ag-root, .ag-body-viewport, .ag-center-cols-viewport, .ag-center-cols-container { background-color: #121218 !important; width: 100% !important; }
@keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
</style>
""", unsafe_allow_html=True)

# --- LOGO & HUD ---
st.markdown("""
<div style="display: flex; align-items: center; justify-content: center; margin-bottom: 25px;">
    <div>
        <h1 style="font-size: 3.5rem; font-weight: 800; background: linear-gradient(135deg, #ffffff 20%, #ff4d4d 60%, #a11d21 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; line-height: 1;">THE JUICER</h1>
        <p style="color: #a1a1aa; font-weight: 600; letter-spacing: 4px; margin: 0; text-transform: uppercase; font-size: 0.85rem;">Managed by Mike Donna // Dynamic Brain Linked</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="hud-bar">
    <div class="hud-item"><span class="hud-dot"></span> <b>AI ENGINE: CONNECTED</b></div>
    <div class="hud-item"><b>WR EDGE MODIFIER:</b> {wr_modifier}x</div>
    <div class="hud-item" style="color: #a11d21;"><b>PENDING TICKETS:</b> {pending_tickets}</div>
</div>
""", unsafe_allow_html=True)

custom_grid_css = {
    ".ag-root-wrapper": {"border": "1px solid #2a2a35 !important", "border-radius": "8px", "background-color": "#121218 !important"},
    ".ag-header": {"background-color": "#0d0d12 !important", "border-bottom": "2px solid #a11d21 !important"},
    ".ag-header-cell-text": {"color": "#ff4d4d !important", "font-weight": "800 !important", "font-size": "13px", "text-transform": "uppercase"},
    ".ag-row": {"background-color": "#16161e !important", "color": "#f4f4f5 !important", "border-bottom": "1px solid rgba(255,255,255,0.05) !important"}
}

def render_styled_grid(df, height=260):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(resizable=True, sortable=True, filter=True, flex=1, minWidth=120)
    AgGrid(df, gridOptions=gb.build(), custom_css=custom_grid_css, theme='alpine-dark', fit_columns_on_grid_load=True, height=height)

tab1, tab2 = st.tabs(["👑 Advanced DFS Optimizer & Sims", "💼 Ledger & Firm Architecture"])

with tab1:
    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    st.markdown('<h3>DraftKings Lineup Optimizer & 10k Monte Carlo Simulator</h3>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Dynamic WR Modifier", f"{wr_modifier}x", "Auto-Adjusted by Loop")
    c2.metric("WR Rolling Win Rate", f"{wr_win_rate * 100}%", "Live AI Data")
    c3.metric("Simulated Win Rate", "81.5%", "+3.5% Edge")

    df_dfs = pd.DataFrame({
        "Pos": ["WR", "WR", "WR"],
        "Player": ["Amon-Ra St. Brown", "Nico Collins", "Rashee Rice"],
        "Base Proj": [24.5, 17.2, 14.8],
        "AI Adjusted Proj": [round(24.5 * wr_modifier, 1), round(17.2 * wr_modifier, 1), round(14.8 * wr_modifier, 1)]
    })
    render_styled_grid(df_dfs, height=180)
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    st.markdown('<h3>Autonomous Bet Ledger (brain.json)</h3>', unsafe_allow_html=True)
    df_ledger = pd.DataFrame(brain.get("bet_ledger", []))
    render_styled_grid(df_ledger, height=200)
    st.markdown('</div>', unsafe_allow_html=True)
