# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "action_grid.db")

def render_news_desk():
    st.markdown("<h2 style='color:#ffa502; margin-bottom:2px;'>📰 LIVE WIRE & INJURY TRACKER</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color:#8b949e; font-size:12px; margin-bottom:18px;'>ESPN Breaking News &bull; Sleeper Injury Tracking &bull; Beat Reports</div>", unsafe_allow_html=True)
    
    if os.path.exists(DB_PATH):
        with sqlite3.connect(DB_PATH) as conn:
            news_df = pd.read_sql("SELECT Headline, Description, Source, Published_At FROM breaking_news_feed ORDER BY Published_At DESC", conn)
            
        if not news_df.empty:
            for _, row in news_df.iterrows():
                st.markdown(f"""
                    <div style='background:#0d1117; border:1px solid #30363d; border-left:4px solid #ffa502; border-radius:8px; padding:12px; margin-bottom:10px;'>
                        <div style='font-size:14px; font-weight:800; color:#ffffff;'>{row["Headline"]}</div>
                        <div style='font-size:12px; color:#c9d1d9; margin-top:4px;'>{row["Description"]}</div>
                        <div style='font-size:10px; color:#8b949e; margin-top:6px;'>Source: {row["Source"]} &bull; {row["Published_At"]}</div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No breaking news items currently recorded. Run data_news_wire.py to sync.")

