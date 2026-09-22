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
        
        .player-card {
            background-color: #12101b;
            border: 1px solid #2a224a;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        .card-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1a162b; padding-bottom: 10px; margin-bottom: 10px; }
        .p-name { font-size: 18px; font-weight: 900; color: #e6edf3; }
        .p-team { font-size: 14px; color: #8b949e; font-weight: bold; margin-left: 8px; }
        .p-pos { background-color: rgba(255, 42, 109, 0.15); color: #ff2a6d; border: 1px solid #ff2a6d; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; margin-right: 12px; }
        .p-fp { color: #00e5ff; font-size: 18px; font-weight: 900; }
        
        .stat-container { display: flex; flex-wrap: wrap; gap: 10px; }
        .stat-badge { background-color: #1a162b; border: 1px solid #2a224a; padding: 6px 12px; border-radius: 4px; font-size: 12px; font-weight: bold; color: #a5b4fc; }
        .stat-value { color: #ffffff; font-size: 14px; font-weight: 900; margin-left: 6px; }
        </style>
    """, unsafe_allow_html=True)

def run_sandbox():
    inject_aesthetic_css()
    st.markdown("<h3 class='neon-title'>🛠️ PHASE 4: DONNA'S LEVERAGE (PLAYER CARDS)</h3><br>", unsafe_allow_html=True)
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM player_rankings LIMIT 15")
            rows = [dict(r) for r in cur.fetchall()]
            
        if not rows:
            st.info("No records found in player_rankings.")
            return

        for r in rows:
            name = r.get("player") or r.get("player_name") or "Unknown"
            team = r.get("team") or "FA"
            pos = r.get("pos") or "FLEX"
            fp = r.get("proj_fp") or r.get("fp") or "0.0"
            
            # Exclude metadata columns to just loop through the actual stats
            exclude_keys = ['id', 'player', 'player_name', 'team', 'pos', 'proj_fp', 'fp', 'rank', 'value_rating']
            stat_html = ""
            for key, val in r.items():
                if key.lower() not in exclude_keys and val is not None:
                    # Clean up the key name for display (e.g., proj_pass_yds -> Proj Pass Yds)
                    clean_key = key.replace("_", " ").title()
                    stat_html += f'<div class="stat-badge">{clean_key}: <span class="stat-value">{val}</span></div>'
            
            st.markdown(f'''
            <div class="player-card">
                <div class="card-header">
                    <div>
                        <span class="p-pos">{pos}</span>
                        <span class="p-name">{name}</span>
                        <span class="p-team">({team})</span>
                    </div>
                    <div class="p-fp">{fp} FP</div>
                </div>
                <div class="stat-container">
                    {stat_html if stat_html else '<div class="stat-badge">No extended stats available</div>'}
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Sandbox Error: {e}")

if __name__ == "__main__":
    run_sandbox()