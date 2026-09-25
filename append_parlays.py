
# --- APPENDED: PARLAY MATRIX DYNAMIC 2-TO-10 LEG DESK ---
def render_parlay_matrix():
    import streamlit as st
    import parlay_engine
    
    st.markdown("<h2 style='color:#00e5ff; margin-bottom:4px;'>⚡ PARLAY MATRIX & DISCREPANCY GENERATOR</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color:#8b949e; font-size:12px; margin-bottom:16px;'>2-to-10 Leg Variations • Mike Projections vs. Vegas Lines • Weighted in Donna's Learning Loop</div>", unsafe_allow_html=True)
    
    col_input, col_metric = st.columns([0.35, 0.65])
    with col_input:
        stake_amount = st.number_input("TICKET STAKE ($):", min_value=1.0, max_value=5000.0, value=20.0, step=5.0)
    with col_metric:
        st.html("""
        <div style='display:flex; gap:10px; margin-top:24px;'>
            <span style='background:rgba(0,255,136,0.12); color:#00ff88; border:1px solid rgba(0,255,136,0.3); padding:4px 10px; border-radius:4px; font-size:11px; font-weight:700;'>Punt Filter: ZERO PUNTS ACTIVE</span>
            <span style='background:rgba(0,229,255,0.12); color:#00e5ff; border:1px solid rgba(0,229,255,0.3); padding:4px 10px; border-radius:4px; font-size:11px; font-weight:700;'>Correlation Engine: SGP BOOST ENABLED</span>
        </div>
        """)
        
    slips = parlay_engine.generate_tiered_slips(stake=float(stake_amount))
    
    for s in slips:
        t_name = s["tier_name"]
        l_cnt = s["leg_count"]
        odds = s["american_odds"]
        payout = s["potential_payout"]
        c_badge = s["correlation_badge"]
        win_rate = s["sim_win_rate"]
        d_weight = s["donna_weight"]
        
        legs_html = ""
        for leg in s["legs"]:
            player = leg["player"]
            team = leg["team"]
            opp = leg["opponent"]
            stat = leg["stat"]
            m_line = leg["market_line"]
            proj = leg["mike_proj"]
            edge = leg["edge_pct"]
            conv = leg["conviction"]
            book = leg["book"]
            
            c_color = "#00ff88" if edge >= 14.0 else "#00e5ff"
            
            legs_html += f"""
            <div style='background:rgba(255,255,255,0.03); border-left:3px solid {c_color}; border-radius:4px; padding:8px 12px; margin-bottom:6px; display:flex; justify-content:space-between; align-items:center;'>
                <div>
                    <span style='color:#ffffff; font-weight:700; font-size:13px;'>{player}</span>
                    <span style='color:#8b949e; font-size:11px;'> ({team} vs {opp})</span>
                    <div style='color:#cad3df; font-size:11px; margin-top:2px;'><b>Over {m_line}</b> {stat} • <span style='color:#ffd700;'>{book}</span></div>
                </div>
                <div style='text-align:right;'>
                    <div style='color:{c_color}; font-weight:800; font-size:12px;'>Mike: {proj} ({edge:+}%)</div>
                    <span style='background:rgba(255,255,255,0.06); color:#cad3df; font-size:9px; padding:2px 6px; border-radius:3px;'>{conv}</span>
                </div>
            </div>
            """
            
        st.html(f"""
        <div style='background:#0d1117; border:1px solid rgba(0,229,255,0.25); border-radius:10px; padding:16px; margin-bottom:18px; box-shadow:0 4px 18px rgba(0,0,0,0.5);'>
            <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;'>
                <div>
                    <span style='color:#00e5ff; font-weight:900; font-size:15px;'>{t_name}</span>
                    <span style='background:rgba(0,229,255,0.1); color:#00e5ff; font-size:10px; padding:2px 8px; border-radius:4px; margin-left:8px; font-weight:700;'>{l_cnt} LEGS</span>
                    <span style='background:rgba(255,215,0,0.12); color:#ffd700; font-size:10px; padding:2px 8px; border-radius:4px; margin-left:6px; font-weight:700;'>{c_badge}</span>
                </div>
                <div style='text-align:right;'>
                    <span style='color:#8b949e; font-size:12px;'>Price: <b style='color:#ffffff;'>{odds}</b></span> | 
                    <span style='color:#8b949e; font-size:12px;'>Win Rate: <b style='color:#00ff88;'>{win_rate}</b></span>
                </div>
            </div>
            {legs_html}
            <div style='display:flex; justify-content:space-between; align-items:center; margin-top:12px; padding-top:10px; border-top:1px solid rgba(255,255,255,0.06); font-size:12px;'>
                <span style='color:#8b949e;'>🧠 Donna Learning Weight: <b style='color:#cad3df;'>{d_weight}</b></span>
                <span style='background:rgba(0,255,136,0.15); border:1px solid rgba(0,255,136,0.35); color:#00ff88; padding:4px 12px; border-radius:6px; font-weight:800; font-size:13px;'>Payout on ${stake_amount:.2f}:${payout:,.2f}</span>
            </div>
        </div>
        """)
