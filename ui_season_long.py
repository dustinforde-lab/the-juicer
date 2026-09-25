import streamlit as st
import pandas as pd
import os

def render_season_long():
    st.markdown("<h2 style='color:#ffd700; margin-bottom:2px;'>🏈 SEASON LONG & MASTER 200</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color:#8b949e; font-size:12px; margin-bottom:14px;'>Master PPR Top 200 • Keeper Valuation • Straight Cash Roster Audit</div>", unsafe_allow_html=True)
    
    file_path = "Jeff_Rankings_TOP_200_PPR__SQL_.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        st.success(f"✅ Loaded Master 200 Sheet ({len(df)} players indexed).")
        st.dataframe(df, use_container_width=True, height=450)
    else:
        st.info("Place Jeff_Rankings_TOP_200_PPR__SQL_.csv in your project folder to display the Master 200 board.")
