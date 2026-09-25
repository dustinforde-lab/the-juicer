# -*- coding: utf-8 -*-
import streamlit as st
import data_service

def render_lineup_lab_tab():
    st.markdown("<h2 style='color:#ffd700; margin-bottom:2px;'>🧪 DFS LAB: TACTICAL WORKBENCH</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color:#8b949e; font-size:12px; margin-bottom:14px;'>Master Player Pool &bull; Live Roster Compiler &bull; Salary Cap Math</div>", unsafe_allow_html=True)

    if "lab_slate" not in st.session_state: st.session_state["lab_slate"] = "Showdown"
    st.session_state["lab_slate"] = st.radio("Workbench Slate", ["Showdown", "Sunday Classic"], horizontal=True)

    col_pool, col_builder = st.columns([1.2, 1.8])
    
    with col_pool:
        st.markdown("<h4 style='color:#00e5ff; margin-bottom:6px;'>Player Pool</h4>", unsafe_allow_html=True)
        df = data_service.get_slate_master_300(st.session_state["lab_slate"])
        
        feed_html = "<div style='height: 600px; overflow-y: auto; scrollbar-width: thin; padding-right: 8px;'>"
        for _, row in df.iterrows():
            pos_col = "#00e5ff" if row['Pos']=="QB" else ("#ff2a6d" if row['Pos']=="RB" else ("#00ff88" if row['Pos']=="WR" else "#ffd700"))
            feed_html += f"""
            <div style='background:rgba(13,17,23,0.75); border:1px solid rgba(255,255,255,0.08); border-left:4px solid {pos_col}; border-radius:6px; padding:10px; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;'>
                <div>
                    <div style='color:#fff; font-size:13px; font-weight:bold;'>{row['Player']} <span style='color:{pos_col}; font-size:10px;'>{row['Pos']}</span></div>
                    <div style='color:#8b949e; font-size:11px;'>${row.get('Salary', 0):,} | xFP: <span style='color:#00ff88;'>{row.get('xFP', 0):.1f}</span></div>
                </div>
                <div style='background:#30363d; color:#fff; font-size:18px; font-weight:bold; width:28px; height:28px; display:flex; align-items:center; justify-content:center; border-radius:4px; cursor:pointer;'>+</div>
            </div>"""
        feed_html += "</div>"
        st.html(feed_html)

    with col_builder:
        st.markdown("<h4 style='color:#00ff88; margin-bottom:6px;'>Active Roster Compiler</h4>", unsafe_allow_html=True)
        
        st.html("""
        <div style='background:rgba(13,17,23,0.9); border:1px solid #30363d; border-radius:10px; padding:16px; margin-bottom:16px;'>
            <div style='display:flex; justify-content:space-between; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:10px; margin-bottom:12px;'>
                <div><span style='color:#8b949e; font-size:12px;'>Rem Cap:</span> <b style='color:#00ff88; font-size:18px;'>$50,000</b></div>
                <div><span style='color:#8b949e; font-size:12px;'>Avg Rem:</span> <b style='color:#00e5ff; font-size:18px;'>$8,333</b></div>
            </div>
            <div style='background:rgba(255,255,255,0.02); border:1px dashed #30363d; padding:12px; border-radius:6px; margin-bottom:8px; display:flex; justify-content:center; color:#8b949e; font-size:12px;'>Empty CPT Slot</div>
            <div style='background:rgba(255,255,255,0.02); border:1px dashed #30363d; padding:12px; border-radius:6px; margin-bottom:8px; display:flex; justify-content:center; color:#8b949e; font-size:12px;'>Empty FLEX Slot</div>
            <div style='background:rgba(255,255,255,0.02); border:1px dashed #30363d; padding:12px; border-radius:6px; margin-bottom:8px; display:flex; justify-content:center; color:#8b949e; font-size:12px;'>Empty FLEX Slot</div>
            <div style='background:rgba(255,255,255,0.02); border:1px dashed #30363d; padding:12px; border-radius:6px; margin-bottom:8px; display:flex; justify-content:center; color:#8b949e; font-size:12px;'>Empty FLEX Slot</div>
            <div style='background:rgba(255,255,255,0.02); border:1px dashed #30363d; padding:12px; border-radius:6px; margin-bottom:8px; display:flex; justify-content:center; color:#8b949e; font-size:12px;'>Empty FLEX Slot</div>
            <div style='background:rgba(255,255,255,0.02); border:1px dashed #30363d; padding:12px; border-radius:6px; display:flex; justify-content:center; color:#8b949e; font-size:12px;'>Empty FLEX Slot</div>
        </div>
        """)
