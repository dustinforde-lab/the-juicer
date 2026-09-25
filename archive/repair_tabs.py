import os
import shutil
import py_compile
import re

print("=" * 65)
print("🔧 [HOTFIX] Repairing t2 (DFS) & t4 (Parlay Matrix) Database Calls...")
print("=" * 65)

if not os.path.exists("app.py"):
    print("❌ Error: app.py not found.")
    exit(1)

shutil.copyfile("app.py", "app_backup_pre_repair.py")
print("   ✅ Backup created: app_backup_pre_repair.py")

with open("app.py", "r", encoding="utf-8-sig", errors="ignore") as f:
    content = f.read()

# 1. Cleanly rewrite the t2 block between 'with t2:' and 'with t3:'
t2_pattern = r'([ \t]*)with t2:.*?(?=[ \t]*with t3:)'
t2_replacement = r"""\1with t2:
\1    import sqlite3
\1    import pandas as pd
\1    st.markdown("<h3 style='color:#00e5ff;'>👑 DFS OPTIMIZER & SOLVENCY ENGINE</h3>", unsafe_allow_html=True)
\1    try:
\1        with sqlite3.connect("action_grid.db") as conn:
\1            df_donna = pd.read_sql("SELECT player_name, team, projected_ownership, vibe_rating, updated_at FROM ownership_projections ORDER BY updated_at DESC", conn)
\1        
\1        if not df_donna.empty:
\1            st.markdown("<h5 style='color:#8b949e;'>Donna's Leverage Matrix</h5>", unsafe_allow_html=True)
\1            for _, row in df_donna.iterrows():
\1                vibe_color = "#ff2a6d" if row['vibe_rating'] == "FADE" else "#00ff88"
\1                card = f'''
\1                <div style="background: #121824; border-left: 4px solid {vibe_color}; padding: 12px; margin-bottom: 8px; border-radius: 4px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
\1                    <div style="display: flex; justify-content: space-between;">
\1                        <span style="color: #e6edf3; font-weight: 800;">{row['player_name']} <span style="color:#8b949e; font-size:0.85rem;">({row['team']})</span></span>
\1                        <span style="color: {vibe_color}; font-weight: 900; letter-spacing: 1px;">{row['vibe_rating']}</span>
\1                    </div>
\1                    <div style="display: flex; justify-content: space-between; margin-top: 6px;">
\1                        <span style="color: #8b949e; font-size: 0.85rem; font-weight: 600;">Proj Own: {row['projected_ownership']}</span>
\1                        <span style="color: #6e7681; font-size: 0.75rem; font-family: monospace;">🕒 LINE LOCKED: {row['updated_at']}</span>
\1                    </div>
\1                </div>
\1                '''
\1                st.markdown(card, unsafe_allow_html=True)
\1            st.markdown("<br>", unsafe_allow_html=True)
\1        else:
\1            st.caption("Awaiting Donna's DFS vibe checks...")
\1    except Exception as e:
\1        st.error(f"DFS Engine Offline: {e}")
\1    
\1    ui.render_dfs(q_db, SIM_FILE)
"""

content = re.sub(t2_pattern, t2_replacement, content, count=1, flags=re.DOTALL)

# 2. Cleanly rewrite the t4 block between 'with t4:' and 'with t5:'
t4_pattern = r'([ \t]*)with t4:.*?(?=[ \t]*with t5:)'
t4_replacement = r"""\1with t4:
\1    import sqlite3
\1    import pandas as pd
\1    import ui_components as ui
\1    st.markdown("<h3 style='color:#ff2a6d;'>🎯 THE PARLAY MATRIX (MULTI-BOOK STAMPED)</h3>", unsafe_allow_html=True)
\1    try:
\1        with sqlite3.connect("action_grid.db") as conn:
\1            df = pd.read_sql("SELECT * FROM theoretical_bets ORDER BY created_at DESC", conn)
\1        if not df.empty:
\1            for _, row in df.iterrows():
\1                card_html = ui.render_stamped_parlay_card(
\1                    row['ticket_id'], row['weight_class'], row['odds'], 
\1                    row['border_color'], row['ticket_json'], row['source'], row['created_at']
\1                )
\1                st.markdown(card_html, unsafe_allow_html=True)
\1        else:
\1            st.caption("Awaiting correlation engine feeds...")
\1    except Exception as e:
\1        st.error(f"Matrix Offline: {e}")
"""

content = re.sub(t4_pattern, t4_replacement, content, count=1, flags=re.DOTALL)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

try:
    py_compile.compile("app.py", doraise=True)
    print("   ✅ app.py compiled with zero errors.")
    print("=" * 65)
    print("🟢 REPAIR COMPLETE: Both tabs now use standalone database connections.")
    print("=" * 65)
except Exception as err:
    print(f"❌ Syntax error detected: {err}. Restoring backup...")
    shutil.copyfile("app_backup_pre_repair.py", "app.py")
