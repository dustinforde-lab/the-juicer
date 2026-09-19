import streamlit as st
import sqlite3
import pandas as pd

def render_live_telemetry(db_file="action_grid.db"):
    st.markdown("<h3 style='color:#00ff88;'>📡 SYNDICATE LIVE TELEMETRY</h3>", unsafe_allow_html=True)
    try:
        with sqlite3.connect(db_file) as conn:
            df = pd.read_sql("SELECT timestamp, sender, action, target, directive FROM agent_chatter ORDER BY message_id DESC LIMIT 5", conn)
            
        if not df.empty:
            for _, row in df.iterrows():
                color = "#ff2a6d" if row['action'] in ["PURGE", "FADE"] else "#00e5ff" if row['action'] == "ADJUST" else "#00ff88"
                
                html = f"""
                <div style="background: #121824; border-left: 4px solid {color}; padding: 12px; margin-bottom: 8px; border-radius: 4px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                    <span style="color: {color}; font-weight: 800; font-size: 0.9rem; letter-spacing: 1px;">[{row['sender']}] {row['action']} &rarr; {row['target']}</span><br>
                    <span style="color: #e6edf3; font-size: 0.85rem; margin-top: 4px; display: block;">{row['directive']}</span>
                </div>
                """
                st.markdown(html, unsafe_allow_html=True)
        else:
            st.caption("Awaiting intelligence feeds...")
    except Exception as e:
        st.error(f"Telemetry Feed Offline: {e}")
