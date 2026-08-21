import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode
from sklearn.ensemble import GradientBoostingRegressor

# --- PINK PONY CLUB // GROOVY APEX CONFIG ---
st.set_page_config(page_title="The Juicer | Pink Pony Club Edition", layout="wide", initial_sidebar_state="expanded")

# --- CINEMATIC GLASSMORPHISM & GROOVY CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;500;800&display=swap');
    
    .stApp {
        background: radial-gradient(circle at 50% 0%, #2a0808 0%, #050505 70%);
        color: #e0e0e0;
        font-family: 'Montserrat', sans-serif;
    }

    .glass-card {
        background: rgba(20, 20, 25, 0.45); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(128, 0, 0, 0.4); border-top: 1px solid rgba(255, 255, 255, 0.1); border-left: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px; padding: 25px; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.6); margin-bottom: 20px;
    }
    
    .luxe-title {
        font-size: 3rem; font-weight: 800; background: linear-gradient(to right, #ffffff, #ff4d4d, #800000);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0; text-align: center; letter-spacing: -1px;
    }
    .luxe-subtitle { text-align: center; color: #ff9999; font-weight: 300; letter-spacing: 4px; margin-bottom: 25px; text-transform: uppercase; font-size: 0.85rem;}
    
    .scoreboard-container {
        background: rgba(10, 10, 12, 0.9); border: 1px solid rgba(128, 0, 0, 0.5);
        padding: 12px 20px; border-radius: 12px; display: flex; justify-content: space-around;
        align-items: center; margin-bottom: 25px; font-size: 0.9rem; letter-spacing: 1px;
    }
    .score-item { text-align: center; border-right: 1px solid rgba(255,255,255,0.1); padding-right: 25px; }
    .score-item:last-child { border-right: none; }
    .live-dot { height: 8px; width: 8px; background-color: #ff3333; border-radius: 50%; display: inline-block; box-shadow: 0 0 10px #ff3333; animation: pulse 1.5s infinite; }
    
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
    </style>
""", unsafe_allow_html=True)

# --- PERSISTENT LIVE SCOREBOARD (HUD) ---
st.markdown("""
<div class="scoreboard-container">
    <div class="score-item"><span class="live-dot"></span> <b>PINK PONY TICKER</b></div>
    <div class="score-item"><b>MIN 24</b> - GB 17 <span style="color:#888;">(4th Qtr)</span></div>
    <div class="score-item"><b>KC 31</b> - LAC 24 <span style="color:#888;">(Final)</span></div>
    <div class="score-item"><b>BUF 28</b> - MIA 21 <span style="color:#888;">(2nd Qtr)</span></div>
    <div class="score-item" style="color: #ff3333;"><b>STATUS:</b> ALWAYS WATCHING</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<h1 class="luxe-title">THE JUICER</h1>', unsafe_allow_html=True)
st.markdown('<p class="luxe-subtitle">Pink Pony Club // Multi-Tab Command Center</p>', unsafe_allow_html=True)

# --- SEPARATE TABS ARCHITECTURE ---
tab1, tab2, tab3, tab4 = st.tabs([
    "🏆 Live War Room", 
    "📊 Prop Matrix & SGPs", 
    "🌤️ Weather & Data Hub", 
    "💰 Bankroll & Bet Tracker (150+)"
])

# ================= TAB 1: LIVE WAR ROOM =================
with tab1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3>Full-Season Spread Movement Tracker (Weeks 1-18)</h3>', unsafe_allow_html=True)
    selected_week = st.selectbox("Select Slate Window", [f"Week {i}" for i in range(1, 19)], index=0)
    
    df_slate = pd.DataFrame({
        "Matchup": ["KC @ DET", "BUF @ NYJ", "SF @ PIT", "PHI @ NE", "MIN @ CHI"],
        "Opening Spread": ["KC -6.5", "BUF -2.5", "SF -3.0", "PHI -4.0", "CHI -3.5"],
        "Current Spread": ["KC -8.5", "BUF -1.5", "SF -4.5", "PHI -3.5", "CHI -4.5"],
        "Line Delta": ["+2.0 (Sharp)", "-1.0 (Steam)", "+1.5 (Sharp)", "-0.5 (Public)", "+1.0 (Sharp)"],
        "O/U Total": [53.5, 45.5, 41.5, 48.0, 43.5],
        "Action Status": ["LOCK", "FADE", "LOCK", "PASS", "LOCK"]
    })
    AgGrid(df_slate, gridOptions=GridOptionsBuilder.from_dataframe(df_slate).build(), theme='alpine-dark', fit_columns_on_grid_load=True, height=220)
    st.markdown('</div>', unsafe_allow_html=True)

    # ML Engine Matrix
    @st.cache_resource
    def train_ai_model():
        np.random.seed(42)
        X = np.random.rand(500, 3) * 100 
        y = X[:, 0] * 0.4 + X[:, 1] * 0.5 - X[:, 2] * 0.2 + np.random.randn(500) * 5 
        model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3)
        model.fit(X, y)
        return model

    model = train_ai_model()
    X_live = np.random.rand(4, 3) * 100
    preds = model.predict(X_live)
    lines = [70.5, 80.0, 95.5, 250.5]
    edges = ((preds - lines) / lines) * 100
    
    df_ml = pd.DataFrame({
        "ASSET": ["Kenneth Walker", "Breece Hall", "Amon-Ra St. Brown", "Justin Herbert"],
        "VEGAS LINE": lines,
        "AI PROJ": np.round(preds, 1),
        "TRUE EDGE": [f"+{e:.1f}%" if e > 0 else f"{e:.1f}%" for e in edges],
        "SYSTEM CALL": ["LOCK" if e > 5 else "FADE" if e < -5 else "PLAY" for e in edges]
    })
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3>Neural Edge Matrix</h3>', unsafe_allow_html=True)
    AgGrid(df_ml, gridOptions=GridOptionsBuilder.from_dataframe(df_ml).build(), theme='alpine-dark', fit_columns_on_grid_load=True, height=200)
    st.markdown('</div>', unsafe_allow_html=True)

# ================= TAB 2: PROP MATRIX & SGPS =================
with tab2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3>Cross-Book Prop Matrix & SGP Correlation Builder</h3>', unsafe_allow_html=True)
    df_props = pd.DataFrame({
        "Player": ["Kenneth Walker", "Breece Hall", "Amon-Ra St. Brown", "Justin Herbert"],
        "Prop Type": ["Rush Yards", "Receptions", "Rec Yards", "Pass Yards"],
        "DraftKings": ["65.5 O (-110)", "4.5 O (-115)", "82.5 O (-105)", "245.5 O (-110)"],
        "FanDuel": ["64.5 O (-115)", "4.5 U (-110)", "84.5 O (-110)", "248.5 O (-115)"],
        "Underdog / PrizePicks": ["65.0 (Higher)", "4.0 (Higher)", "83.0 (Higher)", "246.0 (Higher)"],
        "SGP Correlation Tag": ["QB Stack High", "Isolated Play", "Primary Target", "Game Stack"]
    })
    AgGrid(df_props, gridOptions=GridOptionsBuilder.from_dataframe(df_props).build(), theme='alpine-dark', fit_columns_on_grid_load=True, height=250)
    st.markdown('</div>', unsafe_allow_html=True)

# ================= TAB 3: WEATHER & DATA HUB =================
with tab3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3>Live Stadium Weather & Environmental Impact API</h3>', unsafe_allow_html=True)
    df_weather = pd.DataFrame({
        "Stadium / Venue": ["Lambeau Field", "Soldier Field", "U.S. Bank Stadium", "Arrowhead Stadium"],
        "Condition": ["Clear / Chilly", "High Winds (18mph)", "Dome (Controlled)", "Overcast"],
        "Temp (°F)": [42, 38, 72, 58],
        "Passing Impact": ["Neutral", "Negative (-4.2%)", "Positive (+2.0%)", "Neutral"],
        "Kicking Impact": ["Slight Drift", "High Turbulence", "None", "Optimal"]
    })
    AgGrid(df_weather, gridOptions=GridOptionsBuilder.from_dataframe(df_weather).build(), theme='alpine-dark', fit_columns_on_grid_load=True, height=220)
    st.markdown('</div>', unsafe_allow_html=True)

# ================= TAB 4: BANKROLL & BET TRACKER =================
with tab4:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3>Active Bankroll Survival Meter & 150+ Bet Quota Log</h3>', unsafe_allow_html=True)
    col_b1, col_b2, col_b3 = st.columns(3)
    col_b1.metric("Remaining Bankroll", "$142.50", "-$7.50")
    col_b2.metric("Active Bets Placed", "18 / 150 Target", "Pacing Hot")
    col_b3.metric("System Win Rate", "61.2%", "+4.8% vs Books")
    
    df_bets = pd.DataFrame({
        "Bet ID": ["#1041", "#1042", "#1043", "#1044"],
        "Type": ["SGP (DK)", "PrizePicks 2-Leg", "Over/Under", "Book Straight"],
        "Selection": ["Walker Over + St. Brown Over", "Breece Hall Higher", "KC -8.5", "Herbert 250+ Pass"],
        "Stake": ["$10.00", "$15.00", "$25.00", "$10.00"],
        "Status": ["PENDING", "PENDING", "LOCKED", "PENDING"]
    })
    AgGrid(df_bets, gridOptions=GridOptionsBuilder.from_dataframe(df_bets).build(), theme='alpine-dark', fit_columns_on_grid_load=True, height=200)
    st.markdown('</div>', unsafe_allow_html=True)
