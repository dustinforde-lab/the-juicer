import os
import re
import shutil

print("=" * 65)
print("💉 [PHASE 2 - MOD 10] Surgically Upgrading DFS Optimizer (t2)...")
print("=" * 65)

if not os.path.exists("app.py"):
    print("❌ Error: app.py not found.")
    exit(1)

# 1. Take a Final Pre-Flight Backup
shutil.copyfile("app.py", "app_backup_pre_t2.py")
print("   ✅ Pre-flight backup created: app_backup_pre_t2.py")

with open("app.py", "r", encoding="utf-8-sig") as f:
    content = f.read()

# 2. Safely locate and replace the t2 block using regex
pattern = r'([ \t]*)with t2:\s+ui\.render_dfs\(q_db,\s*SIM_FILE\)'

new_t2_logic = r"""\1with t2:
\1    import pandas as pd
\1    st.markdown("<h3 style='color:#00e5ff;'>👑 DFS OPTIMIZER & SOLVENCY ENGINE</h3>", unsafe_allow_html=True)
\1    try:
\1        conn = q_db() if callable(q_db) else q_db
\1        df_donna = pd.read_sql("SELECT player_name, team, projected_ownership, vibe_rating, updated_at FROM ownership_projections ORDER BY updated_at DESC", conn)
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
\1            
\1        # Retain original rendering underneath
\1        ui.render_dfs(q_db, SIM_FILE)
\1    except Exception as e:
\1        st.error(f"DFS Engine Offline: {e}")
\1        ui.render_dfs(q_db, SIM_FILE)"""

if re.search(pattern, content):
    content = re.sub(pattern, new_t2_logic, content, count=1)
    print("   ✅ DFS Optimizer logic successfully upgraded with Donna's Matrix.")
else:
    print("   ❌ Error: Could not find exact 'with t2:' block. Aborting injection.")
    exit(1)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("=" * 65)
print("🟢 FINAL INJECTION COMPLETE: app.py successfully upgraded.")
print("=" * 65)
