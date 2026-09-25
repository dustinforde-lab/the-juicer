# -*- coding: utf-8 -*-
import streamlit as st
import data_service

def render_film_room():
    st.markdown("<h2 style='color:#a55eea; margin-bottom:2px;'>🎥 FILM ROOM & SCHEME RECON</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color:#8b949e; font-size:12px; margin-bottom:14px;'>Coverage Shells &bull; Defensive Tendencies &bull; Kelly Criterion Sizing</div>", unsafe_allow_html=True)

    tab_film, tab_kelly = st.tabs(["🛡️ Scheme & Coverage Tendencies", "📐 Kelly Criterion Unit Allocation"])

    with tab_film:
        st.markdown("<h4 style='color:#00e5ff; margin-bottom:12px;'>Defensive Shell Mismatches</h4>", unsafe_allow_html=True)
        mismatches = data_service.get_film_room_mismatches()
        
        cols = st.columns(3)
        for idx, match in enumerate(mismatches):
            with cols[idx % 3]:
                html = f"""
                <div style="background: rgba(13,17,23,0.85); backdrop-filter: blur(10px); border: 1px solid #30363d; border-top: 4px solid #a55eea; padding: 14px; border-radius: 8px; margin-bottom: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
                    <div style="color: #8b949e; font-size: 11px; margin-bottom: 4px; text-transform: uppercase; font-weight: 800;">Targeting: {match['defense']}</div>
                    <div style="color: #fff; font-size: 15px; font-weight: bold; margin-bottom: 8px;">{match['shell']}</div>
                    
                    <div style="background: #161b22; padding: 10px; border-radius: 6px; font-size: 12px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                            <span style="color: #8b949e;">Vulnerability:</span>
                            <span style="color: #ff2a6d; font-weight: bold;">{match['vulnerability']}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                            <span style="color: #8b949e;">Optimal Attack:</span>
                            <span style="color: #00ff88; font-weight: bold;">{match['target']}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between;">
                            <span style="color: #8b949e;">YPT Allowed:</span>
                            <span style="color: #ffd700; font-weight: bold;">{match['ypt_allowed']} yds</span>
                        </div>
                    </div>
                    <div style="margin-top: 10px; text-align: right;">
                        <span style="background: rgba(0,255,136,0.15); color: #00ff88; font-size: 11px; font-weight: 900; padding: 4px 8px; border-radius: 4px;">{match['edge']} MATCHUP EDGE</span>
                    </div>
                </div>
                """
                st.html(html)

    with tab_kelly:
        st.markdown("<h4 style='color:#ffd700; margin-bottom:6px;'>Dynamic Kelly Criterion Sizing</h4>", unsafe_allow_html=True)
        st.markdown("<div style='color:#8b949e; font-size:12px; margin-bottom:12px;'>Mathematical bankroll allocation based on detected model edge vs bookmaker vig.</div>", unsafe_allow_html=True)
        k1, k2, k3 = st.columns(3)
        k1.metric("Recommended Sizing Unit", "0.75 Units", "Conservative Quarter-Kelly")
        k2.metric("Detected Slate Edge", "+4.8% EV", "Over Sportsbook Vig")
        k3.metric("Max Roster Allocation", "2.0 Units", "Risk Protection Active")
