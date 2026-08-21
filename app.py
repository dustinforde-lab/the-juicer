import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# --- PAGE CONFIG & SPORTS CAR STYLING ---
st.set_page_config(page_title="The Juicer v2.0", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .stApp { background-color: #0a0a0f; color: #f0f2f6; }
    .neon-card {
        background: linear-gradient(135deg, #131b2f 0%, #0b101a 100%);
        border: 1px solid #2d3748; padding: 20px; border-radius: 12px;
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.3); margin-bottom: 16px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white; border: none; border-radius: 8px; font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR COMMAND CENTER ---
st.sidebar.title("🍹 The Juicer")
st.sidebar.markdown("### Autonomous Quant Engine")

menu = st.sidebar.radio("Navigation", [
    "🏆 Live Draft War Room", 
    "📚 The Repo Library", 
    "📈 Sharp Money & Scoreboard", 
    "🤖 Trade Assassin & Learning Engine"
])

# --- DATA ENGINE (VFD-Style ROI & Keepers) ---
@st.cache_data
def load_engine_data():
    try:
        return pd.read_csv("keepers.csv")
    except Exception:
        return pd.DataFrame({
            "Player": ["Kenneth Walker", "Derrick Henry", "Breece Hall", "Amon-Ra St. Brown"],
            "Tier": ["Tier 2", "Tier 2", "Tier 1", "Tier 1"],
            "Status": ["Keeper", "Keeper", "Draft", "Draft"],
            "Projected Pts": [245.5, 230.1, 290.4, 275.8],
            "Draft Cost ($)": [15, 18, 55, 50],
            "VFD-ROI Yield": ["16.3 pts/$", "12.7 pts/$", "5.2 pts/$", "5.5 pts/$"] 
        })

df = load_engine_data()

# --- MODULE 1: LIVE DRAFT WAR ROOM ---
if menu == "🏆 Live Draft War Room":
    st.title("Live Draft War Room")
    st.markdown("### 12-Team Keeper Optimizer Active")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="neon-card"><h4>Tier Scarcity Alert</h4><h2 style="color:#ef4444;">RB Tier 2 Depleting</h2></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="neon-card"><h4>Beat Writer Sentiment</h4><h2 style="color:#10b981;">Trending UP 📈</h2></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="neon-card"><h4>Highest ROI on Board</h4><h2 style="color:#3b82f6;">K. Walker (16.3/$)</h2></div>', unsafe_allow_html=True)

    st.subheader("Action Grid: Edge Matrix")
    
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_selection('multiple', use_checkbox=True)
    gridOptions = gb.build()

    AgGrid(df, gridOptions=gridOptions, theme='streamlit', fit_columns_on_grid_load=True)

# --- MODULE 2: THE REPO LIBRARY ---
elif menu == "📚 The Repo Library":
    st.title("The Repo Library")
    st.markdown("Centralized hub for external analytics and quantitative scripts.")
    st.code("$ python fetch_dfs_projections.py\n$ python parse_beat_writers.py\n$ status: ALL SYSTEMS NOMINAL", language="bash")
    st.button("Pull Latest Articles & Data")

# --- MODULE 3: SHARP MONEY & SCOREBOARD ---
elif menu == "📈 Sharp Money & Scoreboard":
    st.title("Vegas Odds & Sharp Tracker")
    st.warning("🚨 SHARP MONEY ALERT: Heavy late action detected on Over 65.5 Rush Yds.")
    st.dataframe(pd.DataFrame({
        "Prop": ["Rush Yds", "Rec Yds", "Anytime TD"],
        "Opening Line": [55.5, 62.5, "+120"],
        "Current Line": [65.5, 58.5, "-110"],
        "Sharp Action": ["Heavy Over", "Slight Under", "Heavy Yes"]
    }), use_container_width=True)

# --- MODULE 4: TRADE ASSASSIN ---
elif menu == "🤖 Trade Assassin & Learning Engine":
    st.title("Trade Assassin")
    st.markdown("Multi-Agent reinforcement learning is currently scanning enemy rosters...")
    
    st.markdown('<div class="neon-card">', unsafe_allow_html=True)
    st.markdown("### 🎯 Target Acquired: Team 4")
    st.markdown("**Vulnerability:** Desperate need for WR2. Overvaluing aging RBs.")
    st.markdown("**Calculated Offer:** Send Tier 3 WR + 8th Rd Pick ➡️ Receive Tier 2 RB.")
    st.markdown("**Projected Value Shift:** +18.4% in your favor.")
    if st.button("Generate Trade Text Message"):
        st.success("Drafted: 'Hey man, saw you're hurting at WR. I can float you a starter if you want to swap some backfield depth. Let me know.'")
    st.markdown('</div>', unsafe_allow_html=True)
