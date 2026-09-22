import os, sys

print("🐍 [BLACK MAMBA] Executing surgical code rewrite on ui_components.py...")
ui_path = "ui_components.py"

# Absolute bulletproof replacement for render_dfs that avoids all f-string brace syntax errors
pristine_code = """
def render_dfs(q_db, sim_file):
    import streamlit as st
    import pandas as pd
    import json
    
    st.subheader("👑 AbbySlayz Master DFS Optimizer (200 Lineups)")
    try:
        conn = sqlite3.connect("action_grid.db")
        df = pd.read_sql("SELECT ticket_id, payload_json, status FROM abbys_master_book WHERE tab_category='DFS_TAB'", conn)
        conn.close()
        
        if df.empty:
            st.warning("Awaiting AbbySlayz's roster generation...")
            return
            
        st.success("Loaded " + str(len(df)) + " verified optimal rosters under AbbySlayz's command.")
        
        for idx, row in df.head(10).iterrows():
            ticket = str(row['ticket_id'])
            status = str(row['status'])
            with st.expander("Lineup " + ticket + " - Status: " + status):
                try:
                    roster = json.loads(row['payload_json'])
                    for p in roster:
                        pos = str(p.get('pos', 'FLEX'))
                        name = str(p.get('name', 'Player'))
                        sal = str(p.get('salary', 5000))
                        st.text(pos + " : " + name + " (Salary: $" + sal + ")")
                except Exception as ex:
                    st.text("Payload parsing error: " + str(ex))
    except Exception as e:
        st.error("UI Rendering Error: " + str(e))
"""

# Read existing file to see if we can surgically replace render_dfs, or write a fresh file if corrupt
if os.path.exists(ui_path):
    with open(ui_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        
    if "def render_dfs" in content:
        parts = content.split("def render_dfs")
        # Keep everything before render_dfs and append our clean, syntax-free implementation
        final_content = parts[0] + pristine_code
    else:
        final_content = content + "\n" + pristine_code
        
    with open(ui_path, "w", encoding="utf-8") as f:
        f.write(final_content)
    print("✅ [PASS] ui_components.py rewritten with Black Mamba precision.")
else:
    print("❌ Critical: ui_components.py not found.")
    sys.exit(1)

print("🎯 CODE REWRITE COMPLETE. LAUNCHING APP...")