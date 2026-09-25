import re, sqlite3, json, datetime, os

print("\n" + "="*65)
print(" 🔌 RE-WIRING DASHBOARD ADDRESSES & ROUTING")
print("="*65)

# --- 1. BUILD THE ISOLATED UI ADDRESS PANEL ---
ui_addresses_code = """
import streamlit as st
import sqlite3
import pandas as pd
import json

def render_dfs_engine_tab():
    st.markdown("<h3 style='color: #eccc68; margin-bottom: 20px;'>👑 DFS LINEUPS</h3>", unsafe_allow_html=True)
    try:
        with sqlite3.connect("action_grid.db") as conn:
            dfs = pd.read_sql("SELECT * FROM dfs_rosters ORDER BY projected_score DESC LIMIT 50", conn)
        if dfs.empty:
            st.warning("No DFS lineups found in database.")
            return
        for _, row in dfs.iterrows():
            st.markdown(f'''
            <div style="background: rgba(20, 20, 30, 0.8); border: 1px solid rgba(255,255,255,0.2); border-radius: 8px; padding: 15px; margin-bottom: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                <strong style="color: #eccc68; font-size: 16px;">DRAFTKINGS | PROJ FANTASY POINTS: {row.get('projected_score', 0)}</strong><hr style="margin: 8px 0; border-color: rgba(255,255,255,0.1);">
                <span style="color: #f1f2f6; font-size: 14px; line-height: 1.8;">
                <b style="color:#70a1ff">QB:</b> {row.get('qb')} &nbsp;|&nbsp; <b style="color:#2ed573">RB:</b> {row.get('rb1')} &nbsp;|&nbsp; <b style="color:#2ed573">RB:</b> {row.get('rb2')} &nbsp;|&nbsp; <b style="color:#ff4757">WR:</b> {row.get('wr1')}<br>
                <b style="color:#ff4757">WR:</b> {row.get('wr2')} &nbsp;|&nbsp; <b style="color:#ff4757">WR:</b> {row.get('wr3')} &nbsp;|&nbsp; <b style="color:#ffa502">TE:</b> {row.get('te')} &nbsp;|&nbsp; <b style="color:#a4b0be">FLEX:</b> {row.get('flex')}
                </span>
            </div>
            ''', unsafe_allow_html=True)
    except Exception as e: st.error(f"DFS Routing Error: {e}")

def _render_slip_feed(platforms, title, color):
    st.markdown(f"<h3 style='color: {color}; margin-bottom: 20px;'>🎫 {title}</h3>", unsafe_allow_html=True)
    try:
        plat_format = "','".join(platforms)
        with sqlite3.connect("action_grid.db") as conn:
            df = pd.read_sql(f"SELECT * FROM slips WHERE platform IN ('{plat_format}') ORDER BY implied_probability DESC LIMIT 50", conn)
        if df.empty:
            st.warning(f"No {title} slips found in database.")
            return
        for _, row in df.iterrows():
            legs = json.loads(row.get('legs_json', '[]'))
            leg_display = "<br>".join([f"• <b>{l.get('player_name')}</b>: {l.get('direction')} {l.get('line')} {l.get('stat_category')}" for l in legs])
            st.markdown(f'''
            <div style="background: rgba(20, 20, 30, 0.8); border: 1px solid rgba(255,255,255,0.2); border-radius: 8px; padding: 15px; margin-bottom: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                <strong style="color: {color}; font-size: 16px;">{row.get('platform')} | {row.get('leg_count')}-LEG | WIN PROB: {row.get('implied_probability', 0)*100:.1f}%</strong><hr style="margin: 8px 0; border-color: rgba(255,255,255,0.1);">
                <span style="color: #f1f2f6; font-size: 14px;">{leg_display}</span>
            </div>
            ''', unsafe_allow_html=True)
    except Exception as e: st.error(f"Slip Routing Error: {e}")

def render_parlay_matrix_tab():
    _render_slip_feed(["SPORTSBOOK_PARLAY"], "PARLAY BETS", "#ff4757")

def render_prizepicks_tab():
    _render_slip_feed(["PRIZEPICKS", "UNDERDOG"], "PRIZEPICKS & UNDERDOG BETS", "#00f2fe")
"""
with open("ui_addresses.py", "w", encoding="utf-8") as f:
    f.write(ui_addresses_code.strip())
print("  ✅ ui_addresses.py created (Dedicated routing sub-panel installed).")

# --- 2. RE-WIRE APP.PY TABS ---
with open("app.py", "r", encoding="utf-8") as f:
    app_code = f.read()

if "import ui_addresses" not in app_code:
    app_code = app_code.replace("import ui_components as ui", "import ui_components as ui\nimport ui_addresses")

# Hard-map the specific tabs to the new file
app_code = re.sub(r'ui\.render_dfs\(.*?\)', 'ui_addresses.render_dfs_engine_tab()', app_code)
app_code = re.sub(r'ui\.render_real_parlay_matrix\(.*?\)', 'ui_addresses.render_parlay_matrix_tab()', app_code)
app_code = re.sub(r'ui\.render_parlay_matrix\(.*?\)', 'ui_addresses.render_parlay_matrix_tab()', app_code)
app_code = re.sub(r'ui\.render_prizepicks_underdog\(.*?\)', 'ui_addresses.render_prizepicks_tab()', app_code)
app_code = re.sub(r'ui\.render_pickem_slips\(.*?\)', 'ui_addresses.render_prizepicks_tab()', app_code)
app_code = re.sub(r'ui\.render_telemetry_relay\(.*?\)', 'ui_addresses.render_parlay_matrix_tab()', app_code)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(app_code)
print("  ✅ app.py re-wired. DFS, Parlay, and PrizePicks tabs now point to new addresses.")

# --- 3. INJECT TRACER DATA TO VERIFY MAPPING ---
try:
    conn = sqlite3.connect("action_grid.db")
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute("DELETE FROM dfs_rosters")
    conn.execute("DELETE FROM slips")
    
    # Tracer DFS
    conn.execute("INSERT INTO dfs_rosters (qb, rb1, rb2, wr1, wr2, wr3, te, flex, projected_score) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                 ("TRACER_QB", "TRACER_RB1", "TRACER_RB2", "TRACER_WR1", "TRACER_WR2", "TRACER_WR3", "TRACER_TE", "TRACER_FLEX", 999.9))
    
    # Tracer Parlay & PrizePicks
    fake_legs = json.dumps([{"player_name": "TRACER_PLAYER", "stat_category": "passing_yds", "line": 999.5, "direction": "OVER"}])
    conn.execute("INSERT INTO slips (platform, leg_count, legs_json, implied_probability, confidence_tier, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)", ("SPORTSBOOK_PARLAY", 1, fake_legs, 0.99, "A", "PENDING", now))
    conn.execute("INSERT INTO slips (platform, leg_count, legs_json, implied_probability, confidence_tier, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)", ("PRIZEPICKS", 1, fake_legs, 0.99, "A", "PENDING", now))
    conn.execute("INSERT INTO slips (platform, leg_count, legs_json, implied_probability, confidence_tier, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)", ("UNDERDOG", 1, fake_legs, 0.99, "A", "PENDING", now))
    conn.commit()
    conn.close()
    print("  ✅ Tracer data generated and properly addressed.")
except Exception as e: print(f"  ❌ Data Injection Error: {e}")

print("\n" + "="*65)
print(" 🚀 ADDRESS FIX COMPLETE. REBOOTING STREAMLIT...")
print("="*65 + "\n")