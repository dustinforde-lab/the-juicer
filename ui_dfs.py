# -*- coding: utf-8 -*-
import streamlit as st
import data_service

def render_dfs_tab():
    st.markdown("<h2 style='color:#00ff88; margin-bottom:2px;'>🧬 DFS ENGINE: EVALUATOR OUTPUTS</h2>", unsafe_allow_html=True)
    telemetry = data_service.get_full_telemetry_timestamps()
    st.markdown(f"<div style='color:#8b949e; font-size:12px; margin-bottom:14px;'>Pre-Made Evaluator 3.0 Lineups &bull; ⏱️ Status: {telemetry['odds_badge']}</div>", unsafe_allow_html=True)

    if "dfs_engine_slate" not in st.session_state: st.session_state["dfs_engine_slate"] = "Showdown (1 CPT, 5 FLEX)"
    st.session_state["dfs_engine_slate"] = st.radio("Slate Architecture", ["Showdown (1 CPT, 5 FLEX)", "Sunday Classic Main (9-Man)"], horizontal=True)

    lineups = data_service.get_premade_dfs_lineups(st.session_state["dfs_engine_slate"])
    
    for lu in lineups:
        pills_html = ""
        for p in lu["roster"]:
            pills_html += f"""
            <div style='flex:1; min-width:140px; background:#161b22; border-top:4px solid {p['color']}; padding:10px 12px; border-radius:8px; margin-right:8px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);'>
                <div style='display:flex; justify-content:space-between; margin-bottom:4px;'><b style='color:{p['color']}; font-size:12px;'>{p['pos']}</b><span style='color:#8b949e; font-size:10px;'>💰 ${p['salary']:,}</span></div>
                <div style='font-weight:900; color:#fff; font-size:14px; margin-bottom:6px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;'>{p['name']}</div>
                <div style='display:flex; justify-content:space-between; font-size:10px;'>
                    <span title='Ceiling' style='color:#00ff88;'>⚡ 28.4</span>
                    <span title='Floor' style='color:#ff2a6d;'>🛡️ 12.1</span>
                </div>
            </div>
            """

        st.html(f"""
        <div style='background:rgba(13,17,23,0.85); backdrop-filter:blur(8px); border:1px solid #30363d; border-radius:12px; padding:18px; margin-bottom:18px;'>
            <div style='display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(255,255,255,0.08); padding-bottom:12px; margin-bottom:14px;'>
                <div>
                    <b style='color:#00ff88; font-size:18px;'>{lu['id']}</b> 
                    <span style='background:rgba(0,255,136,0.15); color:#00ff88; font-size:12px; font-weight:800; padding:4px 8px; border-radius:6px; margin-left:12px;'>{lu['type']}</span>
                </div>
                <div style='font-size:14px;'>
                    <span style='color:#8b949e; margin-right:16px;'>Rem Cap: <b style='color:#00e5ff;'>${lu['rem_salary']:,}</b></span>
                    <span style='color:#8b949e;'>Proj: <b style='color:#ffd700;'>{lu['proj']} xFP</b></span>
                </div>
            </div>
            <div style='display:flex; flex-direction:row; overflow-x:auto; width:100%; scrollbar-width:thin; padding-bottom:8px;'>{pills_html}</div>
        </div>
        """)
