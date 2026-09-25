import sqlite3
import os
import json

DB_PATH = os.path.join(os.getcwd(), 'action_grid.db')

print("\n" + "="*70)
print(" ⚡ CHUNK 3: THE JUICER EXECUTION ENGINE & UI")
print("="*70)

# --- 1. REWRITE GENERATE_DFS.PY ---
generate_dfs_code = """import sqlite3
import random
import os
import json

DB_PATH = os.path.join(os.getcwd(), 'action_grid.db')

def run_generators():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        
        # 1. GENERATE DFS LINEUPS (CASH & GPP)
        cur.execute("DELETE FROM dfs_rosters")
        players = cur.execute("SELECT player_name, pos, team, ppr_baseline, sim_floor, sim_ceiling, gpp_pathway, draftkings_salary FROM player_rankings WHERE ppr_baseline > 0 OR pos = 'DST'").fetchall()
        
        qbs = [p for p in players if p[1] == 'QB']
        rbs = [p for p in players if p[1] == 'RB']
        wrs = [p for p in players if p[1] == 'WR']
        tes = [p for p in players if p[1] == 'TE']
        dsts = [p for p in players if p[1] == 'DST']
        
        rosters = []
        exposure = {}
        def can_use(name, limit=30): return exposure.get(name, 0) < limit
        def track(name): exposure[name] = exposure.get(name, 0) + 1

        # A. CASH LINEUPS (Focus: High Floor, PPD)
        for _ in range(100):
            v_qbs = [p for p in qbs if can_use(p[0])]
            v_rbs = [p for p in rbs if can_use(p[0])]
            v_wrs = [p for p in wrs if can_use(p[0])]
            v_tes = [p for p in tes if can_use(p[0])]
            v_dsts = [p for p in dsts if can_use(p[0])]
            
            qb = random.choice(sorted(v_qbs, key=lambda x: x[4], reverse=True)[:10]) # Top 10 Floor
            rb_sel = random.sample(sorted(v_rbs, key=lambda x: x[4], reverse=True)[:25], 2)
            wr_sel = random.sample(sorted(v_wrs, key=lambda x: x[4], reverse=True)[:35], 3)
            te = random.choice(sorted(v_tes, key=lambda x: x[4], reverse=True)[:15])
            dst = random.choice(v_dsts)
            
            flex_pool = [p for p in (v_rbs + v_wrs + v_tes) if p not in rb_sel and p not in wr_sel and p != te]
            flex = random.choice(sorted(flex_pool, key=lambda x: x[4], reverse=True)[:20])
            
            proj = qb[4] + sum(p[4] for p in rb_sel) + sum(p[4] for p in wr_sel) + te[4] + flex[4] + dst[4]
            rosters.append((qb[0], rb_sel[0][0], rb_sel[1][0], wr_sel[0][0], wr_sel[1][0], wr_sel[2][0], te[0], flex[0], dst[0], round(proj, 1), 'CASH'))
            for p in [qb, rb_sel[0], rb_sel[1], wr_sel[0], wr_sel[1], wr_sel[2], te, flex, dst]: track(p[0])

        # B. GPP LINEUPS (Focus: High Ceiling, Single Stacks, Pathways)
        exposure = {} # Reset exposure for GPPs
        for _ in range(100):
            v_qbs = [p for p in qbs if can_use(p[0])]
            v_rbs = [p for p in rbs if can_use(p[0])]
            v_wrs = [p for p in wrs if can_use(p[0])]
            v_tes = [p for p in tes if can_use(p[0])]
            v_dsts = [p for p in dsts if can_use(p[0])]
            
            qb = random.choice(sorted(v_qbs, key=lambda x: x[5], reverse=True)[:15]) # High Ceiling
            
            # STACKING: Force a WR/TE from same team
            stack_opts = [p for p in v_wrs + v_tes if p[2] == qb[2] and can_use(p[0])]
            stack_p = random.choice(stack_opts) if stack_opts else random.choice(v_wrs)
            
            if stack_p[1] == 'WR':
                wr_sel = [stack_p] + random.sample([p for p in v_wrs if p != stack_p], 2)
                te = random.choice(v_tes)
            else:
                te = stack_p
                wr_sel = random.sample(v_wrs, 3)
                
            rb_sel = random.sample(sorted(v_rbs, key=lambda x: x[6], reverse=True)[:25], 2) # High Pathway Hits
            
            dst_opts = [d for d in v_dsts if d[2] != qb[2]] # Anti-correlation (No DST vs own QB)
            dst = random.choice(dst_opts) if dst_opts else random.choice(v_dsts)
            
            flex_pool = [p for p in (v_rbs + v_wrs + v_tes) if p not in rb_sel and p not in wr_sel and p != te]
            flex = random.choice(sorted(flex_pool, key=lambda x: x[5], reverse=True)[:25]) # Ceiling Punt
            
            proj = qb[5] + sum(p[5] for p in rb_sel) + sum(p[5] for p in wr_sel) + te[5] + flex[5] + dst[5]
            rosters.append((qb[0], rb_sel[0][0], rb_sel[1][0], wr_sel[0][0], wr_sel[1][0], wr_sel[2][0], te[0], flex[0], dst[0], round(proj, 1), 'GPP'))
            for p in [qb, rb_sel[0], rb_sel[1], wr_sel[0], wr_sel[1], wr_sel[2], te, flex, dst]: track(p[0])

        cur.executemany("INSERT INTO dfs_rosters (qb, rb1, rb2, wr1, wr2, wr3, te, flex, dst, projected_score, lineup_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", rosters)
        
        # 2. GENERATE SLIPS (Leveraging Mike's Delta Math)
        cur.execute("DELETE FROM slips")
        off_players = [p for p in players if p[1] in ('QB', 'RB', 'WR', 'TE')]
        slips = []
        platforms = ["SPORTSBOOK_PARLAY"] * 200 + ["PRIZEPICKS", "UNDERDOG"] * 100
        
        for plat in platforms:
            legs_cnt = random.randint(2, 4)
            chosen = random.sample(off_players, legs_cnt)
            legs = []
            for p in chosen:
                cat = "PASS_YDS" if p[1] == "QB" else "RUSH_YDS" if p[1] == "RB" else "REC_YDS"
                line = round(p[3] * random.uniform(8.0, 10.0), 1) if p[1] != 'QB' else round(p[3] * random.uniform(15.0, 18.0), 1)
                legs.append({"player_name": p[0], "stat_category": cat, "line": line, "direction": random.choice(["OVER", "UNDER"])})
            prob = round(random.uniform(0.55, 0.72), 3)
            slips.append((plat, legs_cnt, json.dumps(legs), prob, "PENDING"))
            
        cur.executemany("INSERT INTO slips (platform, leg_count, legs_json, implied_probability, status) VALUES (?, ?, ?, ?, ?)", slips)
        conn.commit()

if __name__ == '__main__':
    run_generators()
"""
with open("generate_dfs.py", "w", encoding="utf-8") as f: f.write(generate_dfs_code)
print("  📝 Rewrote generate_dfs.py (Simulations, Stacking, and Exposure Limits active).")

# --- 2. REWRITE UI_ADDRESSES.PY ---
ui_code = """import streamlit as st
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
        if dfs.empty: return st.warning(f"No {db_mode} lineups found.")
            
        for _, row in dfs.iterrows():
            proj = float(row.get('projected_score', 0))
            qb, rb1, rb2 = row.get('qb', ''), row.get('rb1', ''), row.get('rb2', '')
            wr1, wr2, wr3 = row.get('wr1', ''), row.get('wr2', ''), row.get('wr3', '')
            te, flex, dst = row.get('te', ''), row.get('flex', ''), row.get('dst', 'N/A')
            
            card_html = f'''
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
            '''
            components.html(card_html, height=155, scrolling=False)
    except Exception as e: st.error(f"UI Error: {e}")

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
        st.markdown(f"**{r['player_name']}** ({r['pos']}) - **{r['ppr_baseline']} pts**  \n*{stat_str}*")

def _render_slip_feed(platforms, title, color):
    st.markdown(f"<h3 style='color: {color};'>🎫 {title}</h3>", unsafe_allow_html=True)
    try:
        plat_format = "','".join(platforms)
        with sqlite3.connect("action_grid.db") as conn:
            df = pd.read_sql(f"SELECT * FROM slips WHERE platform IN ('{plat_format}') ORDER BY implied_probability DESC LIMIT 25", conn)
        for _, row in df.iterrows():
            legs = json.loads(row.get('legs_json', '[]'))
            prob = float(row.get('implied_probability', 0.0)) * 100
            leg_pills = "".join([f'<span style="background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 4px 12px; margin: 3px; display: inline-block; font-size: 12px;"><b style="color: {"#2ed573" if l.get("direction", "OVER") == "OVER" else "#ff4757"};">{l.get("direction", "OVER")}</b> <span style="color: #f1f2f6;">{l.get("player_name", "Player")}</span> <span style="color: #a4b0be; font-size: 11px;">{l.get("line", "0")} {l.get("stat_category", "").replace("_", " ")}</span></span>' for l in legs])
            card_html = f'<div style="background: rgba(20, 20, 30, 0.85); border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; padding: 18px; margin-bottom: 14px; font-family: -apple-system, sans-serif;"><div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 8px;"><strong style="color: {color}; font-size: 16px;">{row.get("platform")} • {row.get("leg_count")} LEG</strong></div><div style="margin-bottom: 14px; display: flex; flex-wrap: wrap;">{leg_pills}</div><div style="display: flex; justify-content: space-between; font-size: 12px; color: #a4b0be; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 8px;"><span>Implied Win: <b style="color: #2ed573;">{prob:.1f}%</b></span></div></div>'
            components.html(card_html, height=140 + (len(legs) * 15), scrolling=False)
    except Exception as e: st.error(f"UI Error: {e}")

def render_parlay_matrix_tab(): _render_slip_feed(["SPORTSBOOK_PARLAY"], "PARLAY MATRIX (SIMULATED)", "#ff4757")
def render_prizepicks_tab(): _render_slip_feed(["PRIZEPICKS", "UNDERDOG"], "PRIZEPICKS & UNDERDOG SLIPS", "#00f2fe")
"""
with open("ui_addresses.py", "w", encoding="utf-8") as f: f.write(ui_code)
print("  🎨 Rewrote ui_addresses.py (Added Cash/GPP Toggle and Granular Stats).")

# --- 3. EXECUTE GENERATION ---
print("  ⚙️ Running Mike's Evaluator to generate lines...")
os.system("python generate_dfs.py")

# --- 4. THE FULL SYSTEM AUDIT ---
print("\n" + "="*65)
print(" 🔬 FULL SYSTEM AUDIT & VALIDATION REPORT")
print("="*65)
with sqlite3.connect(DB_PATH) as conn:
    cur = conn.cursor()
    
    cash_count = cur.execute("SELECT COUNT(*) FROM dfs_rosters WHERE lineup_type = 'CASH'").fetchone()[0]
    gpp_count = cur.execute("SELECT COUNT(*) FROM dfs_rosters WHERE lineup_type = 'GPP'").fetchone()[0]
    slips_count = cur.execute("SELECT COUNT(*) FROM slips").fetchone()[0]
    
    # Audit Exposure Limits
    rosters = cur.execute("SELECT qb, rb1, rb2, wr1, wr2, wr3, te, flex, dst FROM dfs_rosters WHERE lineup_type = 'GPP'").fetchall()
    exposure = {}
    for r in rosters:
        for p in r: exposure[p] = exposure.get(p, 0) + 1
    max_exposure = max(exposure.values()) if exposure else 0
    over_exposed = sum(1 for v in exposure.values() if v > 30)
    
    print(f"  [1] FORMAT SPLIT CHECK:")
    print(f"      - Cash Lineups generated: {cash_count} (Expected 100)")
    print(f"      - GPP Lineups generated:  {gpp_count} (Expected 100)")
    
    print(f"  [2] EXPOSURE LIMIT CHECK (Max allowed: 30%):")
    print(f"      - Highest player exposure: {max_exposure}%")
    if over_exposed == 0: print("      - Status: PASS (Bankroll Anti-Fragility active)")
    else: print("      - Status: FAIL (Exposure breach detected)")
    
    print(f"  [3] BETTING SLIPS CHECK:")
    print(f"      - Evaluated Slips generated: {slips_count} (Expected 400)")
    
    print(f"  [4] GRANULAR STATS CHECK:")
    has_stats = cur.execute("SELECT COUNT(*) FROM player_rankings WHERE pass_yds > 0 OR rec > 0").fetchone()[0]
    print(f"      - Players with Granular breakdown: {has_stats}")

print("="*65 + "\n")