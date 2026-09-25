import os

path = "ui_components.py"
# The 'ignore' flag acts as a bulldozer, skipping any corrupted terminal bytes left over
with open(path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# Completely sever the broken functions
if "def render_real_parlay_matrix" in content:
    content = content.split("def render_real_parlay_matrix")[0]
if "def render_dfs_lineups" in content:
    content = content.split("def render_dfs_lineups")[0]

# The MVP Micro-Grid Showdown & Unpacked Parlay Code
new_code = """
def render_real_parlay_matrix(conn):
    import streamlit as st
    import pandas as pd
    import json
    st.markdown("<h3 style='color:#ff2a6d;'>🎯 THE PARLAY MATRIX</h3>", unsafe_allow_html=True)
    try:
        df = pd.read_sql("SELECT ticket_id, odds, border_color, ticket_json, confidence_score FROM theoretical_bets WHERE ticket_id NOT LIKE 'SBOX%'", conn)
        if df.empty: return st.warning("⚠️ No live tickets.")
        for _, row in df.iterrows():
            legs_html = ""
            try:
                for leg in json.loads(row['ticket_json']):
                    legs_html += f"<li style='margin-bottom:2px;'><b>{leg.get('player','')}</b> ({leg.get('team','')}) - {leg.get('stat','')}</li>"
            except:
                legs_html = "<li><i>Data on book</i></li>"
            
            card = f"<div style='background:rgba(255,255,255,0.05); padding:12px; border-radius:8px; border-left:4px solid {row.get('border_color','#00e5ff')}; margin-bottom:10px;'><b style='color:#00ff88;'>{row['ticket_id']} ({row['odds']})</b><ul style='margin:5px 0 0; padding-left:20px; font-size:12px;'>{legs_html}</ul></div>"
            st.markdown(card, unsafe_allow_html=True)
    except Exception as e: st.error(e)

def render_dfs_lineups(conn):
    import streamlit as st
    import pandas as pd
    st.markdown("<h3 style='color:#ffd700;'>👑 DFS SHOWDOWN ROSTERS</h3>", unsafe_allow_html=True)
    try:
        df = pd.read_sql("SELECT * FROM dfs_showdown_lineups ORDER BY projected_pts DESC LIMIT 5", conn)
        if df.empty: return st.warning("⚠️ No Showdown lineups.")
        for _, row in df.iterrows():
            grid = f"<div style='display:grid; grid-template-columns:repeat(6,1fr); gap:5px; font-size:11px; text-align:center; margin-top:8px;'><div style='background:rgba(255,0,0,0.1); padding:4px;'><b>CPT</b><br>{row['captain']}</div><div style='background:rgba(255,255,255,0.05); padding:4px;'><b>FLEX</b><br>{row['flex_1']}</div><div style='background:rgba(255,255,255,0.05); padding:4px;'><b>FLEX</b><br>{row['flex_2']}</div><div style='background:rgba(255,255,255,0.05); padding:4px;'><b>FLEX</b><br>{row['flex_3']}</div><div style='background:rgba(255,255,255,0.05); padding:4px;'><b>FLEX</b><br>{row['flex_4']}</div><div style='background:rgba(255,255,255,0.05); padding:4px;'><b>FLEX</b><br>{row['flex_5']}</div></div>"
            st.markdown(f"<div style='background:rgba(255,215,0,0.05); padding:12px; border-radius:8px; border:1px solid rgba(255,215,0,0.2); margin-bottom:10px;'><b>Lineup #{row['lineup_num']}</b> | <span style='color:#00ff88;'>{row['projected_pts']} pts</span>{grid}</div>", unsafe_allow_html=True)
    except Exception as e: st.error(e)
"""

with open(path, "w", encoding="utf-8") as f:
    f.write(content.strip() + "\n\n" + new_code)
print("✅ MAMBA OUT. Code injected perfectly. Line 263 is dead.")