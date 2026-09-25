import re

new_ui_block = """
# --- RESTORED: ⚡ JUICE RANKINGS DUAL-TABLE & PILL INSPECTOR ---
def render_juice_rankings():
    import streamlit as st
    import juice_pipeline
    
    st.markdown("<h2 style='color:#ffd700; margin-bottom:2px;'>⚡ JUICE RANKINGS & BENCHMARK DESK</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color:#8b949e; font-size:12px; margin-bottom:14px;'>Mike Projections • Monte Carlo Constraint • Positional Caps (32 QB | 50 RB | 75 WR | 35 TE | 32 K | 32 DST)</div>", unsafe_allow_html=True)
    
    df = juice_pipeline.get_juice_data()
    pos_colors = {"QB": "#00e5ff", "RB": "#ff2a6d", "WR": "#00ff88", "TE": "#ffd700", "K": "#ff9f43", "DST": "#a55eea"}
    
    # 1. Selected Player "Pill Bottle" Inspector Card
    p_names = df["Player"].tolist()
    sel_player = st.selectbox("🔍 INSPECT PLAYER CARD / STAT LINE:", p_names, index=0)
    p = df[df["Player"] == sel_player].iloc[0]
    p_col = pos_colors.get(p["Pos"], "#00e5ff")
    
    st.html(f\"\"\"
    <div style='background:#0d1117; border:1px solid {p_col}66; border-left:6px solid {p_col}; border-radius:10px; padding:12px 16px; margin-bottom:14px; box-shadow:0 4px 16px rgba(0,0,0,0.5);'>
        <div style='display:flex; justify-content:space-between; align-items:center;'>
            <div>
                <span style='font-size:16px; font-weight:900; color:#ffffff;'>{p["Player"]}</span>
                <span style='background:{p_col}22; color:{p_col}; font-size:11px; font-weight:800; padding:2px 8px; border-radius:4px; margin-left:6px;'>{p["Pos"]}</span>
                <span style='color:#8b949e; font-size:12px; margin-left:6px;'>{p["Team"]} vs {p["Opp"]}</span>
            </div>
            <div style='text-align:right;'>
                <span style='color:#8b949e; font-size:11px;'>Full PPR Projection:</span>
                <span style='color:#00ff88; font-size:16px; font-weight:900; margin-left:6px;'>{p["Full PPR"]:.2f} pts</span>
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
    \"\"\")
    
    # 2. Side-by-Side Synchronized Tables
    col_master, col_pos = st.columns([0.42, 0.58])
    
    with col_master:
        st.markdown("<h4 style='color:#00e5ff; margin-bottom:8px;'>MASTER TOP 300 (FULL PPR)</h4>", unsafe_allow_html=True)
        m_display = df[["Rank", "Player", "Pos", "Team", "Full PPR", "Edge"]].copy()
        st.dataframe(m_display, use_container_width=True, height=520, hide_index=True)
        
    with col_pos:
        pos_tabs = ["QB", "RB", "WR", "TE", "K", "DST"]
        selected_pos = st.radio("POSITION FILTER:", pos_tabs, horizontal=True)
        
        pos_df = juice_pipeline.get_position_slice(df, selected_pos)
        st.markdown(f"<h4 style='color:#00ff88; margin-bottom:8px;'>TOP {juice_pipeline.POSITION_CAPS.get(selected_pos, 50)} {selected_pos} BENCHMARK</h4>", unsafe_allow_html=True)
        
        if selected_pos in ["K"]:
            p_cols = ["Pos Rank", "Player", "Team", "Opp", "FGM", "FG50", "XPM", "Full PPR", "Edge"]
        elif selected_pos in ["DST"]:
            p_cols = ["Pos Rank", "Player", "Team", "Opp", "Sacks", "Turnovers", "PtsAllowed", "Full PPR", "Edge"]
        else:
            p_cols = ["Pos Rank", "Player", "Team", "Opp", "PassYds", "RushYds", "Rec", "RecYds", "Full PPR", "Edge"]
            
        valid_cols = [c for c in p_cols if c in pos_df.columns]
        st.dataframe(pos_df[valid_cols], use_container_width=True, height=480, hide_index=True)
"""

with open("ui_components.py", "r", encoding="utf-8") as f:
    ui_code = f.read()

# Replace existing render_juice_rankings cleanly
ui_code = re.sub(r'def render_juice_rankings\(\):[\s\S]*?(?=def render_slip_card_html|def render_parlay_matrix|def render_prizepicks_desk|$)', new_ui_block + '\n\n', ui_code)

with open("ui_components.py", "w", encoding="utf-8") as f:
    f.write(ui_code)

print("✅ Successfully deployed Dual-Table & Pill Card Desk into ui_components.py")
