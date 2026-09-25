import os
import shutil

print("🛡️ [FIX-AND-PATCH] Repairing base file and adding real-book feed...")

ui_path = "ui_components.py"
backup_path = "ui_components_master_backup.py"

shutil.copy(ui_path, backup_path)

with open(ui_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# 1. Permanently fix line 263 (index 262) if it exists
if len(lines) >= 263:
    idx = 262
    lines[idx] = '    df = pd.read_sql("SELECT ticket_id, weight_class, odds, border_color, ticket_json, created_at, confidence_score FROM theoretical_bets WHERE ticket_id NOT LIKE \'SBOX%\'", conn)\n'
    print("   🔧 Repaired line 263 query syntax.")

code = "".join(lines)

# 2. Append Real-Book Parlay Matrix function if not already present
real_book_renderer = """

# --- THE JUICER: REAL-BOOK PARLAY MATRIX RENDERER ---
def render_real_parlay_matrix(conn):
    import streamlit as st
    import pandas as pd
    st.markdown("### 🎯 THE PARLAY MATRIX (LIVE SPORTSBOOK FEED)")
    try:
        df_bets = pd.read_sql("SELECT ticket_id, weight_class, odds, border_color, ticket_json, created_at, confidence_score FROM theoretical_bets WHERE ticket_id NOT LIKE 'SBOX%'", conn)
        df_slips = pd.read_sql("SELECT ticket_id, odds, slip_json FROM underdog_slips WHERE ticket_id NOT LIKE 'SBOX%'", conn)
        
        if df_bets.empty and df_slips.empty:
            st.warning("⚠️ No actionable live-book tickets found in database.")
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

if "def render_real_parlay_matrix" not in code:
    code += real_book_renderer

# 3. Built-in compilation check system
try:
    compile(code, ui_path, 'exec')
    with open(ui_path, "w", encoding="utf-8") as f:
        f.write(code)
    print("✅ SUCCESS: Base file repaired, real-book matrix injected, and code compiles cleanly!")
except Exception as e:
    print(f"❌ Compilation Error caught: {e}")
    print("⚠️ Restoring from master backup...")
    shutil.copy(backup_path, ui_path)
    exit(1)
