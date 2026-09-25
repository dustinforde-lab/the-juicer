import streamlit as st

def render_film_room():
    st.markdown("<h2 style='color:#a55eea; margin-bottom:2px;'>🎥 FILM ROOM & QUANTITATIVE LAB</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color:#8b949e; font-size:12px; margin-bottom:16px;'>Coverage Shells • Defensive Tendencies • Dynamic Kelly Unit Sizing Model</div>", unsafe_allow_html=True)

    tab_film, tab_kelly = st.tabs(["🛡️ Scheme & Coverage Tendencies", "📐 Kelly Criterion Unit Allocation"])

    with tab_film:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
            <div style='background:rgba(13,17,23,0.85); border-left:6px solid #00e5ff; border-radius:10px; padding:16px; margin-bottom:14px;'>
                <h4 style='color:#00e5ff; margin-top:0;'>🛡️ Green Bay Defensive Shell</h4>
                <div style='font-size:12px; color:#c9d1d9; line-height:1.6;'>
                    • <b>Primary Shell:</b> Cover-3 / Quarters split (72% on early downs).<br>
                    • <b>Mismatch:</b> RB checkdown funnel; Bijan Robinson grade: <b style='color:#00ff88;'>A+</b>.<br>
                    • <b>Slot Flaw:</b> 8.4 yards per target allowed to inside crossers.
                </div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("""
            <div style='background:rgba(13,17,23,0.85); border-left:6px solid #ff2a6d; border-radius:10px; padding:16px; margin-bottom:14px;'>
                <h4 style='color:#ff2a6d; margin-top:0;'>⚔️ Atlanta Falcons Scheme Trajectory</h4>
                <div style='font-size:12px; color:#c9d1d9; line-height:1.6;'>
                    • <b>Pace of Play:</b> Top 8 neutral-script hurry-up velocity.<br>
                    • <b>Target Funnel:</b> Drake London commands 31% third-down share.<br>
                    • <b>Red Zone Stall:</b> 46% drive stall rate (elevates Younghoe Koo).
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab_kelly:
        st.markdown("<h4 style='color:#ffd700; margin-bottom:6px;'>Dynamic Kelly Criterion Sizing (Relocated)</h4>", unsafe_allow_html=True)
        st.markdown("<div style='color:#8b949e; font-size:12px; margin-bottom:12px;'>Mathematical bankroll allocation based on detected model edge vs bookmaker vig.</div>", unsafe_allow_html=True)
        k1, k2, k3 = st.columns(3)
        k1.metric("Recommended Unit Size", "0.75 Units", "Conservative Quarter-Kelly")
        k2.metric("Edge Threshold", "+4.8% EV", "Over Sportsbook Vig")
        k3.metric("Max Allocation Cap", "2.0 Units", "Risk Protection Active")
