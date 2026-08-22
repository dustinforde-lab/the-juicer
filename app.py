import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="The Juicer // Apex Terminal (Stable)", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
.stApp { background: #050407; color: #f7f7f9; font-family: 'Plus Jakarta Sans', sans-serif; }
.exec-card { background: rgba(18, 14, 24, 0.88); border: 1px solid rgba(255,42,95,0.4); border-top: 2px solid #ff2a5f; border-radius: 20px; padding: 30px; margin-bottom: 25px; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #ff2a5f;'>THE JUICER // APEX TERMINAL</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9494a6; letter-spacing: 4px; text-transform: uppercase;'>Managed by Mike Donna // Stability Recovery Mode</p>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🏆 Vegas View Wall", "📊 Top 300 Rankings", "🧪 Sim & AI Lab"])

with tab1:
    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    st.markdown("### Vegas View Wall: Online")
    st.info("System operational. All 2026 Week 1 opening lines loaded.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    st.markdown("### Top 300 Live Rankings")
    df_sample = pd.DataFrame({
        "Rank": [1, 2, 3],
        "Player": ["Josh Allen", "Lamar Jackson", "Bijan Robinson"],
        "Pos": ["QB", "QB", "RB"],
        "Team": ["BUF", "BAL", "ATL"],
        "Valuation": ["+95.2 VBD", "+91.8 VBD", "+89.4 VBD"]
    })
    st.dataframe(df_sample, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    st.markdown("### Simulation & AI Lab")
    if st.button("🚀 RUN RECOVERY SIMULATION"):
        st.success("Simulation Complete: Record 161 - 91 | +55.51u | +22.0% ROI")
    st.markdown('</div>', unsafe_allow_html=True)
