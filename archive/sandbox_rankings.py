import sqlite3
import pandas as pd
import streamlit as st
import os

st.set_page_config(layout="wide")
DB_PATH = os.path.join(os.getcwd(), "action_grid.db")

def inject_aesthetic_css():
    st.markdown("""
        <style>
        .stApp { background-color: #0b0914; color: #ffffff; }
        .neon-title { color: #bb88ff; text-align: center; font-weight: 900; letter-spacing: 2px; }
        /* Style the dataframe container to blend with dark mode */
        [data-testid="stDataFrame"] { border-radius: 8px; border: 1px solid #2a224a; overflow: hidden; }
        </style>
    """, unsafe_allow_html=True)

def run_sandbox():
    inject_aesthetic_css()
    st.markdown("<h3 class='neon-title'>🛠️ PHASE 4 SANDBOX: CLASSY RANKINGS & DONNA'S LEVERAGE</h3><br>", unsafe_allow_html=True)
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            # Safely read the entire table structure as it currently exists
            df = pd.read_sql("SELECT * FROM player_rankings LIMIT 300", conn)
            
        if df.empty:
            st.info("No records found in player_rankings.")
            return
            
        # Dynamically generate a position filter if a 'pos' column exists
        if 'pos' in df.columns:
            positions = ["ALL"] + sorted(list(df['pos'].dropna().unique()))
            col1, col2 = st.columns([1, 4])
            with col1:
                filter_pos = st.selectbox("🎯 Filter Position Group", positions)
            if filter_pos != "ALL":
                df = df[df['pos'] == filter_pos]
                
        # Render the full sortable interactive dataframe
        st.dataframe(df, use_container_width=True, height=600)
        
    except Exception as e:
        st.error(f"Sandbox Error: {e}")

if __name__ == "__main__":
    run_sandbox()