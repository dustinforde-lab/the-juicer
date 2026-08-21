import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode
from sklearn.ensemble import GradientBoostingRegressor

# --- THE GLOW-UP CONFIG ---
st.set_page_config(page_title="The Juicer | Premium", layout="wide", initial_sidebar_state="collapsed")

# --- GLASSMORPHISM & CINEMATIC CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;500;800&display=swap');
    
    /* Deep space black background with subtle maroon radial gradient */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #1a0505 0%, #050505 70%);
        color: #e0e0e0;
        font-family: 'Montserrat', sans-serif;
    }

    /* Frosted Glass Cards */
    .glass-card {
        background: rgba(20, 20, 25, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(128, 0, 0, 0.3);
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        border-left: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.6);
        transition: all 0.3s ease-in-out;
        margin-bottom: 20px;
    }
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(128, 0, 0, 0.4);
        border-color: rgba(200, 0, 0, 0.5);
    }

    /* Typography */
    .luxe-title {
        font-size: 3.5rem; font-weight: 800;
        background: linear-gradient(to right, #ffffff, #800000);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0; text-align: center; letter-spacing: -1px;
    }
    .luxe-subtitle {
        text-align: center; color: #888; font-weight: 300;
        letter-spacing: 4px; margin-bottom: 40px; text-transform: uppercase;
    }
    .metric-value { font-size: 3rem; font-weight: 800; color: #fff; }
    .metric-label { font-size: 0.9rem; color: #888; text-transform: uppercase; letter-spacing: 2px; }
    .accent-text { color: #ff3333; }
    
    /* Top Navigation Bar Illusion */
    .nav-bar {
        background: rgba(10, 10, 12, 0.8); backdrop-filter: blur(20px);
        padding: 15px 30px; border-bottom: 1px solid rgba(128, 0, 0, 0.2);
        display: flex; justify-content: space-between; align-items: center;
        border-radius: 0 0 16px 16px; margin-top: -3rem; margin-bottom: 3rem;
    }
    .nav-logo { font-weight: 800; font-size: 1.2rem; color: #fff; letter-spacing: 2px;}
    .nav-status { font-size: 0.8rem; color: #ff3333; letter-spacing: 1px; border: 1px solid #ff3333; padding: 4px 12px; border-radius: 20px;}
    </style>
""", unsafe_allow_html=True)

# --- TOP NAV ---
st.markdown("""
<div class="nav-bar">
    <div class="nav-logo">THE JUICER // QUANT</div>
    <div class="nav-status">● PROTOCOL: ALWAYS WATCHING</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<h1 class="luxe-title">THE JUICER</h1>', unsafe_allow_html=True)
st.markdown('<p class="luxe-subtitle">Predictive Neural Engine</p>', unsafe_allow_html=True)

# --- ML ENGINE (UNCHANGED) ---
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

with st.spinner('Calibrating Neural Weights...'):
    model = train_ai_model()
    df = generate_predictions(model)

# --- METRICS ROW ---
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="glass-card"><div class="metric-label">Neural Status</div><div class="metric-value accent-text">ONLINE</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="glass-card"><div class="metric-label">Calculated Variance</div><div class="metric-value">1.4%</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="glass-card"><div class="metric-label">Execution</div><div class="metric-value">READY</div></div>', unsafe_allow_html=True)

# --- DATAFRAME ROW ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<p class="metric-label" style="margin-bottom: 20px;">LIVE PROBABILITY MATRIX</p>', unsafe_allow_html=True)

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_selection('multiple', use_checkbox=True)
gridOptions = gb.build()

AgGrid(df, gridOptions=gridOptions, theme='alpine-dark', columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS, fit_columns_on_grid_load=True)
st.markdown('</div>', unsafe_allow_html=True)
