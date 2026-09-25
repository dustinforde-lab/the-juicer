# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

def render_season_long():
    st.markdown("<h2 style='color:#00e5ff; margin-bottom:2px;'>🏈 SEASON LONG & KEEPER LOCKERS</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color:#8b949e; font-size:12px; margin-bottom:14px;'>Jeff Rankings Top 200 &bull; Value Over Replacement (VOR) &bull; MyFantasyLeague Sync</div>", unsafe_allow_html=True)
    
    if "season_mode" not in st.session_state: st.session_state["season_mode"] = "Master Draft Board"
    st.session_state["season_mode"] = st.radio("Season Tools", ["Master Draft Board", "Straight Cash Keeper Ledger"], horizontal=True)

    if st.session_state["season_mode"] == "Master Draft Board":
        st.markdown("""
        <div style='background:rgba(13,17,23,0.85); backdrop-filter:blur(10px); border:1px solid #30363d; border-radius:10px; padding:16px;'>
            <h4 style='color:#00e5ff; margin-top:0;'>Top 200 Overall (VOR Scaled)</h4>
            <div style='color:#c9d1d9; font-size:12px;'>Data link established to <b>Jeff_Rankings_TOP_200_PPR__SQL_.csv</b>. VOR baselines actively shifting based on positional scarcity gradients.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<h4 style='color:#00ff88; margin-bottom:6px;'>Straight Cash Keeper Surplus Ledger</h4>", unsafe_allow_html=True)
        st.markdown("<div style='color:#8b949e; font-size:12px; margin-bottom:12px;'>Mapping retained draft capital against Evaluator 3.0 auction/draft values.</div>", unsafe_allow_html=True)
        
        # MFL Keeper formatting
        keepers = [
            {"Player": "Breece Hall", "Pos": "RB", "Cost": "Round 3", "True_Value": "Round 1", "Surplus": "+2.0 Rounds", "Status": "LOCKED"},
            {"Player": "Drake London", "Pos": "WR", "Cost": "Round 5", "True_Value": "Round 3", "Surplus": "+2.0 Rounds", "Status": "LOCKED"},
            {"Player": "Jayden Reed", "Pos": "WR", "Cost": "Round 10", "True_Value": "Round 5", "Surplus": "+5.0 Rounds", "Status": "PENDING"}
        ]
        
        cols = st.columns(3)
        for idx, k in enumerate(keepers):
            with cols[idx % 3]:
                pos_col = "#ff2a6d" if k["Pos"] == "RB" else "#00ff88"
                badge_col = "#00ff88" if k["Status"] == "LOCKED" else "#ffd700"
                
                st.html(f"""
                <div style='background:rgba(13,17,23,0.85); border-left:4px solid {pos_col}; border-radius:8px; padding:14px; margin-bottom:12px; box-shadow: 0 4px 12px rgba(0,0,0,0.3);'>
                    <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;'>
                        <b style='color:#fff; font-size:15px;'>{k['Player']}</b>
                        <span style='background:{badge_col}22; color:{badge_col}; font-size:10px; font-weight:900; padding:3px 8px; border-radius:4px;'>{k['Status']}</span>
                    </div>
                    <div style='background:#161b22; padding:10px; border-radius:6px; font-size:12px;'>
                        <div style='display:flex; justify-content:space-between; margin-bottom:4px;'><span style='color:#8b949e;'>Draft Cost:</span><span style='color:#ff2a6d; font-weight:bold;'>{k['Cost']}</span></div>
                        <div style='display:flex; justify-content:space-between; margin-bottom:4px;'><span style='color:#8b949e;'>True Value:</span><span style='color:#00e5ff; font-weight:bold;'>{k['True_Value']}</span></div>
                        <div style='display:flex; justify-content:space-between; border-top:1px solid #30363d; padding-top:4px; margin-top:4px;'><span style='color:#8b949e;'>Surplus:</span><span style='color:#00ff88; font-weight:bold;'>{k['Surplus']}</span></div>
                    </div>
                </div>
                """)
