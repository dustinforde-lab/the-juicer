import os
import re
import shutil

print("=" * 65)
print("💉 [PHASE 2 - MOD 9] Surgically Upgrading Parlay Matrix (t4)...")
print("=" * 65)

if not os.path.exists("app.py"):
    print("❌ Error: app.py not found.")
    exit(1)

# 1. Take a Pre-Flight Backup
shutil.copyfile("app.py", "app_backup_pre_t4.py")
print("   ✅ Pre-flight backup created: app_backup_pre_t4.py")

with open("app.py", "r", encoding="utf-8-sig") as f:
    content = f.read()

# 2. Safely locate and replace the t4 block using regex to preserve indentation
pattern = r'([ \t]*)with t4:\s+ui\.render_parlays\(q_db\)'

new_t4_logic = r"""\1with t4:
\1    import pandas as pd
\1    import ui_components as ui
\1    st.markdown("<h3 style='color:#ff2a6d;'>🎯 THE PARLAY MATRIX (MULTI-BOOK STAMPED)</h3>", unsafe_allow_html=True)
\1    try:
\1        conn = q_db() if callable(q_db) else q_db
\1        df = pd.read_sql("SELECT * FROM theoretical_bets ORDER BY created_at DESC", conn)
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
\1        st.error(f"Matrix Offline: {e}")"""

if re.search(pattern, content):
    content = re.sub(pattern, new_t4_logic, content, count=1)
    print("   ✅ Parlay Matrix logic successfully upgraded to use multi-book cards.")
else:
    print("   ❌ Error: Could not find exact 'with t4:' block. Aborting injection.")
    exit(1)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("=" * 65)
print("🟢 INJECTION COMPLETE: app.py successfully upgraded.")
print("=" * 65)
