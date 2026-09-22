import sqlite3
import json
import streamlit as st
import os

st.set_page_config(layout="wide")

DB_PATH = os.path.join(os.getcwd(), "action_grid.db")

def inject_aesthetic_css():
    st.markdown("""
        <style>
        .stApp { background-color: #0b0914; color: #ffffff; }
        
        /* Custom Expander Styling */
        .streamlit-expanderHeader { font-weight: 800 !important; color: #00e5ff !important; background-color: #12101b !important; border: 1px solid #2a224a !important; }
        
        /* Player Box Grid */
        .player-box {
            background-color: #1a162b;
            border-left: 3px solid #ff2a6d;
            padding: 10px;
            border-radius: 4px;
            text-align: center;
            height: 100%;
        }
        .player-pos { color: #ff2a6d; font-weight: 900; font-size: 13px; margin-bottom: 4px; letter-spacing: 1px; }
        .player-name { color: #e6edf3; font-size: 11px; font-weight: bold; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        </style>
    """, unsafe_allow_html=True)

def run_sandbox():
    inject_aesthetic_css()
    st.markdown("<h3 style='color:#00e5ff; text-align:center;'>🛠️ PHASE 2 SANDBOX: DFS OPTIMIZER GRID</h3><br>", unsafe_allow_html=True)
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            # Pulling exact columns based on the audit report schema
            cur.execute("SELECT * FROM dfs_classic_lineups LIMIT 5")
            rows = cur.fetchall()
            
        for row in rows:
            lineup_id = row[0]
            proj_pts = row[3] if row[3] is not None else 0.0
            roster_str = row[4]
            
            # Safely parse the JSON payload from the database
            if roster_str and isinstance(roster_str, str) and roster_str.startswith('['):
                roster = json.loads(roster_str)
                
                with st.expander(f"👑 CLASSIC 9-MAN ROSTER #{lineup_id}  |  Proj: {proj_pts}", expanded=True):
                    cols = st.columns(9)
                    for i, p in enumerate(roster[:9]):
                        with cols[i]:
                            st.markdown(f'''
                            <div class="player-box">
                                <div class="player-pos">{p.get('pos', 'FLEX')}</div>
                                <div class="player-name">{p.get('name', 'Unknown')}</div>
                            </div>
                            ''', unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Sandbox Error: {e}")

if __name__ == "__main__":
    run_sandbox()