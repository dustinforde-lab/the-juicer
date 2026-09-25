import os

print("\n" + "="*65)
print(" 🚀 DEPLOYING FINAL PRODUCTION-READY UI FIX")
print("="*65)

native_ui = """
import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import pandas as pd
import json

def render_dfs_engine_tab():
    st.markdown("<h3 style='color: #eccc68; margin-bottom: 15px; letter-spacing: 1px;'>👑 DFS CLASSIC 9-MAN LINEUPS</h3>", unsafe_allow_html=True)
    try:
        with sqlite3.connect("action_grid.db") as conn:
            dfs = pd.read_sql("SELECT * FROM dfs_rosters ORDER BY projected_score DESC LIMIT 25", conn)
        
        if dfs.empty:
            st.warning("No DFS lineups found in database.")
            return
            
        for _, row in dfs.iterrows():
            proj = row.get('projected_score', 0)
            proj_val = float(proj) if proj is not None else 0.0
            
            card_html = f'''
            <div style="background: rgba(20, 20, 30, 0.85); border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; padding: 18px; margin-bottom: 14px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; box-shadow: 0 4px 12px rgba(0,0,0,0.4);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 8px;">
                    <div>
                        <span style="background: rgba(46, 213, 115, 0.15); color: #2ed573; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 11px; margin-right: 8px;">CASH • DK</span>
                        <strong style="color: #f1f2f6; font-size: 15px; letter-spacing: 0.5px;">OPTIMAL ROSTER CONFIGURATION</strong>
                    </div>
                    <div style="text-align: right;">
                        <span style="color: #2ed573; font-size: 18px; font-weight: bold;">{proj_val:.1f}</span>
                        <span style="color: #a4b0be; font-size: 11px; margin-left: 5px;">PROJ PTS</span>
                    </div>
                </div>
                
                <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                    <div style="background: rgba(112, 161, 255, 0.1); border: 1px solid rgba(112, 161, 255, 0.2); border-radius: 6px; padding: 6px 10px; flex: 1; min-width: 120px;">
                        <span style="color: #70a1ff; font-size: 10px; font-weight: bold; display: block;">QB</span>
                        <strong style="color: #f1f2f6; font-size: 13px;">{row.get('qb', 'N/A')}</strong>
                    </div>
                    <div style="background: rgba(46, 213, 115, 0.1); border: 1px solid rgba(46, 213, 115, 0.2); border-radius: 6px; padding: 6px 10px; flex: 1; min-width: 120px;">
                        <span style="color: #2ed573; font-size: 10px; font-weight: bold; display: block;">RB</span>
                        <strong style="color: #f1f2f6; font-size: 13px;">{row.get('rb1', 'N/A')}</strong>
                    </div>
                    <div style="background: rgba(46, 213, 115, 0.1); border: 1px solid rgba(46, 213, 115, 0.2); border-radius: 6px; padding: 6px 10px; flex: 1; min-width: 120px;">
                        <span style="color: #2ed573; font-size: 10px; font-weight: bold; display: block;">RB</span>
                        <strong style="color: #f1f2f6; font-size: 13px;">{row.get('rb2', 'N/A')}</strong>
                    </div>
                    <div style="background: rgba(255, 71, 87, 0.1); border: 1px solid rgba(255, 71, 87, 0.2); border-radius: 6px; padding: 6px 10px; flex: 1; min-width: 120px;">
                        <span style="color: #ff4757; font-size: 10px; font-weight: bold; display: block;">WR</span>
                        <strong style="color: #f1f2f6; font-size: 13px;">{row.get('wr1', 'N/A')}</strong>
                    </div>
                    <div style="background: rgba(255, 71, 87, 0.1); border: 1px solid rgba(255, 71, 87, 0.2); border-radius: 6px; padding: 6px 10px; flex: 1; min-width: 120px;">
                        <span style="color: #ff4757; font-size: 10px; font-weight: bold; display: block;">WR</span>
                        <strong style="color: #f1f2f6; font-size: 13px;">{row.get('wr2', 'N/A')}</strong>
                    </div>
                    <div style="background: rgba(255, 71, 87, 0.1); border: 1px solid rgba(255, 71, 87, 0.2); border-radius: 6px; padding: 6px 10px; flex: 1; min-width: 120px;">
                        <span style="color: #ff4757; font-size: 10px; font-weight: bold; display: block;">WR</span>
                        <strong style="color: #f1f2f6; font-size: 13px;">{row.get('wr3', 'N/A')}</strong>
                    </div>
                    <div style="background: rgba(255, 165, 2, 0.1); border: 1px solid rgba(255, 165, 2, 0.2); border-radius: 6px; padding: 6px 10px; flex: 1; min-width: 120px;">
                        <span style="color: #ffa502; font-size: 10px; font-weight: bold; display: block;">TE</span>
                        <strong style="color: #f1f2f6; font-size: 13px;">{row.get('te', 'N/A')}</strong>
                    </div>
                    <div style="background: rgba(164, 176, 190, 0.1); border: 1px solid rgba(164, 176, 190, 0.2); border-radius: 6px; padding: 6px 10px; flex: 1; min-width: 120px;">
                        <span style="color: #a4b0be; font-size: 10px; font-weight: bold; display: block;">FLEX</span>
                        <strong style="color: #f1f2f6; font-size: 13px;">{row.get('flex', 'N/A')}</strong>
                    </div>
                </div>
            </div>
            '''
            components.html(card_html, height=155, scrolling=False)
    except Exception as e:
        st.error(f"DFS UI Error: {e}")

def _render_slip_feed(platforms, title, color):
    st.markdown(f"<h3 style='color: {color}; margin-bottom: 15px; letter-spacing: 1px;'>🎫 {title}</h3>", unsafe_allow_html=True)
    try:
        plat_format = "','".join(platforms)
        with sqlite3.connect("action_grid.db") as conn:
            df = pd.read_sql(f"SELECT * FROM slips WHERE platform IN ('{plat_format}') ORDER BY implied_probability DESC LIMIT 25", conn)
            
        if df.empty:
            st.warning(f"No {title} slips found in database.")
            return
            
        for _, row in df.iterrows():
            raw_legs = row.get('legs_json', '[]')
            try:
                legs = json.loads(raw_legs) if isinstance(raw_legs, str) else raw_legs
                if not isinstance(legs, list):
                    legs = []
            except:
                legs = []
                
            tier = row.get('confidence_tier', 'A')
            prob_raw = row.get('implied_probability', 0.0)
            prob = float(prob_raw) * 100 if prob_raw is not None else 0.0
            
            leg_pills = ""
            if legs:
                for l in legs:
                    p_name = l.get('player_name', l.get('player', 'Player'))
                    direction = str(l.get('direction', l.get('pick', 'OVER'))).upper()
                    line = l.get('line', l.get('value', '35.5'))
                    cat = str(l.get('stat_category', l.get('stat', 'PROP'))).replace('_', ' ')
                    if cat == 'VAL':
                        cat = 'PROP'
                    
                    dir_color = "#2ed573" if direction == 'OVER' else "#ff4757"
                    leg_pills += f'<span style="background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 4px 12px; margin: 3px; display: inline-block; font-size: 12px;"><b style="color: {dir_color};">{direction}</b> <span style="color: #f1f2f6;">{p_name}</span> <span style="color: #a4b0be; font-size: 11px;">{line} {cat}</span></span>'
            else:
                leg_pills = '<span style="color: #a4b0be; font-size: 12px; padding: 5px; display: inline-block;">No leg details recorded.</span>'
            
            card_html = f'''
            <div style="background: rgba(20, 20, 30, 0.85); border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; padding: 18px; margin-bottom: 14px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; box-shadow: 0 4px 12px rgba(0,0,0,0.4);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 8px;">
                    <div>
                        <strong style="color: {color}; font-size: 16px; letter-spacing: 0.5px;">{row.get('platform')} • {row.get('leg_count')} LEG BUILD</strong>
                    </div>
                    <div>
                        <span style="background: #ff4757; color: white; padding: 3px 10px; border-radius: 12px; font-weight: bold; font-size: 11px; letter-spacing: 1px;">TIER {tier}</span>
                    </div>
                </div>
                
                <div style="margin-bottom: 14px; display: flex; flex-wrap: wrap;">
                    {leg_pills}
                </div>
                
                <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 8px; font-size: 12px; color: #a4b0be;">
                    <span>Implied Win Probability: <b style="color: #2ed573;">{prob:.1f}%</b></span>
                    <span>Status: <b style="color: #70a1ff;">{row.get('status', 'PENDING')}</b></span>
                </div>
            </div>
            '''
            box_height = 140 + (len(legs) * 15)
            components.html(card_html, height=box_height, scrolling=False)
    except Exception as e:
        st.error(f"Slip UI Error: {e}")

def render_parlay_matrix_tab():
    _render_slip_feed(["SPORTSBOOK_PARLAY"], "PARLAY MATRIX (SINGLE-BOOK SOURCED)", "#ff4757")

def render_prizepicks_tab():
    _render_slip_feed(["PRIZEPICKS", "UNDERDOG"], "PRIZEPICKS & UNDERDOG SLIPS", "#00f2fe")
"""

with open("ui_addresses.py", "w", encoding="utf-8") as f:
    f.write(native_ui.strip())
print("  ✅ ui_addresses.py deployed cleanly.")
