import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode
from sklearn.ensemble import GradientBoostingRegressor

# --- GVP APEX CONFIG ---
st.set_page_config(page_title="The Juicer // Full-Season Command Center", layout="wide", initial_sidebar_state="collapsed")

# --- CINEMATIC GLASSMORPHISM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;500;800&display=swap');
    
    .stApp {
        background: radial-gradient(circle at 50% 0%, #1a0505 0%, #050505 70%);
        color: #e0e0e0;
        font-family: 'Montserrat', sans-serif;
    }

    .glass-card {
        background: rgba(20, 20, 25, 0.4); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(128, 0, 0, 0.3); border-top: 1px solid rgba(255, 255, 255, 0.1); border-left: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px; padding: 25px; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.6); margin-bottom: 20px;
    }
    
    .luxe-title {
        font-size: 3rem; font-weight: 800; background: linear-gradient(to right, #ffffff, #800000);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0; text-align: center; letter-spacing: -1px;
    }
    .luxe-subtitle { text-align: center; color: #888; font-weight: 300; letter-spacing: 3px; margin-bottom: 30px; text-transform: uppercase; font-size: 0.85rem;}
    
    /* Live Scoreboard Header */
    .scoreboard-container {
        background: rgba(10, 10, 12, 0.9); border: 1px solid rgba(128, 0, 0, 0.4);
        padding: 12px 20px; border-radius: 12px; display: flex; justify-content: space-around;
        align-items: center; margin-bottom: 30px; font-size: 0.9rem; letter-spacing: 1px;
    }
    .score-item { text-align: center; border-right: 1px solid rgba(255,255,255,0.1); padding-right: 25px; }
    .score-item:last-child { border-right: none; }
    .live-dot { height: 8px; width: 8px; background-color: #ff3333; border-radius: 50%; display: inline-block; box-shadow: 0 0 8px #ff3333; animation: pulse 1.5s infinite; }
    
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
    </style>
""", unsafe_allow_html=True)

# --- PERSISTENT LIVE SCOREBOARD (HUD) ---
st.markdown("""
<div class="scoreboard-container">
    <div class="score-item"><span class="live-dot"></span> <b>LIVE TICKER</b></div>
    <div class="score-item"><b>MIN 24</b> - GB 17 <span style="color:#888;">(4th Qtr)</span></div>
    <div class="score-item"><b>KC 31</b> - LAC 24 <span style="color:#888;">(Final)</span></div>
    <div class="score-item"><b>BUF 28</b> - MIA 21 <span style="color:#888;">(2nd Qtr)</span></div>
    <div class="score-item" style="color: #ff3333;"><b>SYSTEM:</b> ONLINE</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<h1 class="luxe-title">THE JUICER</h1>', unsafe_allow_html=True)
st.markdown('<p class="luxe-subtitle">Full-Season Spread Matrix & Neural Engine</p>', unsafe_allow_html=True)

# --- FULL-SEASON SLATE & SPREAD TRACKER (WEEKS 1-18) ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
col_head1, col_head2 = st.columns([2, 1])
with col_head1:
    st.markdown('<p style="color: #fff; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; margin-bottom:0;">Full-Season Spread Movement Tracker</p>', unsafe_allow_html=True)
with col_head2:
    selected_week = st.selectbox("Select Slate Window", [f"Week {i}" for i in range(1, 19)], index=0, label_visibility="collapsed")

@st.cache_data
def load_season_slate(week):
    # Simulating data tracking movement from Week 1 baseline to current tracking
    return pd.DataFrame({
        "Matchup": ["KC @ DET", "BUF @ NYJ", "SF @ PIT", "PHI @ NE", "MIN @ CHI"],
        "Opening Spread": ["KC -6.5", "BUF -2.5", "SF -3.0", "PHI -4.0", "CHI -3.5"],
        "Current Spread": ["KC -8.5", "BUF -1.5", "SF -4.5", "PHI -3.5", "CHI -4.5"],
        "Line Delta": ["+2.0 (Sharp)", "-1.0 (Steam)", "+1.5 (Sharp)", "-0.5 (Public)", "+1.0 (Sharp)"],
        "O/U Total": [53.5, 45.5, 41.5, 48.0, 43.5],
        "Action Status": ["LOCK", "FADE", "LOCK", "PASS", "LOCK"]
    })

df_slate = load_season_slate(selected_week)
sb = GridOptionsBuilder.from_dataframe(df_slate)
sb.configure_selection('multiple', use_checkbox=True)
AgGrid(df_slate, gridOptions=sb.build(), theme='alpine-dark', fit_columns_on_grid_load=True, height=220)
st.markdown('</div>', unsafe_allow_html=True)

# --- ML ENGINE & PROBABILITY MATRIX ---
@st.cache_resource
def train_ai_model():
    np.random.seed(42)
    X = np.random.rand(500, 3) * 100 
    y = X[:, 0] * 0.4 + X[:, 1] * 0.5 - X[:, 2] * 0.2 + np.random.randn(500) * 5 
    model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3)
    model.fit(X, y)
    return model

@st.cache_data
def generate_predictions(_model):
    players = ["Kenneth Walker", "Breece Hall", "Amon-Ra St. Brown", "Justin Herbert"]
    X_live = np.random.rand(4, 3) * 100
    preds = _model.predict(X_live)
    lines = [70.5, 80.0, 95.5, 250.5]
    edges = ((preds - lines) / lines) * 100
    
    return pd.DataFrame({
        "ASSET": players,
        "VEGAS LINE": lines,
        "MODEL PROJ": np.round(preds, 1),
        "TRUE EDGE": [f"+{e:.1f}%" if e > 0 else f"{e:.1f}%" for e in edges],
        "SYSTEM CALL": ["LOCK" if e > 5 else "FADE" if e < -5 else "PLAY" for e in edges]
    })

with st.spinner('Calibrating Neural Network...'):
    model = train_ai_model()
    df_ml = generate_predictions(model)

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<p style="color: #888; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 2px;">NEURAL EDGE MATRIX</p>', unsafe_allow_html=True)

gb = GridOptionsBuilder.from_dataframe(df_ml)
gb.configure_selection('multiple', use_checkbox=True)
AgGrid(df_ml, gridOptions=gb.build(), theme='alpine-dark', fit_columns_on_grid_load=True, height=220)
st.markdown('</div>', unsafe_allow_html=True)
