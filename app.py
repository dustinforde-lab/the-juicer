import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# --- PAGE CONFIG ---
st.set_page_config(page_title="The Juicer", layout="wide")

# --- CUSTOM STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #f0f2f6; }
    .metric-card {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        border: 1px solid #374151; padding: 20px; border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3); margin-bottom: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# --- APP HEADER ---
st.title("🍹 The Juicer: Action Grid Optimizer")

# --- DATA PROCESSING ---
@st.cache_data
def load_data():
    try:
        return pd.read_csv("keepers.csv")
    except FileNotFoundError:
        return pd.DataFrame({
            "Player": ["Kenneth Walker", "Derrick Henry", "Open Roster Spot"], 
            "Status": ["Keeper", "Keeper", "Draft"], 
            "Value": [150, 180, 0]
        })

df = load_data()

# --- DASHBOARD METRICS ---
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="metric-card">Total Assets Loaded: ' + str(len(df)) + '</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card">Optimizer Status: Active</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card">System Health: 100%</div>', unsafe_allow_html=True)

# --- ACTION GRID ---
st.subheader("Action Grid")

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_selection('multiple', use_checkbox=True)
gridOptions = gb.build()

AgGrid(
    df, 
    gridOptions=gridOptions, 
    theme='streamlit', 
    fit_columns_on_grid_load=True,
    update_mode=GridUpdateMode.MODEL_CHANGED
)