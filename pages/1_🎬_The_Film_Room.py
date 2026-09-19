import streamlit as st
import sqlite3
import pandas as pd
import os

st.set_page_config(page_title="The Film Room", layout="wide", page_icon="🎬")

st.markdown("""
<style>
    .stDataFrame { border-radius: 8px; overflow: hidden; border: 1px solid #212838; }
    h3 { letter-spacing: 1.5px; text-transform: uppercase; font-size: 1.05rem; margin-bottom: -15px;}
    .block-container { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: #fff; letter-spacing: 4px; font-weight: 900;'>🎬 THE FILM ROOM <span style='color:#00e5ff'>// AGENT ANALYTICS</span></h2><hr style='border-color: #212838;'>", unsafe_allow_html=True)

try:
    # Streamlit runs from the root directory, so paths remain the same
    conn = sqlite3.connect("action_grid.db")
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("<h3 style='color:#00e5ff;'>🧠 MIKE'S NEURAL MAP (RECIPE WEIGHTS)</h3><br>", unsafe_allow_html=True)
        if os.path.exists("film_room_radar.png"):
            st.image("film_room_radar.png", use_container_width=True)
            
        df_weights = pd.read_sql("SELECT recipe_name as 'Recipe Strategy', sample_size as 'Slips Graded', win_rate as 'Win %', weight_modifier as 'AI Multiplier' FROM correlation_weights ORDER BY win_rate DESC", conn)
        st.dataframe(df_weights, use_container_width=True, hide_index=True)

        st.markdown("<br><h3 style='color:#ffaa00;'>📉 DONNA'S VIBE CHECK (LIVE CHALK DATA)</h3><br>", unsafe_allow_html=True)
        try:
            df_vibe = pd.read_sql("SELECT player_name as 'Player', team as 'Team', projected_ownership as 'Ownership', vibe_rating as 'Donna Tag' FROM ownership_projections", conn)
            st.dataframe(df_vibe, use_container_width=True, hide_index=True)
        except Exception: 
            st.caption("No DFS ownership data active.")

    with col2:
        st.markdown("<h3 style='color:#00ff88;'>🔥 THE JUICE PRESS (+EV MARKET EDGES)</h3><br>", unsafe_allow_html=True)
        try:
            df_sharp = pd.read_sql("SELECT player_name as 'Player', stat_target as 'Prop', sharp_odds as 'Pinnacle', soft_odds as 'DraftKings', ev_edge as 'Edge %' FROM sharp_market_lines", conn)
            st.dataframe(df_sharp, use_container_width=True, hide_index=True)
        except Exception:
            st.caption("No sharp market edges detected.")

        st.markdown("<br><h3 style='color:#ff2a6d;'>🚑 THE MEDIC (LIVE HOSPITAL WARD)</h3><br>", unsafe_allow_html=True)
        try:
            df_inj = pd.read_sql("SELECT player_name as 'Player', team as 'Team', status as 'Status', medical_note as 'Injury Wire', updated_at as 'Last Synced' FROM hospital_ward", conn)
            st.dataframe(df_inj, use_container_width=True, hide_index=True)
        except Exception:
            st.caption("Hospital ward empty.")

except Exception as e:
    st.error(f"Failed to connect to War Room database: {e}. Run the Orchestrator on the main page first.")
