import sqlite3
import os
import json

DB_PATH = os.path.join(os.getcwd(), 'action_grid.db')

# --- 1. CLEAN UI_ADDRESSES.PY PATCH ---
ui_code = '''import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import pandas as pd
import json

def render_dfs_engine_tab():
    st.markdown("<h3 style='color: #eccc68; margin-bottom: 5px;'>👑 DFS 9-MAN LINEUPS (SIMULATED EDGE)</h3>", unsafe_allow_html=True)
    mode = st.radio("Select Construction Format:", ["CASH (50/50s) - Floor Focus", "GPP (Tournaments) - Ceiling & Stack Focus"], horizontal=True)
    db_mode = 'CASH' if 'CASH' in mode else 'GPP'
    
    try:
        with sqlite3.connect("action_grid.db") as conn:
            dfs = pd.read_sql(f"SELECT * FROM dfs_rosters WHERE lineup_type = '{db_mode}' ORDER BY projected_score DESC LIMIT 25", conn)
        if dfs.empty: 
            st.warning(f"No {db_mode} lineups found.")
            return
            
        for _, row in dfs.iterrows():
            proj = float(row.get('projected_score', 0))
            qb, rb1, rb2 = row.get('qb', ''), row.get('rb1', ''), row.get('rb2', '')
            wr1, wr2, wr3 = row.get('wr1', ''), row.get('wr2', ''), row.get('wr3', '')
            te, flex, dst = row.get('te', ''), row.get('flex', ''), row.get('dst', 'N/A')
            
            card_html = f"""
            <div style="background: rgba(20, 20, 30, 0.85); border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; padding: 16px; margin-bottom: 14px; font-family: -apple-system, sans-serif;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 6px;">
                    <div><span style="color: #2ed573; font-size: 12px; font-weight: bold; margin-right: 8px;">{db_mode} • DK</span><strong style="color: #f1f2f6;">OPTIMIZED 9-MAN LINEUP</strong></div>
                    <div style="text-align: right;"><span style="color: #2ed573; font-size: 18px; font-weight: bold;">{proj:.1f}</span><span style="color: #a4b0be; font-size: 11px; margin-left: 5px;">PROJ PTS</span></div>
                </div>
                <div style="display: flex; flex-wrap: wrap; gap: 6px;">
                    <div style="background: rgba(112, 161, 255, 0.1); border: 1px solid rgba(112, 161, 255, 0.2); border-radius: 6px; padding: 4px 8px; flex: 1; min-width: 95px;"><span style="color: #70a1ff; font-size: 10px; font-weight: bold; display: block;">QB 🎯</span><strong style="color: #f1f2f6; font-size: 12px;">{qb}</strong></div>
                    <div style="background: rgba(46, 213, 115, 0.1); border: 1px solid rgba(46, 213, 115, 0.2); border-radius: 6px; padding: 4px 8px; flex: 1; min-width: 95px;"><span style="color: #2ed573; font-size: 10px; font-weight: bold; display: block;">RB 🔥</span><strong style="color: #f1f2f6; font-size: 12px;">{rb1}</strong></div>
                    <div style="background: rgba(46, 213, 115, 0.1); border: 1px solid rgba(46, 213, 115, 0.2); border-radius: 6px; padding: 4px 8px; flex: 1; min-width: 95px;"><span style="color: #2ed573; font-size: 10px; font-weight: bold; display: block;">RB 🔥</span><strong style="color: #f1f2f6; font-size: 12px;">{rb2}</strong></div>
                    <div style="background: rgba(255, 71, 87, 0.1); border: 1px solid rgba(255, 71, 87, 0.2); border-radius: 6px; padding: 4px 8px; flex: 1; min-width: 95px;"><span style="color: #ff4757; font-size: 10px; font-weight: bold; display: block;">WR 📈</span><strong style="color: #f1f2f6; font-size: 12px;">{wr1}</strong></div>
                    <div style="background: rgba(255, 71, 87, 0.1); border: 1px solid rgba(255, 71, 87, 0.2); border-radius: 6px; padding: 4px 8px; flex: 1; min-width: 95px;"><span style="color: #ff4757; font-size: 10px; font-weight: bold; display: block;">WR 📈</span><strong style="color: #f1f2f6; font-size: 12px;">{wr2}</strong></div>
                    <div style="background: rgba(255, 71, 87, 0.1); border: 1px solid rgba(255, 71, 87, 0.2); border-radius: 6px; padding: 4px 8px; flex: 1; min-width: 95px;"><span style="color: #ff4757; font-size: 10px; font-weight: bold; display: block;">WR 📈</span><strong style="color: #f1f2f6; font-size: 12px;">{wr3}</strong></div>
                    <div style="background: rgba(255, 165, 2, 0.1); border: 1px solid rgba(255, 165, 2, 0.2); border-radius: 6px; padding: 4px 8px; flex: 1; min-width: 95px;"><span style="color: #ffa502; font-size: 10px; font-weight: bold; display: block;">TE ⚡</span><strong style="color: #f1f2f6; font-size: 12px;">{te}</strong></div>
                    <div style="background: rgba(164, 176, 190, 0.1); border: 1px solid rgba(164, 176, 190, 0.2); border-radius: 6px; padding: 4px 8px; flex: 1; min-width: 95px;"><span style="color: #a4b0be; font-size: 10px; font-weight: bold; display: block;">FLEX 🎯</span><strong style="color: #f1f2f6; font-size: 12px;">{flex}</strong></div>
                    <div style="background: rgba(87, 101, 116, 0.2); border: 1px solid rgba(87, 101, 116, 0.4); border-radius: 6px; padding: 4px 8px; flex: 1; min-width: 95px;"><span style="color: #c8d6e5; font-size: 10px; font-weight: bold; display: block;">DST 🛡️</span><strong style="color: #f1f2f6; font-size: 12px;">{dst}</strong></div>
                </div>
            </div>
            """
            components.html(card_html, height=155, scrolling=False)
    except Exception as e: 
        st.error(f"UI Error: {e}")

def render_rankings_tab():
    st.markdown("<h3 style='color: #eccc68;'>🏆 EVALUATION MASTER (1-POINT PPR)</h3>", unsafe_allow_html=True)
    with sqlite3.connect("action_grid.db") as conn:
        df = pd.read_sql("SELECT player_name, pos, team, ppr_baseline, pass_yds, pass_tds, rush_yds, rush_tds, rec, rec_yds, rec_tds FROM player_rankings WHERE ppr_baseline > 0 ORDER BY ppr_baseline DESC LIMIT 300", conn)
    
    st.dataframe(df[['player_name', 'pos', 'team', 'ppr_baseline']], use_container_width=True)
    
    st.markdown("#### 🔍 GRANULAR STAT PROJECTIONS")
    for _, r in df.head(15).iterrows():
        stats = []
        if r['pass_yds'] > 0: stats.append(f"{int(r['pass_yds'])} pass yds, {int(r['pass_tds'])} pass TD")
        if r['rush_yds'] > 0: stats.append(f"{int(r['rush_yds'])} rush yds, {int(r['rush_tds'])} rush TD")
        if r['rec'] > 0: stats.append(f"{int(r['rec'])} rec, {int(r['rec_yds'])} rec yds, {int(r['rec_tds'])} rec TD")
        stat_str = ", ".join(stats) if stats else "Defensive/Special Teams Simulator Base"
        st.markdown(f"**{r['player_name']}** ({r['pos']}) - **{r['ppr_baseline']} pts**")
        st.caption(stat_str)

def _render_slip_feed(platforms, title, color):
    st.markdown(f"<h3 style='color: {color};'>🎫 {title}</h3>", unsafe_allow_html=True)
    try:
        plat_format = "','".join(platforms)
        with sqlite3.connect("action_grid.db") as conn:
            df = pd.read_sql(f"SELECT * FROM slips WHERE platform IN ('{plat_format}') ORDER BY implied_probability DESC LIMIT 25", conn)
        if df.empty:
            st.warning(f"No {title} found.")
            return
        for _, row in df.iterrows():
            legs = json.loads(row.get('legs_json', '[]'))
            prob = float(row.get('implied_probability', 0.0)) * 100
            leg_pills = "".join([f'<span style="background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 4px 12px; margin: 3px; display: inline-block; font-size: 12px;"><b style="color: {"#2ed573" if l.get("direction", "OVER") == "OVER" else "#ff4757"};">{l.get("direction", "OVER")}</b> <span style="color: #f1f2f6;">{l.get("player_name", "Player")}</span> <span style="color: #a4b0be; font-size: 11px;">{l.get("line", "0")} {l.get("stat_category", "").replace("_", " ")}</span></span>' for l in legs])
            card_html = f'<div style="background: rgba(20, 20, 30, 0.85); border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; padding: 18px; margin-bottom: 14px; font-family: -apple-system, sans-serif;"><div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 8px;"><strong style="color: {color}; font-size: 16px;">{row.get("platform")} • {row.get("leg_count")} LEG</strong></div><div style="margin-bottom: 14px; display: flex; flex-wrap: wrap;">{leg_pills}</div><div style="display: flex; justify-content: space-between; font-size: 12px; color: #a4b0be; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 8px;"><span>Implied Win: <b style="color: #2ed573;">{prob:.1f}%</b></span></div></div>'
            components.html(card_html, height=140 + (len(legs) * 15), scrolling=False)
    except Exception as e:
        st.error(f"UI Error: {e}")

def render_parlay_matrix_tab(): _render_slip_feed(["SPORTSBOOK_PARLAY"], "PARLAY MATRIX (SIMULATED)", "#ff4757")
def render_prizepicks_tab(): _render_slip_feed(["PRIZEPICKS", "UNDERDOG"], "PRIZEPICKS & UNDERDOG SLIPS", "#00f2fe")
'''

with open("ui_addresses.py", "w", encoding="utf-8") as f:
    f.write(ui_code)
print("  ✓ ui_addresses.py written successfully.")

# --- 2. RUN GENERATOR ---
print("  ⚙️ Executing generate_dfs.py...")
os.system("python generate_dfs.py")

# --- 3. FULL SYSTEM AUDIT ---
print("\n" + "="*65)
print(" 🔬 COMPLETE PIPELINE AUDIT REPORT")
print("="*65)

with sqlite3.connect(DB_PATH) as conn:
    cur = conn.cursor()
    
    # Roster Counts
    cash_count = cur.execute("SELECT COUNT(*) FROM dfs_rosters WHERE lineup_type = 'CASH'").fetchone()[0]
    gpp_count = cur.execute("SELECT COUNT(*) FROM dfs_rosters WHERE lineup_type = 'GPP'").fetchone()[0]
    total_rosters = cur.execute("SELECT COUNT(*) FROM dfs_rosters").fetchone()[0]
    
    # Slips Counts
    parlay_count = cur.execute("SELECT COUNT(*) FROM slips WHERE platform = 'SPORTSBOOK_PARLAY'").fetchone()[0]
    pp_count = cur.execute("SELECT COUNT(*) FROM slips WHERE platform IN ('PRIZEPICKS', 'UNDERDOG')").fetchone()[0]
    total_slips = cur.execute("SELECT COUNT(*) FROM slips").fetchone()[0]
    
    # Player Pool
    total_players = cur.execute("SELECT COUNT(*) FROM player_rankings").fetchone()[0]
    dst_count = cur.execute("SELECT COUNT(*) FROM player_rankings WHERE pos = 'DST'").fetchone()[0]
    evaluated_count = cur.execute("SELECT COUNT(*) FROM player_rankings WHERE ppr_baseline > 0").fetchone()[0]
    
    # Exposure audit on GPP lineups
    gpp_rosters = cur.execute("SELECT qb, rb1, rb2, wr1, wr2, wr3, te, flex, dst FROM dfs_rosters WHERE lineup_type = 'GPP'").fetchall()
    exposure = {}
    for r in gpp_rosters:
        for p in r:
            exposure[p] = exposure.get(p, 0) + 1
            
    max_exp_player = max(exposure, key=exposure.get) if exposure else "None"
    max_exp_pct = exposure[max_exp_player] if exposure else 0
    over_limit = sum(1 for v in exposure.values() if v > 30)

    print(f"  [1] DFS ROSTERS AUDIT:")
    print(f"      - Cash Lineups:      {cash_count} / 100")
    print(f"      - GPP Lineups:       {gpp_count} / 100")
    print(f"      - Total Lineups:     {total_rosters} / 200")
    print(f"      - Lineup Slots:      9 slots (QB, 2 RB, 3 WR, TE, FLEX, DST)")

    print(f"\n  [2] EXPOSURE GOVERNOR AUDIT:")
    print(f"      - Highest Exposure:  {max_exp_player} ({max_exp_pct}%)")
    print(f"      - Exposure Breaches: {over_limit} (Target: 0 over 30%)")
    print(f"      - Status:            {'✅ PASS' if over_limit == 0 else '❌ FAIL'}")

    print(f"\n  [3] BETTING SLIPS AUDIT:")
    print(f"      - Parlay Slips:      {parlay_count} / 200")
    print(f"      - Prop Slips (PP/UD):{pp_count} / 200")
    print(f"      - Total Slips:       {total_slips} / 400")

    print(f"\n  [4] PLAYER EVALUATION POOL:")
    print(f"      - MFL Player Roster: {total_players} players")
    print(f"      - NFL Defenses (DST):{dst_count} / 32")
    print(f"      - Evaluated with PPR:{evaluated_count} active")

print("="*65 + "\n")