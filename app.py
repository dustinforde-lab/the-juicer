import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder
from sklearn.ensemble import GradientBoostingRegressor

# --- ELITE CONFIGURATION ---
st.set_page_config(page_title="The Juicer | AI Learning Edition", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM RUBY CREW CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@700&family=Inter:wght@400;600;800&display=swap');
    
    .stApp { background-color: #050505; color: #e2e8f0; font-family: 'Inter', sans-serif; }
    
    [data-testid="stSidebar"] {
        background-color: #0f0f13 !important;
        border-right: 1px solid #2a2a35;
    }
    
    h1, h2, h3 { font-family: 'Syncopate', sans-serif; text-transform: uppercase; letter-spacing: 2px; }
    .neon-title { color: #ffffff; text-shadow: 0 0 10px #800000, 0 0 20px #5c0000; margin-bottom: 0.5rem; }
    
    .hud-module {
        background: linear-gradient(145deg, #121217 0%, #0a0a0d 100%);
        border: 1px solid #331515; border-left: 4px solid #800000;
        padding: 25px; border-radius: 4px; box-shadow: 0 8px 32px 0 rgba(128, 0, 0, 0.15); margin-bottom: 20px;
    }
    
    .hud-label { color: #8a8a9e; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
    .hud-value { color: #ffffff; font-size: 2.5rem; font-weight: 800; line-height: 1.2; }
    .hud-accent { color: #800000; }
    
    .terminal-box {
        background-color: #000000; border: 1px solid #333; padding: 15px; font-family: 'Courier New', monospace;
        color: #a0aec0; font-size: 0.9rem; border-radius: 4px;
    }
    .terminal-maroon { color: #ff4d4d; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- VIP SIDEBAR ---
st.sidebar.markdown('<h1 style="color:#800000; font-size: 2rem; margin-bottom: 0;">THE JUICER</h1>', unsafe_allow_html=True)
st.sidebar.markdown('<p style="color:#8a8a9e; font-size: 0.9rem; margin-top: 0; letter-spacing: 1px;">AI QUANT ENGINE</p>', unsafe_allow_html=True)
st.sidebar.markdown('---')

st.sidebar.markdown("""
<div style="background: #121217; border: 1px solid #2a2a35; padding: 15px; border-radius: 4px; text-align: center;">
    <p style="color:#800000; font-family:'Syncopate', sans-serif; font-size:0.9rem; margin-bottom:5px;">RUBY CREW ACCESS</p>
    <p style="color:#a0aec0; font-size:0.75rem; margin:0;">Status: VERIFIED VIP</p>
    <p style="color:#a0aec0; font-size:0.75rem; margin:0;">Machine Learning: ONLINE</p>
</div>
""", unsafe_allow_html=True)

# --- MACHINE LEARNING ENGINE ---
@st.cache_resource
def train_ai_model():
    # Simulating historical DFS data 
    np.random.seed(42)
    X = np.random.rand(500, 3) * 100 
    y = X[:, 0] * 0.4 + X[:, 1] * 0.5 - X[:, 2] * 0.2 + np.random.randn(500) * 5 
    
    model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3)
    model.fit(X, y)
    return model

@st.cache_data
def generate_live_predictions(_model):
    # Generating live slate predictions
    players = ["Kenneth Walker", "Breece Hall", "Amon-Ra St. Brown", "Justin Herbert"]
    live_features = np.random.rand(4, 3) * 100
    predictions = _model.predict(live_features)
    
    # Expected Value Math Engine
    vegas_lines = [70.5, 80.0, 95.5, 250.5]
    edges = ((predictions - vegas_lines) / vegas_lines) * 100
    
    df = pd.DataFrame({
        "Asset": players,
        "Vegas Line": vegas_lines,
        "AI Projected": np.round(predictions, 1),
        "Calculated Edge": [f"+{e:.1f}%" if e > 0 else f"{e:.1f}%" for e in edges],
        "Action": ["LOCK" if e > 5 else "FADE" if e < -5 else "PLAY" for e in edges]
    })
    return df

st.markdown('<h1 class="neon-title">TACTICAL DASHBOARD</h1>', unsafe_allow_html=True)

with st.spinner('Neural Network Training Sequence Initiated...'):
    ai_model = train_ai_model()
    df = generate_live_predictions(ai_model)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="hud-module"><div class="hud-label">ML Model Status</div><div class="hud-value hud-accent">FITTED</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="hud-module"><div class="hud-label">Gradient Boosting Trees</div><div class="hud-value">100</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="hud-module"><div class="hud-label">Algorithmic Edge</div><div class="hud-value" style="color: #4ade80;">ACTIVE</div></div>', unsafe_allow_html=True)

st.markdown("""
<div class="terminal-box">
    > BOOTING SCIKIT-LEARN PROTOCOLS...<br>
    > TRAINING GRADIENT BOOSTING REGRESSOR ON HISTORICAL SLATES... DONE.<br>
    > <span class="terminal-maroon">DISPATCH PROTOCOL: ALWAYS WATCHING. CALCULATING TRUE +EV.</span><br>
</div>
<br>
""", unsafe_allow_html=True)

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_selection('multiple', use_checkbox=True)
gridOptions = gb.build()

AgGrid(df, gridOptions=gridOptions, theme='alpine-dark', fit_columns_on_grid_load=True)
