# ==========================================
# === JUICER EXTENSION MODULE (NON-DESTRUCTIVE) ===
# ==========================================
import streamlit as st
import sqlite3
import pandas as pd
import datetime

DB_PATH = "action_grid.db"

def render_safe_vegas_wall():
    st.markdown("### 🏆 VEGAS ACTION SCOREBOARD & LIVE LINES")
    try:
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql("SELECT game, week, over_under, spread, sportsbook, updated_at FROM game_lines", conn)
            if not df.empty:
                cols = st.columns(2)
                for idx, row in df.iterrows():
                    with cols[idx % 2]:
                        st.markdown(f"""
                            <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border: 1px solid #334155; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
                                <h4 style="margin: 0; color: #f8fafc;">{row['game']} <span style="background: #ff3366; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem;">Wk {row['week']}</span></h4>
                                <p style="margin: 8px 0 0 0; color: #cbd5e1;"><b>Spread:</b> {row['spread']} | <b>O/U:</b> {row['over_under']}</p>
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("No active game lines found.")
    except Exception as e:
        st.error(f"Scoreboard error: {e}")

def render_safe_prizepicks():
    st.markdown("### 📈 PRIZEPICKS & UNDERDOG SLIPS")
    try:
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql("SELECT id, platform, leg_count, implied_probability, confidence_tier, status FROM slips LIMIT 20", conn)
            if not df.empty:
                for _, row in df.iterrows():
                    st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border: 1px solid #334155; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
                            <div style="display: flex; justify-content: space-between;">
                                <b>Slip #{row['id']}</b> ({row['platform']})
                                <span style="background: #0284c7; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem;">Tier {row['confidence_tier']}</span>
                            </div>
                            <p style="margin: 5px 0 0 0; color: #cbd5e1;">Legs: <b>{row['leg_count']}</b> | Prob: <code>{row['implied_probability']}</code> | Status: <b>{row['status']}</b></p>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("No slips available.")
    except Exception as e:
        st.error(f"PrizePicks error: {e}")