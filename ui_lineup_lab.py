import streamlit as st
import data_service
import address_book

def render_lineup_lab_tab():
    st.markdown("<h2 style='color:#ffd700; margin-bottom:2px;'>🧪 DFS LAB & TACTICAL WORKBENCH</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color:#8b949e; font-size:12px; margin-bottom:14px;'>Horizontal Test-Tube Racks • Nested Capsule Pills • Fantastic Four Anchors</div>", unsafe_allow_html=True)

    if "dfs_lab_slate" not in st.session_state: st.session_state["dfs_lab_slate"] = "Showdown (6 Spots)"
    if "dfs_lab_type" not in st.session_state: st.session_state["dfs_lab_type"] = "🏆 GPP (150 MME)"

    c_slate, c_type, c_btn = st.columns([1.5, 1.5, 1])
    with c_slate:
        slate = st.radio("Slate Architecture", ["Showdown (6 Spots)", "Sunday Classic Main (9 Spots)"], horizontal=True, key="lab_slate")
    with c_type:
        ctype = st.radio("Contest Target", ["🏆 GPP (150 MME)", "🛡️ Cash Games (25 High-Floor)"], horizontal=True, key="lab_type")
    with c_btn:
        st.button("📥 Export CSV", use_container_width=True)

    st.markdown("""
    <style>
        .test-tube-rack { background: rgba(13, 17, 23, 0.85); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 12px 16px; margin-bottom: 14px; }
        .tube-header { display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 6px; margin-bottom: 8px; font-size: 12px; }
        .pill-container { display: flex; flex-direction: row; gap: 6px; width: 100%; }
        .player-pill { flex: 1; background: #161b22; border-radius: 8px; padding: 6px 8px; display: flex; flex-direction: column; font-size: 11px; border-top: 3px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

    lineups = data_service.get_dfs_lab_lineups(slate, ctype)
    
    for lu in lineups:
        pills_html = ""
        for p in lu["pills"]:
            # Standardized dictionary access (No tuple crashes)
            pos_col = "#ffd700" if p["pos"]=="CPT" else ("#00e5ff" if p["pos"]=="QB" else ("#ff2a6d" if "RB" in p["pos"] else ("#00ff88" if "WR" in p["pos"] else "#a55eea")))
            core_fx = "border: 1.5px solid #00ff88; box-shadow: 0 0 8px rgba(0,255,136,0.2);" if p["core"] else ""
            
            pills_html += f"""
            <div class='player-pill' style='border-top: 3px solid {pos_col}; {core_fx}'>
                <div style='display:flex; justify-content:space-between;'><b style='color:{pos_col};'>{p["pos"]}</b></div>
                <div style='font-weight:700; color:#fff; margin:2px 0;'>{p["name"]}</div>
                <div style='display:flex; justify-content:space-between; color:#8b949e;'><span>{p["sal"]}</span><b style='color:#00ff88;'>{p["pts"]}</b></div>
            </div>
            """
        
        st.html(f"""
        <div class='test-tube-rack'>
            <div class='tube-header'>
                <div><b style='color:#00e5ff;'>ROSTER {lu['id']}</b> • Cap: <b>${lu['salary']:,}</b> • ⚡ {lu['script']}</div>
                <div><span style='color:#8b949e;'>Ceiling:</span> <b style='color:#00ff88; font-size:14px;'>{lu['ceiling']} pts</b></div>
            </div>
            <div class='pill-container'>{pills_html}</div>
        </div>
        """)
