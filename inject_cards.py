import re

with open("ui_components.py", "r", encoding="utf-8") as f:
    code = f.read()

# The new HTML template matching your Rankings tab
new_pickem_ui = """
# --- PICK'EM SLIPS VIEWER (ROADMAP #83-92) ---
def render_pickem_slips():
    import streamlit as st
    import sqlite3
    import pandas as pd
    import json
    
    st.markdown("<h3 class='neon-title'>🎫 DFS, PRIZEPICKS & UNDERDOG SLIPS</h3>", unsafe_allow_html=True)
    
    try:
        with sqlite3.connect("action_grid.db") as conn:
            slips_df = pd.read_sql("SELECT * FROM slips ORDER BY implied_probability DESC", conn)
            
        if slips_df.empty:
            st.info("No active slips generated. Waiting for the AI generator loop.")
            return
            
        for _, row in slips_df.iterrows():
            legs = json.loads(row.get('legs_json', '[]'))
            platform = row.get('platform', 'DFS')
            
            # Platform colors
            p_color = "#00f2fe" if platform.upper() == "PRIZEPICKS" else ("#fbc531" if platform.upper() == "UNDERDOG" else "#4cd137")
            
            # Start Flexbox Card
            st.markdown(f'''
            <div style="display: flex; justify-content: space-between; background: rgba(20, 20, 30, 0.6); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 15px; margin-bottom: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                
                <!-- Left Side: Roster / Legs -->
                <div style="flex: 2; padding-right: 20px;">
                    <div style="margin-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 5px;">
                        <strong style="color: {p_color}; font-size: 16px; letter-spacing: 1px;">{platform.upper()} | {row.get('leg_count', len(legs))}-LEG CONFIGURATION</strong>
                    </div>
            ''', unsafe_allow_html=True)
            
            # Player Legs with Neon Badges
            for leg in legs:
                pos = leg.get('position', 'FLEX')
                # Map badge colors
                badge_bg = "rgba(255, 71, 87, 0.15)" if pos == "WR" else ("rgba(46, 213, 115, 0.15)" if pos == "RB" else "rgba(112, 161, 255, 0.15)")
                badge_text = "#ff4757" if pos == "WR" else ("#2ed573" if pos == "RB" else "#70a1ff")
                
                st.markdown(f'''
                    <div style="display: flex; align-items: center; margin-bottom: 8px; font-size: 14px;">
                        <span style="background: {badge_bg}; color: {badge_text}; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; margin-right: 12px; width: 40px; text-align: center;">{pos}</span>
                        <strong style="color: #f1f2f6; width: 180px;">{leg.get('player_name', 'Unknown')}</strong>
                        <span style="color: #a4b0be;">{leg.get('direction', '')} {leg.get('line', '')} <span style="opacity:0.5; font-size: 12px;">({leg.get('stat_category', '').replace('_', ' ')})</span></span>
                    </div>
                ''', unsafe_allow_html=True)
                
            # Right Side: Diagnosis Panel
            st.markdown(f'''
                </div>
                <div style="flex: 1; border-left: 1px solid rgba(255,255,255,0.1); padding-left: 20px; display: flex; flex-direction: column; justify-content: center;">
                    <div style="margin-bottom: 15px;">
                        <span style="color: #a4b0be; font-size: 11px; font-weight: bold; letter-spacing: 1px; text-transform: uppercase;">The Juicer Diagnosis</span><br/>
                        <span style="color: #f1f2f6; font-size: 13px;">High-correlation build exploiting structural edges in targeted matchups.</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 10px;">
                        <span style="color: #a4b0be; font-size: 12px;">WIN PROB</span>
                        <strong style="color: #2ed573;">{row.get('implied_probability', 0)*100:.1f}%</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 5px;">
                        <span style="color: #a4b0be; font-size: 12px;">EV METRIC</span>
                        <strong style="color: #eccc68;">+{row.get('ev_edge', 4.2)}%</strong>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Error loading slips: {e}")
"""

# Replace the old function with the new flexbox version
pattern = r"# --- PICK'EM SLIPS VIEWER.*?def render_pickem_slips\(\):.*?except Exception as e:.*?st\.error\(f\"Error loading slips: \{e\}\"\)"
if re.search(pattern, code, re.DOTALL):
    code = re.sub(pattern, new_pickem_ui.strip(), code, flags=re.DOTALL)
    with open("ui_components.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("✅ Flexbox slip cards successfully injected.")
else:
    print("⚠️ Could not find the target block. File might be modified.")