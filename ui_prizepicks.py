# -*- coding: utf-8 -*-
import streamlit as st
import data_service
from parlay_engine import validate_slip

def render_prizepicks():
    st.markdown("<h2 style='color:#ff2a6d; margin-bottom:2px;'>🎟️ PRIZEPICKS & UNDERDOG PROP SLIPS</h2>", unsafe_allow_html=True)
    timestamps = data_service.get_last_pulse()
    st.markdown(f"<div style='color:#8b949e; font-size:12px; margin-bottom:14px;'>Platform Rule Enforcement &bull; Break-Even Math &bull; ⏱️ Data Synced: {timestamps['odds']}</div>", unsafe_allow_html=True)

    if "pp_slate" not in st.session_state: st.session_state["pp_slate"] = "Sunday Classic Full Slate"
    
    c_tog, c_plat = st.columns([1.5, 2.5])
    with c_tog:
        st.session_state["pp_slate"] = st.radio("Props Slate Context", ["Showdown Primetime Props", "Sunday Classic Full Slate"], horizontal=True)
    with c_plat:
        platform_raw = st.radio("Platform Deck", ["PrizePicks (75 Slips)", "Underdog Fantasy (75 Slips)"], horizontal=True)

    platform_key = "prizepicks" if platform_raw.startswith("PrizePicks") else "underdog"
    slips = data_service.get_prop_slips(st.session_state["pp_slate"], "PrizePicks" if platform_key == "prizepicks" else "Underdog")
    
    border_accent = "#00e5ff" if platform_key == "prizepicks" else "#ffd700"

    cols = st.columns(2)
    for idx, slip in enumerate(slips):
        # 🚨 Hooking up the engine: Validate the slip in real-time
        # Convert tuple legs into dicts for the validator
        validation_payload = [{"team": leg[0], "prop": leg[2]} for leg in slip["legs"]]
        val_result = validate_slip(validation_payload, platform_key)
        
        # UI reacts to the validation math
        if val_result["valid"]:
            val_badge = f"<span style='color:#00ff88; font-weight:800;'>✅ Valid (BE: {val_result['break_even_pct']}%)</span>"
            border = f"1px solid #30363d; border-left: 5px solid {border_accent};"
        else:
            val_badge = f"<span style='color:#ff2a6d; font-weight:800;'>❌ INVALID: {val_result['errors'][0]}</span>"
            border = "1px dashed #ff2a6d; border-left: 5px solid #ff2a6d;"

        pills_html = ""
        for leg in slip["legs"]:
            pills_html += f"<div style='flex:0 0 auto; min-width:105px; background:#161b22; border-top:3px solid {leg[3]}; padding:6px 10px; border-radius:6px; margin-right:8px; font-size:11px;'><b style='color:#fff;'>{leg[0]}</b><br><span style='color:#00ff88; font-weight:800;'>{leg[1]}</span><br><span style='color:#8b949e; font-size:10px;'>{leg[2]}</span></div>"

        slip_html = f"""
        <div style='background:rgba(13,17,23,0.85); backdrop-filter:blur(8px); border:{border} border-radius:10px; padding:14px; margin-bottom:14px;'>
            <div style='display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(255,255,255,0.08); padding-bottom:8px; margin-bottom:10px;'>
                <div><span style='font-size:14px; font-weight:900; color:#fff;'>{slip['id']}</span> <span style='color:#8b949e; font-size:11px; margin-left:6px;'>&bull; {slip['title']}</span></div>
                <div><span style='background:rgba(0,255,136,0.15); color:#00ff88; font-weight:900; font-size:12px; padding:3px 8px; border-radius:4px;'>{slip['payout']}</span></div>
            </div>
            <div style='display:flex; flex-direction:row; overflow-x:auto; margin-bottom:10px; width:100%; scrollbar-width:thin; padding-bottom:4px;'>{pills_html}</div>
            <div style='font-size:11px; color:#8b949e; background:#0d1117; padding: 6px 10px; border-radius: 4px;'>{val_badge}</div>
        </div>"""
        with cols[idx % 2]: st.html(slip_html)
