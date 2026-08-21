import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder

# --- ELITE CONFIGURATION ---
st.set_page_config(page_title="The Juicer | Ruby Crew VIP", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM RUBY CREW CSS INJECTION ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@700&family=Inter:wght@400;600;800&display=swap');
    
    /* Core App Theme: Deep Black & Charcoal */
    .stApp { background-color: #050505; color: #e2e8f0; font-family: 'Inter', sans-serif; }
    
    /* Sidebar: Premium Dark Grey */
    [data-testid="stSidebar"] {
        background-color: #0f0f13 !important;
        border-right: 1px solid #2a2a35;
    }
    
    /* Neon Maroon Headers */
    h1, h2, h3 {
        font-family: 'Syncopate', sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .neon-title {
        color: #ffffff;
        text-shadow: 0 0 10px #800000, 0 0 20px #5c0000;
        margin-bottom: 0.5rem;
    }
    
    /* Professional HUD Modules */
    .hud-module {
        background: linear-gradient(145deg, #121217 0%, #0a0a0d 100%);
        border: 1px solid #331515;
        border-left: 4px solid #800000;
        padding: 25px;
        border-radius: 4px;
        box-shadow: 0 8px 32px 0 rgba(128, 0, 0, 0.15);
        margin-bottom: 20px;
        transition: transform 0.2s ease;
    }
    .hud-module:hover { transform: translateY(-2px); border-left: 4px solid #ff1a1a; }
    
    /* Metric Typography */
    .hud-label { color: #8a8a9e; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
    .hud-value { color: #ffffff; font-size: 2.5rem; font-weight: 800; line-height: 1.2; }
    .hud-accent { color: #800000; }
    
    /* Terminal Console */
    .terminal-box {
        background-color: #000000;
        border: 1px solid #333;
        padding: 15px;
        font-family: 'Courier New', monospace;
        color: #a0aec0;
        font-size: 0.9rem;
        border-radius: 4px;
    }
    .terminal-maroon { color: #ff4d4d; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- VIP SIDEBAR ---
st.sidebar.markdown('<h1 style="color:#800000; font-size: 2rem; margin-bottom: 0;">THE JUICER</h1>', unsafe_allow_html=True)
st.sidebar.markdown('<p style="color:#8a8a9e; font-size: 0.9rem; margin-top: 0; letter-spacing: 1px;">QUANTITATIVE DFS ENGINE</p>', unsafe_allow_html=True)
st.sidebar.markdown('---')

st.sidebar.radio("COMMAND PROTOCOLS", [
    "⚡ Live Edge Matrix",
    "🎯 Draft War Room",
    "📈 Vegas Odds Tracker",
    "⚙️ Model Parameters"
])

st.sidebar.markdown('---')
st.sidebar.markdown("""
<div style="background: #121217; border: 1px solid #2a2a35; padding: 15px; border-radius: 4px; text-align: center;">
    <p style="color:#800000; font-family:'Syncopate', sans-serif; font-size:0.9rem; margin-bottom:5px;">RUBY CREW ACCESS</p>
    <p style="color:#a0aec0; font-size:0.75rem; margin:0;">Status: VERIFIED VIP</p>
    <p style="color:#a0aec0; font-size:0.75rem; margin:0;">Override Auth: AbbySlayz</p>
</div>
""", unsafe_allow_html=True)

# --- MAIN DASHBOARD ---
st.markdown('<h1 class="neon-title">TACTICAL DASHBOARD</h1>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="hud-module">
        <div class="hud-label">Slate Optimization</div>
        <div class="hud-value hud-accent">ACTIVE</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="hud-module">
        <div class="hud-label">Expected Value Threshold</div>
        <div class="hud-value">+14.2%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="hud-module">
        <div class="hud-label">System Security</div>
        <div class="hud-value" style="color: #4ade80;">SECURE</div>
    </div>
    """, unsafe_allow_html=True)

# --- TERMINAL OVERRIDE ---
st.markdown("""
<div class="terminal-box">
    > INITIATING STARTUP SEQUENCE...<br>
    > BYPASSING STANDARD PROTOCOLS...<br>
    > <span class="terminal-maroon">ABBYSLAYZ MANDATE RECOGNIZED. ENFORCING MAXIMUM YIELD.</span><br>
    > LOADING EDGE MATRIX... DONE.
</div>
<br>
""", unsafe_allow_html=True)

# --- THE ACTION GRID ---
@st.cache_data
def load_elite_data():
    return pd.DataFrame({
        "Asset": ["Kenneth Walker", "Breece Hall", "Amon-Ra St. Brown", "Justin Herbert"],
        "Exposure": ["25%", "15%", "30%", "10%"],
        "Vegas Line": ["65.5", "75.5", "82.5", "245.5"],
        "Model Proj": ["74.2", "70.1", "91.0", "260.0"],
        "Calculated Edge": ["+14.2%", "-4.1%", "+18.3%", "+8.5%"],
        "Action": ["LOCK", "FADE", "LOCK", "PLAY"]
    })

df = load_elite_data()

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_selection('multiple', use_checkbox=True)
gb.configure_default_column(flex=1, minWidth=120)
gridOptions = gb.build()

st.markdown('<h3 style="color:#e2e8f0; font-family:Inter; font-size:1.2rem;">PROBABILITY MATRIX</h3>', unsafe_allow_html=True)

AgGrid(
    df,
    gridOptions=gridOptions,
    theme='alpine-dark', 
    fit_columns_on_grid_load=True,
    height=300
)
