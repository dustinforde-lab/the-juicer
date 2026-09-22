import sqlite3
import pandas as pd
import streamlit as st
import os

st.set_page_config(layout="wide")

DB_PATH = os.path.join(os.getcwd(), "action_grid.db")

def inject_aesthetic_css():
    st.markdown("""
        <style>
        /* Base background from Streamlit cloud production */
        .stApp { background-color: #0b0914; color: #ffffff; }
        
        /* 3-Column Dark Card Matchup Grid */
        .matchup-card {
            background-color: #12101b;
            border: 1px solid #2a224a;
            border-radius: 6px;
            padding: 12px;
            margin-bottom: 16px;
        }
        .time-head { font-size: 11px; color: #8b949e; font-weight: 600; margin-bottom: 12px; }
        .team-row { display: flex; justify-content: space-between; font-size: 18px; font-weight: 800; margin-bottom: 8px; font-family: sans-serif; }
        .time-foot { font-size: 11px; color: #00e5ff; font-weight: 700; margin-top: 14px; background: #1a162b; padding: 6px; border-radius: 4px; }
        .matrix-foot { font-size: 10px; color: #6e7681; text-align: center; margin-top: 10px; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

def run_sandbox():
    inject_aesthetic_css()
    st.markdown("<h3 style='color:#ff2a6d; text-align:center;'>🛠️ PHASE 1 SANDBOX: VEGAS SCOREBOARD</h3><br>", unsafe_allow_html=True)
    
    # Visually mapping exact matchups from your production screenshots
    games = [
        ("CAR", "ATL", "Sun, September 20th at 1:00 PM EDT"),
        ("MIN", "CHI", "Sun, September 20th at 1:00 PM EDT"),
        ("PHI", "TEN", "Sun, September 20th at 1:00 PM EDT"),
        ("PIT", "NE", "Sun, September 20th at 1:00 PM EDT"),
        ("GB", "NYJ", "Sun, September 20th at 1:00 PM EDT"),
        ("CLE", "TB", "Sun, September 20th at 1:00 PM EDT"),
        ("NO", "BAL", "Sun, September 20th at 1:00 PM EDT"),
        ("CIN", "HOU", "Sun, September 20th at 1:00 PM EDT"),
        ("JAX", "DEN", "Sun, September 20th at 4:05 PM EDT")
    ]
    
    cols = st.columns(3)
    for i, (away, home, time_str) in enumerate(games):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="matchup-card">
                <div class="time-head">{time_str}</div>
                <div class="team-row"><span>{away}</span><span>0</span></div>
                <div class="team-row"><span>{home}</span><span>0</span></div>
                <div class="time-foot">{time_str}</div>
                <div class="matrix-foot">DK / FD / MGM / CZR Matrix</div>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    run_sandbox()