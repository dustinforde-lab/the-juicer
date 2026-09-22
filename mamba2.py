import os, re

path = "ui_components.py"
with open(path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# Strip out the old rendering functions
content = re.sub(r"def render_real_parlay_matrix\(conn\):.*?(?=def |\Z)", "", content, flags=re.DOTALL)
content = re.sub(r"def render_dfs_lineups\(conn\):.*?(?=def |\Z)", "", content, flags=re.DOTALL)

new_code = """
def render_real_parlay_matrix(conn):
    import streamlit as st
    import pandas as pd
    import json
    st.markdown("<h3 style='color:#ff2a6d;'>🎯 THE PARLAY MATRIX (LIVE TICKETS)</h3>", unsafe_allow_html=True)
    try:
        df = pd.read_sql("SELECT ticket_id, odds, border_color, ticket_json FROM theoretical_bets WHERE ticket_id NOT LIKE 'SBOX%'", conn)
        if df.empty: return st.warning("⚠️ No live tickets.")
        for _, row in df.iterrows():
            legs_html = ""
            try:
                for leg in json.loads(row['ticket_json']):
                    if isinstance(leg, dict):
                        # Dynamically extract player info
                        player = leg.get('player', leg.get('name', leg.get('playerName', 'Unknown Player')))
                        team = leg.get('team', leg.get('team_abbr', ''))
                        stat = leg.get('stat', leg.get('market', leg.get('prop', leg.get('description', ''))))
                        line = leg.get('line', leg.get('value', leg.get('point', '')))
                        
                        text = f"<b>{player}</b>"
                        if team: text += f" ({team})"
                        if stat: text += f" - {stat}"
                        if line: text += f" <b>{line}</b>"
                        
                        # CATCH-ALL: If the book uses custom keys (e.g., 'receptions': 5.5), extract them automatically
                        if not stat and not line:
                            extras = [f"{str(k).replace('_', ' ').title()}: {v}" for k, v in leg.items() if k.lower() not in ['player', 'name', 'team', 'playername']]
                            if extras: text += " - " + " | ".join(extras)
                            
                        legs_html += f"<li style='margin-bottom:6px;'>{text}</li>"
                    else:
                        legs_html += f"<li>{str(leg)}</li>"
            except:
                legs_html = "<li><i>Data on book</i></li>"
            
            card = f"<div style='background:rgba(255,255,255,0.05); padding:16px; border-radius:8px; border-left:4px solid {row.get('border_color','#00e5ff')}; margin-bottom:12px;'><div style='display:flex; justify-content:space-between; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:8px; margin-bottom:10px;'><span style='font-size:16px; font-weight:bold;'>Ticket: {row['ticket_id']}</span><span style='font-size:16px;'>Odds: <b style='color:#00ff88;'>{row['odds']}</b></span></div><ul style='margin:0; padding-left:20px; font-size:14px; color:#e2e8f0;'>{legs_html}</ul></div>"
            st.markdown(card, unsafe_allow_html=True)
    except Exception as e: st.error(e)

def render_dfs_lineups(conn):
    import streamlit as st
    import pandas as pd
    import json
    st.markdown("<h3 style='color:#ffd700;'>👑 CLASSIC SUNDAY SLATE (9-MAN ROSTERS)</h3>", unsafe_allow_html=True)
    try:
        df = pd.read_sql("SELECT * FROM dfs_classic_lineups ORDER BY projected_pts DESC LIMIT 10", conn)
        if df.empty: return st.warning("⚠️ No Classic lineups found.")
        for _, row in df.iterrows():
            try: roster = json.loads(row['roster_json'])
            except: roster = []
            
            # Strict 9-Column Slotting Logic
            slots = {'QB': None, 'RB1': None, 'RB2': None, 'WR1': None, 'WR2': None, 'WR3': None, 'TE': None, 'FLEX': None, 'DST': None}
            
            for player in roster:
                pos = player.get('pos', '').upper()
                name = player.get('name', 'Unknown')
                
                if pos == 'QB' and not slots['QB']: slots['QB'] = name
                elif pos == 'RB':
                    if not slots['RB1']: slots['RB1'] = name
                    elif not slots['RB2']: slots['RB2'] = name
                    elif not slots['FLEX']: slots['FLEX'] = f"{name} (RB)"
                elif pos == 'WR':
                    if not slots['WR1']: slots['WR1'] = name
                    elif not slots['WR2']: slots['WR2'] = name
                    elif not slots['WR3']: slots['WR3'] = name
                    elif not slots['FLEX']: slots['FLEX'] = f"{name} (WR)"
                elif pos == 'TE':
                    if not slots['TE']: slots['TE'] = name
                    elif not slots['FLEX']: slots['FLEX'] = f"{name} (TE)"
                elif pos in ['DST', 'DEF']: slots['DST'] = name
            
            grid = f\"\"\"<div style='display:grid; grid-template-columns:repeat(9,1fr); gap:6px; font-size:11px; text-align:center; margin-top:8px;'>
                <div style='background:rgba(255,255,255,0.05); padding:6px; border-radius:4px;'><b style='color:#8b949e;'>QB</b><br>{slots['QB'] or '-'}</div>
                <div style='background:rgba(255,255,255,0.05); padding:6px; border-radius:4px;'><b style='color:#8b949e;'>RB</b><br>{slots['RB1'] or '-'}</div>
                <div style='background:rgba(255,255,255,0.05); padding:6px; border-radius:4px;'><b style='color:#8b949e;'>RB</b><br>{slots['RB2'] or '-'}</div>
                <div style='background:rgba(255,255,255,0.05); padding:6px; border-radius:4px;'><b style='color:#8b949e;'>WR</b><br>{slots['WR1'] or '-'}</div>
                <div style='background:rgba(255,255,255,0.05); padding:6px; border-radius:4px;'><b style='color:#8b949e;'>WR</b><br>{slots['WR2'] or '-'}</div>
                <div style='background:rgba(255,255,255,0.05); padding:6px; border-radius:4px;'><b style='color:#8b949e;'>WR</b><br>{slots['WR3'] or '-'}</div>
                <div style='background:rgba(255,255,255,0.05); padding:6px; border-radius:4px;'><b style='color:#8b949e;'>TE</b><br>{slots['TE'] or '-'}</div>
                <div style='background:rgba(255,255,255,0.05); padding:6px; border-radius:4px;'><b style='color:#8b949e;'>FLEX</b><br>{slots['FLEX'] or '-'}</div>
                <div style='background:rgba(255,255,255,0.05); padding:6px; border-radius:4px;'><b style='color:#8b949e;'>DST</b><br>{slots['DST'] or '-'}</div>
            </div>\"\"\"
            
            arch = row.get('archetype', f"Lineup #{row.get('id', '')}")
            st.markdown(f"<div style='background:rgba(255,215,0,0.05); padding:15px; border-radius:8px; border:1px solid rgba(255,215,0,0.2); margin-bottom:12px;'><b style='font-size:14px;'>{arch.upper()}</b> | <span style='color:#00ff88; float:right;'>{row.get('projected_pts', 0)} pts</span>{grid}</div>", unsafe_allow_html=True)
    except Exception as e: st.error(e)
"""

with open(path, "w", encoding="utf-8") as f:
    f.write(content.strip() + "\n\n" + new_code)
print("✅ SUNDAY SLATE & PARLAY PARSERS ENGAGED.")