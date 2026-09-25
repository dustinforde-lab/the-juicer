import streamlit as st
import pandas as pd

def calc_ppr(row):
    pos = row.get("Pos", "")
    if pos == "K":
        return round(row.get("FGM", 2.1) * 3.0 + row.get("FG50", 0.4) * 2.0 + row.get("XPM", 2.6) * 1.0, 2)
    if pos == "DST":
        return round(row.get("Sacks", 3.0) * 1.0 + row.get("Turnovers", 1.4) * 2.0 + row.get("DefTD", 0.15) * 6.0 + max(0, 10.0 - (row.get("PtsAllowed", 21) * 0.3)), 2)
    
    pts = (row.get("PassYds", 0) / 25.0) + (row.get("RushYds", 0) / 10.0) + (row.get("RecYds", 0) / 10.0) + (row.get("Rec", 0) * 1.0)
    pts += (row.get("PassTD", 0) * 4.0) + (row.get("RushTD", 0) * 6.0) + (row.get("RecTD", 0) * 6.0)
    return round(pts, 2)

BASE_SEED = [
    {"Player": "Josh Allen", "Pos": "QB", "Team": "BUF", "Opp": "MIA", "PassYds": 268, "PassTD": 2.1, "RushYds": 38, "RushTD": 0.5, "Rec": 0, "RecYds": 0, "VegasProp": "254.5 Pass Yds", "Edge": "+5.3%"},
    {"Player": "Breece Hall", "Pos": "RB", "Team": "NYJ", "Opp": "NE", "PassYds": 0, "PassTD": 0, "RushYds": 82, "RushTD": 0.8, "Rec": 4.8, "RecYds": 38, "VegasProp": "67.5 Rush Yds", "Edge": "+21.5%"},
    {"Player": "Justin Jefferson", "Pos": "WR", "Team": "MIN", "Opp": "GB", "PassYds": 0, "PassTD": 0, "RushYds": 0, "RushTD": 0.0, "Rec": 7.4, "RecYds": 98, "VegasProp": "84.5 Rec Yds", "Edge": "+16.0%"},
    {"Player": "Travis Kelce", "Pos": "TE", "Team": "KC", "Opp": "LAC", "PassYds": 0, "PassTD": 0, "RushYds": 0, "RushTD": 0.0, "Rec": 5.6, "RecYds": 64, "VegasProp": "56.5 Rec Yds", "Edge": "+13.3%"},
    {"Player": "Brandon Aubrey", "Pos": "K", "Team": "DAL", "Opp": "NYG", "FGM": 2.4, "FG50": 0.8, "XPM": 2.8, "VegasProp": "1.5 FGM", "Edge": "+14.0%"},
    {"Player": "Minnesota Vikings", "Pos": "DST", "Team": "MIN", "Opp": "GB", "Sacks": 3.4, "Turnovers": 1.5, "DefTD": 0.2, "PtsAllowed": 19, "VegasProp": "2.5 Sacks", "Edge": "+14.0%"}
]

def get_juice_data():
    df = pd.DataFrame(BASE_SEED)
    df["Full PPR"] = df.apply(calc_ppr, axis=1)
    df = df.sort_values(by="Full PPR", ascending=False).reset_index(drop=True)
    df["Rank"] = df.index + 1
    return df

POSITION_CAPS = {"QB": 32, "RB": 50, "WR": 75, "TE": 35, "K": 32, "DST": 32}

def render():
    st.markdown("<h2 style='color:#ffd700; margin-bottom:2px;'>⚡ JUICE RANKINGS & BENCHMARK DESK</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color:#8b949e; font-size:12px; margin-bottom:14px;'>Mike Projections • Monte Carlo Constraint • Positional Caps</div>", unsafe_allow_html=True)
    
    try:
        df = get_juice_data()
    except Exception as e:
        st.error(f"Data Pipeline Error: {e}")
        return
        
    pos_colors = {"QB": "#00e5ff", "RB": "#ff2a6d", "WR": "#00ff88", "TE": "#ffd700", "K": "#ff9f43", "DST": "#a55eea"}
    
    p_names = df["Player"].tolist()
    sel_player = st.selectbox("🔍 INSPECT PLAYER CARD / STAT LINE:", p_names, index=0)
    p = df[df["Player"] == sel_player].iloc[0]
    p_col = pos_colors.get(p["Pos"], "#00e5ff")
    
    st.html(f"""
    <div style='background:#0d1117; border:1px solid {p_col}66; border-left:6px solid {p_col}; border-radius:10px; padding:12px 16px; margin-bottom:14px; box-shadow:0 4px 16px rgba(0,0,0,0.5);'>
        <div style='display:flex; justify-content:space-between; align-items:center;'>
            <div>
                <span style='font-size:16px; font-weight:900; color:#ffffff;'>{p["Player"]}</span>
                <span style='background:{p_col}22; color:{p_col}; font-size:11px; font-weight:800; padding:2px 8px; border-radius:4px; margin-left:6px;'>{p["Pos"]}</span>
                <span style='color:#8b949e; font-size:12px; margin-left:6px;'>{p.get("Team", "UNK")} vs {p.get("Opp", "UNK")}</span>
            </div>
            <div style='text-align:right;'>
                <span style='color:#8b949e; font-size:11px;'>Full PPR Projection:</span>
                <span style='color:#00ff88; font-size:16px; font-weight:900; margin-left:6px;'>{p.get("Full PPR", 0):.2f} pts</span>
            </div>
        </div>
        <div style='display:flex; flex-wrap:wrap; gap:8px; margin-top:10px;'>
            <div style='background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:6px; padding:4px 10px; font-size:11px;'>
                <span style='color:#8b949e;'>Pass:</span> <b style='color:#ffffff;'>{p.get("PassYds", 0)} yds | {p.get("PassTD", 0)} TD</b>
            </div>
            <div style='background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:6px; padding:4px 10px; font-size:11px;'>
                <span style='color:#8b949e;'>Rush:</span> <b style='color:#ffffff;'>{p.get("RushYds", 0)} yds | {p.get("RushTD", 0)} TD</b>
            </div>
            <div style='background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:6px; padding:4px 10px; font-size:11px;'>
                <span style='color:#8b949e;'>Rec:</span> <b style='color:#ffffff;'>{p.get("Rec", 0)} rec | {p.get("RecYds", 0)} yds</b>
            </div>
            <div style='background:rgba(0,255,136,0.1); border:1px solid rgba(0,255,136,0.3); border-radius:6px; padding:4px 10px; font-size:11px;'>
                <span style='color:#cad3df;'>Prop: <b>{p.get("VegasProp", "N/A")}</b></span>
                <span style='color:#00ff88; font-weight:bold; margin-left:6px;'>Edge: {p.get("Edge", "0.0%")}</span>
            </div>
        </div>
    </div>
    """)
    
    col_master, col_pos = st.columns([0.42, 0.58])
    with col_master:
        st.markdown("<h4 style='color:#00e5ff; margin-bottom:8px;'>MASTER TOP 300 (PPR)</h4>", unsafe_allow_html=True)
        m_display = df[["Rank", "Player", "Pos", "Team", "Full PPR", "Edge"]].copy()
        st.dataframe(m_display, use_container_width=True, height=520, hide_index=True)
        
    with col_pos:
        pos_tabs = ["QB", "RB", "WR", "TE", "K", "DST"]
        selected_pos = st.radio("POSITION FILTER:", pos_tabs, horizontal=True)
        
        cap = POSITION_CAPS.get(selected_pos, 50)
        pos_df = df[df["Pos"] == selected_pos].copy().reset_index(drop=True)
        pos_df["Pos Rank"] = pos_df.index + 1
        pos_df = pos_df.head(cap)
        
        st.markdown(f"<h4 style='color:#00ff88; margin-bottom:8px;'>TOP {selected_pos} BENCHMARK</h4>", unsafe_allow_html=True)
        
        if selected_pos in ["K"]:
            p_cols = ["Pos Rank", "Player", "Team", "Opp", "FGM", "FG50", "XPM", "Full PPR", "Edge"]
        elif selected_pos in ["DST"]:
            p_cols = ["Pos Rank", "Player", "Team", "Opp", "Sacks", "Turnovers", "PtsAllowed", "Full PPR", "Edge"]
        else:
            p_cols = ["Pos Rank", "Player", "Team", "Opp", "PassYds", "RushYds", "Rec", "RecYds", "Full PPR", "Edge"]
            
        valid_cols = [c for c in p_cols if c in pos_df.columns]
        st.dataframe(pos_df[valid_cols], use_container_width=True, height=480, hide_index=True)
