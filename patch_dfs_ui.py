import re

with open("ui_components.py", "r", encoding="utf-8") as f:
    code = f.read()

new_dfs_ui = """
# --- DFS ENGINE (ROADMAP #40-50) ---
def render_dfs_engine():
    import streamlit as st
    import sqlite3
    import pandas as pd
    
    st.markdown("<h3 class='neon-title'>👑 DFS CLASSIC ROSTERS</h3>", unsafe_allow_html=True)
    
    try:
        with sqlite3.connect("action_grid.db") as conn:
            # Check if table exists before querying
            tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table' AND name='dfs_rosters'", conn)
            if tables.empty:
                st.info("DFS table missing. Run the generator script.")
                return
                
            dfs_df = pd.read_sql("SELECT * FROM dfs_rosters ORDER BY projected_score DESC", conn)
            
        if dfs_df.empty:
            st.info("No DFS rosters generated. Waiting for the AI generator loop.")
            return
            
        for _, row in dfs_df.iterrows():
            st.markdown(f'''
            <div style="display: flex; justify-content: space-between; background: rgba(20, 20, 30, 0.6); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 15px; margin-bottom: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                
                <!-- Left Side: Roster -->
                <div style="flex: 2; padding-right: 20px;">
                    <div style="margin-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 5px;">
                        <strong style="color: #eccc68; font-size: 16px; letter-spacing: 1px;">DRAFTKINGS | CLASSIC 9-MAN</strong>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 14px;">
                        <div><span style="background: rgba(112, 161, 255, 0.15); color: #70a1ff; padding: 2px 6px; border-radius: 3px; font-weight: bold; font-size: 11px; margin-right: 8px;">QB</span> {row['qb']}</div>
                        <div><span style="background: rgba(46, 213, 115, 0.15); color: #2ed573; padding: 2px 6px; border-radius: 3px; font-weight: bold; font-size: 11px; margin-right: 8px;">RB</span> {row['rb1']}</div>
                        <div><span style="background: rgba(46, 213, 115, 0.15); color: #2ed573; padding: 2px 6px; border-radius: 3px; font-weight: bold; font-size: 11px; margin-right: 8px;">RB</span> {row['rb2']}</div>
                        <div><span style="background: rgba(255, 71, 87, 0.15); color: #ff4757; padding: 2px 6px; border-radius: 3px; font-weight: bold; font-size: 11px; margin-right: 8px;">WR</span> {row['wr1']}</div>
                        <div><span style="background: rgba(255, 71, 87, 0.15); color: #ff4757; padding: 2px 6px; border-radius: 3px; font-weight: bold; font-size: 11px; margin-right: 8px;">WR</span> {row['wr2']}</div>
                        <div><span style="background: rgba(255, 71, 87, 0.15); color: #ff4757; padding: 2px 6px; border-radius: 3px; font-weight: bold; font-size: 11px; margin-right: 8px;">WR</span> {row['wr3']}</div>
                        <div><span style="background: rgba(255, 165, 2, 0.15); color: #ffa502; padding: 2px 6px; border-radius: 3px; font-weight: bold; font-size: 11px; margin-right: 8px;">TE</span> {row['te']}</div>
                        <div><span style="background: rgba(164, 176, 190, 0.15); color: #a4b0be; padding: 2px 6px; border-radius: 3px; font-weight: bold; font-size: 11px; margin-right: 8px;">FLEX</span> {row['flex']}</div>
                    </div>
                </div>
                
                <!-- Right Side: Diagnosis Panel -->
                <div style="flex: 1; border-left: 1px solid rgba(255,255,255,0.1); padding-left: 20px; display: flex; flex-direction: column; justify-content: center;">
                    <div style="margin-bottom: 15px;">
                        <span style="color: #a4b0be; font-size: 11px; font-weight: bold; letter-spacing: 1px; text-transform: uppercase;">The Juicer Diagnosis</span><br/>
                        <span style="color: #f1f2f6; font-size: 13px;">Optimal positional allocation maximizing raw median volume.</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 10px;">
                        <span style="color: #a4b0be; font-size: 12px;">PROJ FANTASY POINTS</span>
                        <strong style="color: #2ed573;">{row['projected_score']}</strong>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Error loading DFS rosters: {e}")
"""

# Regex to safely replace the old DFS engine function
pattern = r"# --- DFS ENGINE.*?def render_dfs_engine\(\):.*?except Exception as e:.*?st\.error\(f\"Error loading DFS rosters: \{e\}\"\)"
if re.search(pattern, code, re.DOTALL):
    code = re.sub(pattern, new_dfs_ui.strip(), code, flags=re.DOTALL)
else:
    # If it doesn't exist, inject it at the top of the UI components (under imports)
    code = re.sub(r'(import pandas as pd)', r'\1\n\n' + new_dfs_ui.strip(), code)

with open("ui_components.py", "w", encoding="utf-8") as f:
    f.write(code)
print("✅ DFS Flexbox UI injected successfully.")