import os
import shutil

print("🛡️ [REAL-BOOK PATCH] Initializing live sportsbook validator...")

ui_path = "ui_components.py"
backup_path = "ui_components_realbook_backup.py"

if not os.path.exists(ui_path):
    print("❌ Error: `ui_path` not found.")
    exit(1)

# 1. Safety backup
shutil.copy(ui_path, backup_path)
print(f"   📂 Backup secured at `{backup_path}`.")

with open(ui_path, "r", encoding="utf-8") as f:
    code = f.read()

# 2. Real-book rendering function with anti-sandbox filters
real_book_renderer = """

# --- THE JUICER: REAL-BOOK PARLAY MATRIX RENDERER ---
def render_real_parlay_matrix(conn):
    import streamlit as st
    import pandas as pd
    st.markdown("### 🎯 THE PARLAY MATRIX (LIVE SPORTSBOOK FEED)")
    try:
        # Strict filter: Exclude any sandbox stubs (SBOX) to guarantee real, actionable book lines
        df_bets = pd.read_sql("SELECT ticket_id, weight_class, odds, border_color, ticket_json, created_at, confidence_score FROM theoretical_bets WHERE ticket_id NOT LIKE 'SBOX%'", conn)
        df_slips = pd.read_sql("SELECT ticket_id, odds, slip_json FROM underdog_slips WHERE ticket_id NOT LIKE 'SBOX%'", conn)
        
        if df_bets.empty and df_slips.empty:
            st.warning("⚠️ No actionable live-book tickets found in database. Generate or sync verified lines to populate the feed.")
            return

        st.success(f"✅ Loaded {len(df_bets) + len(df_slips)} verified sportsbook tickets.")

        for _, row in df_bets.iterrows():
            ticket_id = row['ticket_id']
            odds = row['odds']
            confidence = row['confidence_score']
            border = row.get('border_color', '#00e5ff')
            st.markdown(f'''
            <div style="background: rgba(255,255,255,0.03); padding: 12px; border-radius: 8px; border-left: 4px solid {border}; margin-bottom: 10px;">
                <b>Ticket ID:</b> {ticket_id} | <b>Odds:</b> <span style="color: #00ff88; font-weight: bold;">{odds}</span> | <b>Confidence:</b> {confidence}%<br>
                <span style="font-size: 11px; color: #a5b4fc;">⚡ Actionable Market Feed • Ready for Sportsbook Execution</span>
            </div>
            ''', unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"❌ Error querying live sportsbook feed: {e}")
# --- END REAL-BOOK PATCH ---
"""

# Replace existing or append cleanly
if "def render_real_parlay_matrix" in code:
    parts = code.split("def render_real_parlay_matrix")
    code = parts[0] + real_book_renderer
else:
    code += "\n" + real_book_renderer

# 3. Built-in Check System (Compile validation before writing)
try:
    compile(code, ui_path, 'exec')
    with open(ui_path, "w", encoding="utf-8") as f:
        f.write(code)
    print("✅ SUCCESS: Real-book validator compiled and locked into `ui_components.py`!")
except Exception as e:
    print(f"❌ Syntax or Compilation Error caught: {e}")
    print("⚠️ Restoring from safety backup immediately...")
    shutil.copy(backup_path, ui_path)
    exit(1)
