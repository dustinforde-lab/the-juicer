import streamlit as st
import data_service

def get_positional_showdown_data():
    return [
        {"Player": "Jordan Love", "Pos": "QB", "Salary": 10200, "Mike_Base": 19.8, "Sim_Ceiling": 31.5, "Sim_Floor": 12.0, "Delta": +11.7, "Tier": "Tier 1: Core Smash", "Status": "ACTIVE", "Wire": "Full playbook clearance."},
        {"Player": "Bijan Robinson", "Pos": "RB", "Salary": 10800, "Mike_Base": 21.4, "Sim_Ceiling": 32.8, "Sim_Floor": 14.2, "Delta": +11.4, "Tier": "Tier 1: Core Smash", "Status": "ACTIVE", "Wire": "Mismatch vs GB linebackers."},
        {"Player": "Jayden Reed", "Pos": "WR", "Salary": 8600, "Mike_Base": 14.6, "Sim_Ceiling": 27.4, "Sim_Floor": 6.8, "Delta": +12.8, "Tier": "Tier 2: GPP Ceiling", "Status": "ACTIVE", "Wire": "Primary slot duties and motion."},
        {"Player": "MarShawn Lloyd", "Pos": "RB", "Salary": 4800, "Mike_Base": 4.1, "Sim_Ceiling": 10.5, "Sim_Floor": 1.0, "Delta": +6.4, "Tier": "Tier 5: Trap Chalk", "Status": "QUESTIONABLE", "Wire": "Battling groin/ankle injuries; rough Week 1 outing."},
        {"Player": "Younghoe Koo", "Pos": "K", "Salary": 4400, "Mike_Base": 8.8, "Sim_Ceiling": 15.0, "Sim_Floor": 4.0, "Delta": +6.2, "Tier": "Tier 3: Floor Anchor", "Status": "ACTIVE", "Wire": "Falcons 46% stall rate projects 2.4 FGs."}
    ]

def render_the_rankings():
    st.markdown("<h2 style='color:#00ff88; margin-bottom:2px;'>⚡ THE RANKINGS & EVALUATOR 3.0 WAR ROOM</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color:#8b949e; font-size:12px; margin-bottom:14px;'>Dual Glassmorphic Desk • Top 300 Board • Positional Showdown Desk • Zero-Latency Drawers</div>", unsafe_allow_html=True)

    if "rankings_slate" not in st.session_state: st.session_state["rankings_slate"] = "Primetime Showdown"
    st.session_state["rankings_slate"] = st.radio("Rankings Slate Mode", ["Primetime Showdown", "Sunday Classic Main"], horizontal=True, key="rnk_rad")

    st.markdown("""<style>
        details { background: rgba(22, 27, 34, 0.85); border: 1px solid #30363d; border-radius: 8px; margin-bottom: 10px; padding: 10px 14px; box-shadow: 0 4px 10px rgba(0,0,0,0.4); transition: all 0.2s; }
        details[open] { border-color: #00ff88; background: rgba(13, 17, 23, 0.95); }
        summary { font-weight: 700; cursor: pointer; list-style: none; display: flex; justify-content: space-between; align-items: center; }
        summary::-webkit-details-marker { display: none; }
    </style>""", unsafe_allow_html=True)

    col_l, col_r = st.columns([1.05, 1.15])
    with col_l:
        st.markdown("<h4 style='color:#00ff88; margin-bottom:6px;'>🏆 SLATE TOP 300 BOARD</h4>", unsafe_allow_html=True)
        df_300 = data_service.get_slate_master_300(st.session_state["rankings_slate"])
        st.dataframe(df_300, use_container_width=True, height=580, hide_index=True)
    
    with col_r:
        st.markdown("<h4 style='color:#00e5ff; margin-bottom:6px;'>🎯 SHOWDOWN DESK & RECON</h4>", unsafe_allow_html=True)
        pos_tabs = st.radio("Positional Filter", ["ALL", "QB", "RB", "WR", "TE", "K", "DST"], horizontal=True)
        showdown_players = get_positional_showdown_data()
        if pos_tabs != "ALL": showdown_players = [p for p in showdown_players if p["Pos"] == pos_tabs]

        for p in showdown_players:
            tier_col = "#00ff88" if "Tier 1" in p["Tier"] else ("#00e5ff" if "Tier 2" in p["Tier"] else ("#ffd700" if "Tier 3" in p["Tier"] else "#ff4757"))
            pos_col = "#00e5ff" if p["Pos"]=="QB" else ("#ff2a6d" if p["Pos"]=="RB" else ("#00ff88" if p["Pos"]=="WR" else ("#ffd700" if p["Pos"]=="TE" else ("#ff9f43" if p["Pos"]=="K" else "#a55eea"))))
            stat_col = "#00ff88" if p["Status"] == "ACTIVE" else "#ffa502"
            badge = f"<span style='background:{stat_col}22; color:{stat_col}; font-size:10px; padding:2px 6px; border-radius:4px;'>{p['Status']}</span>"
            
            st.html(f"""
            <details><summary>
                <div><b style='color:#fff; font-size:14px;'>{p['Player']}</b><span style='background:{pos_col}22; color:{pos_col}; font-size:10px; padding:2px 6px; border-radius:4px; margin-left:6px;'>{p['Pos']}</span><span style='color:#8b949e; font-size:12px; margin-left:8px;'>${p['Salary']:,}</span> <span style='margin-left:6px;'>{badge}</span></div>
                <div style='text-align:right;'><span style='font-size:11px; color:#8b949e;'>Ceil:</span> <b style='color:{tier_col}; font-size:14px;'>{p['Sim_Ceiling']}</b></div>
            </summary>
            <div style='margin-top:12px; padding-top:10px; border-top:1px solid rgba(255,255,255,0.06); font-size:11px;'>
                <div style='display:flex; justify-content:space-between; margin-bottom:8px;'>
                    <span><b>Mike Base xFP:</b> <span style='color:#fff;'>{p['Mike_Base']:.1f}</span></span>
                    <span><b>Sim Floor:</b> <span style='color:#fff;'>{p['Sim_Floor']:.1f}</span></span>
                    <span><b>Delta:</b> <b style='color:#00ff88;'>+{p['Delta']:.1f}</b></span>
                </div>
                <div style='background:#0d1117; border-left:4px solid #00e5ff; border-radius:4px; padding:8px 10px; color:#c9d1d9;'><b style='color:#00e5ff;'>⚡ ESPN/Sleeper Wire:</b> {p['Wire']}</div>
            </div></details>
            """)
