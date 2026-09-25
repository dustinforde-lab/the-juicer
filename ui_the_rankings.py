# -*- coding: utf-8 -*-
import streamlit as st
import data_service

def get_positional_showdown_data():
    return [
        {"Player": "Jordan Love", "Pos": "QB", "Salary": 10200, "Mike_Base": 19.8, "Sim_Ceiling": 31.5, "Sim_Floor": 12.0, "Delta": +11.7, "Tier": "Tier 1: Core Smash", "Status": "ACTIVE", "Wire": "Full playbook clearance. Deep boundaries open."},
        {"Player": "Bijan Robinson", "Pos": "RB", "Salary": 10800, "Mike_Base": 21.4, "Sim_Ceiling": 32.8, "Sim_Floor": 14.2, "Delta": +11.4, "Tier": "Tier 1: Core Smash", "Status": "ACTIVE", "Wire": "Clear mismatch vs Green Bay linebackers."},
        {"Player": "Jayden Reed", "Pos": "WR", "Salary": 8600, "Mike_Base": 14.6, "Sim_Ceiling": 27.4, "Sim_Floor": 6.8, "Delta": +12.8, "Tier": "Tier 2: GPP Ceiling", "Status": "ACTIVE", "Wire": "Primary slot duties and motion active."}
    ]

def render_the_rankings():
    st.markdown("<h2 style='color:#00ff88; margin-bottom:2px;'>⚡ THE RANKINGS & EVALUATOR 3.0 WAR ROOM</h2>", unsafe_allow_html=True)
    timestamps = data_service.get_last_pulse()
    st.markdown(f"<div style='color:#8b949e; font-size:12px; margin-bottom:14px;'>Infinite Scroll Assets &bull; Massive Showdown Recon &bull; ⏱️ Data Synced: {timestamps['espn']}</div>", unsafe_allow_html=True)

    if "rankings_slate" not in st.session_state: st.session_state["rankings_slate"] = "Primetime Showdown"
    st.session_state["rankings_slate"] = st.radio("Rankings Slate Mode", ["Primetime Showdown", "Sunday Classic Main"], horizontal=True, key="rnk_rad")

    st.markdown("""<style>
        details { background: rgba(22, 27, 34, 0.85); border: 1px solid #30363d; border-radius: 10px; margin-bottom: 14px; padding: 14px 18px; box-shadow: 0 6px 14px rgba(0,0,0,0.4); transition: all 0.2s; }
        details[open] { border-color: #00ff88; background: rgba(13, 17, 23, 0.95); }
        summary { font-weight: 700; cursor: pointer; list-style: none; display: flex; justify-content: space-between; align-items: center; }
        summary::-webkit-details-marker { display: none; }
    </style>""", unsafe_allow_html=True)

    col_l, col_r = st.columns([1.0, 1.2])
    with col_l:
        st.markdown("<h4 style='color:#00ff88; margin-bottom:6px;'>🏆 SLATE TOP 300 BOARD</h4>", unsafe_allow_html=True)
        df_300 = data_service.get_slate_master_300(st.session_state["rankings_slate"])
        
        feed_html = "<div style='height: 650px; overflow-y: auto; scrollbar-width: thin; padding-right: 10px;'>"
        for idx, row in df_300.iterrows():
            pos = row['Pos']
            pos_col = "#00e5ff" if pos=="QB" else ("#ff2a6d" if pos=="RB" else ("#00ff88" if pos=="WR" else ("#ffd700" if pos=="TE" else ("#ff9f43" if pos=="K" else "#a55eea"))))
            feed_html += f"""
            <div style='background:rgba(13,17,23,0.75); border:1px solid rgba(255,255,255,0.08); border-top:4px solid {pos_col}; border-radius:8px; padding:14px; margin-bottom:12px;'>
                <div style='display:flex; justify-content:space-between;'>
                    <div><b style='color:#fff; font-size:15px;'>{row['Player']}</b> <span style='color:#8b949e; font-size:11px;'>{row['Team']}</span></div>
                    <div style='background:{pos_col}22; color:{pos_col}; font-weight:900; font-size:11px; padding:2px 8px; border-radius:4px;'>{pos}</div>
                </div>
                <div style='display:flex; justify-content:space-between; margin-top:8px; font-size:12px;'>
                    <span style='color:#8b949e;'>Sal: <b style='color:#fff;'>${row['Salary']:,}</b></span>
                    <span style='color:#8b949e;'>Base: <b style='color:#00ff88;'>{row['Mike_PPR']}</b></span>
                    <span style='color:#8b949e;'>Val: <b style='color:#ffd700;'>{row['Value']}x</b></span>
                </div>
            </div>"""
        feed_html += "</div>"
        st.html(feed_html)
    
    with col_r:
        st.markdown("<h4 style='color:#00e5ff; margin-bottom:6px;'>🎯 SHOWDOWN DESK & RECON</h4>", unsafe_allow_html=True)
        pos_tabs = st.radio("Positional Filter", ["ALL", "QB", "RB", "WR", "TE", "K", "DST"], horizontal=True)
        showdown_players = get_positional_showdown_data()
        if pos_tabs != "ALL": showdown_players = [p for p in showdown_players if p["Pos"] == pos_tabs]

        for p in showdown_players:
            tier_col = "#00ff88" if "Tier 1" in p["Tier"] else ("#00e5ff" if "Tier 2" in p["Tier"] else ("#ffd700" if "Tier 3" in p["Tier"] else "#ff4757"))
            pos_col = "#00e5ff" if p["Pos"]=="QB" else ("#ff2a6d" if p["Pos"]=="RB" else ("#00ff88" if p["Pos"]=="WR" else ("#ffd700" if p["Pos"]=="TE" else ("#ff9f43" if p["Pos"]=="K" else "#a55eea"))))
            badge = f"<span style='background:#00ff8822; color:#00ff88; font-size:11px; padding:3px 8px; border-radius:6px;'>{p['Status']}</span>"
            
            st.html(f"""
            <details><summary>
                <div><b style='color:#fff; font-size:17px;'>{p['Player']}</b><span style='background:{pos_col}22; color:{pos_col}; font-size:12px; padding:3px 8px; border-radius:6px; margin-left:8px;'>{p['Pos']}</span><span style='color:#8b949e; font-size:14px; margin-left:10px;'>${p['Salary']:,}</span> <span style='margin-left:10px;'>{badge}</span></div>
                <div style='text-align:right;'><span style='font-size:12px; color:#8b949e;'>Ceiling:</span> <b style='color:{tier_col}; font-size:18px;'>{p['Sim_Ceiling']}</b></div>
            </summary>
            <div style='margin-top:14px; padding-top:12px; border-top:1px solid rgba(255,255,255,0.08); font-size:13px;'>
                <div style='display:flex; justify-content:space-between; margin-bottom:12px;'>
                    <span><b>Mike Base xFP:</b> <span style='color:#fff;'>{p['Mike_Base']:.1f}</span></span>
                    <span><b>Sim Floor:</b> <span style='color:#fff;'>{p['Sim_Floor']:.1f}</span></span>
                    <span><b>Delta:</b> <b style='color:#00ff88;'>+{p['Delta']:.1f}</b></span>
                </div>
                <div style='background:#0d1117; border-left:5px solid #00e5ff; border-radius:6px; padding:12px 14px; color:#c9d1d9; font-size:14px;'><b style='color:#00e5ff;'>⚡ Donna's Recon Read:</b> {p['Wire']}</div>
            </div></details>
            """)
