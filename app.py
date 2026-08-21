import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder

st.set_page_config(page_title="The Juicer: Quant Engine", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0a0a0f; color: #f0f2f6; }
    .metric-box { background: linear-gradient(135deg, #131b2f 0%, #0b101a 100%); border: 1px solid #2d3748; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.4); }
    </style>
""", unsafe_allow_html=True)

st.title("🍹 The Juicer: Autonomous Quant Engine")
st.markdown("### DFS Slate Optimizer & Prop Matrix")

@st.cache_data
def load_matrix():
    return pd.DataFrame({
        "Player": ["Kenneth Walker", "Derrick Henry", "Breece Hall", "Amon-Ra St. Brown"],
        "Market": ["Rush Yds", "Rush Yds", "Anytime TD", "Rec Yds"],
        "Line": [65.5, 72.5, "N/A", 82.5],
        "Our Proj": [74.2, 68.1, "N/A", 91.0],
        "Win Prob %": [62.4, 41.2, 58.9, 65.1],
        "Edge / ROI": ["+14.2%", "-4.1%", "+8.5%", "+18.3%"]
    })

df = load_matrix()

col1, col2, col3 = st.columns(3)
col1.markdown('<div class="metric-box">Active Slate: <b>Main</b></div>', unsafe_allow_html=True)
col2.markdown('<div class="metric-box">Top Value: <b>A. St. Brown (+18.3%)</b></div>', unsafe_allow_html=True)
col3.markdown('<div class="metric-box">System Status: <b>OPTIMIZED</b></div>', unsafe_allow_html=True)

st.subheader("Action Grid: Edge Matrix")
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_selection('multiple', use_checkbox=True)
gridOptions = gb.build()

AgGrid(df, gridOptions=gridOptions, theme='streamlit', fit_columns_on_grid_load=True)
