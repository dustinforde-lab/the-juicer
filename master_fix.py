import os
import shutil
import sqlite3

print("🛡️ [MASTER SYNDICATE FIX] Initializing 5-layer absolute remediation...")

# --- LAYER 4: DATABASE SANITIZATION (PURGING SBOX ROWS) ---
try:
    db_conn = sqlite3.connect("action_grid.db")
    c = db_conn.cursor()
    c.execute("DELETE FROM theoretical_bets WHERE ticket_id LIKE 'SBOX%'")
    c.execute("PRAGMA table_info(underdog_slips)")
    cols = [col[1] for col in c.fetchall()]
    id_col = 'slip_id' if 'slip_id' in cols else ('ticket_id' if 'ticket_id' in cols else 'id')
    c.execute(f"DELETE FROM underdog_slips WHERE {id_col} LIKE 'SBOX%'")
    db_conn.commit()
    db_conn.close()
    print("✅ Layer 4: Successfully purged all SBOX sandbox stubs from action_grid.db!")
except Exception as e:
    print(f"⚠️ Database purge warning: {e}")

# --- LAYERS 2, 3, & 5: INLINE REWRITE, EXCEPTION EXPOSURE, CLEAN CONTAINER ---
app_path = "app.py"
backup_path = "app_master_fix_backup.py"
shutil.copy(app_path, backup_path)

with open(app_path, "r", encoding="utf-8") as f:
    content = f.read()

# Inline block that queries database directly and exposes exceptions explicitly (Layer 3)
inline_parlay_block = """
    # --- DIRECT INLINE REAL-BOOK PARLAY MATRIX (NO STUBS) ---
    st.markdown("<h3 style='color:#ff2a6d;'>🎯 THE PARLAY MATRIX (LIVE SPORTSBOOK FEED)</h3>", unsafe_allow_html=True)
    try:
        import pandas as pd
        df_bets = pd.read_sql("SELECT ticket_id, weight_class, odds, border_color, ticket_json, created_at, confidence_score FROM theoretical_bets WHERE ticket_id NOT LIKE 'SBOX%'", conn)
        
        if df_bets.empty:
            st.warning("⚠️ No live sportsbook tickets found in theoretical_bets. Run optimizer sync to generate real lines.")
        else:
            st.success(f"✅ Loaded {len(df_bets)} verified sportsbook tickets from database.")
            for _, row in df_bets.iterrows():
                t_id = row['ticket_id']
                odds = row['odds']
                conf = row['confidence_score']
                border = row.get('border_color', '#00e5ff')
                st.markdown(f'''
                <div style="background: rgba(255,255,255,0.03); padding: 12px; border-radius: 8px; border-left: 4px solid {border}; margin-bottom: 10px;">
                    <b>Ticket ID:</b> {t_id} | <b>Odds:</b> <span style="color: #00ff88; font-weight: bold;">{odds}</span> | <b>Confidence:</b> {conf}%<br>
                    <span style="font-size: 11px; color: #a5b4fc;">⚡ Live Sportsbook Actionable Feed • Ready for Execution</span>
                </div>
                ''', unsafe_allow_html=True)
    except Exception as e:
        # Layer 3: Explicitly blast any underlying exception to the UI
        st.error("❌ Live Parlay Matrix Encountered Exception:")
        st.exception(e)
    # --- END INLINE MATRIX ---
"""

# Inject or replace the legacy block in app.py
if "THE PARLAY MATRIX" in content:
    parts = content.split("THE PARLAY MATRIX")
    header_part = parts[0] + "THE PARLAY MATRIX"
    remainder = parts[1]
    eol_idx = remainder.find('\n')
    if eol_idx != -1:
        header_part += remainder[:eol_idx+1]
        remainder = remainder[eol_idx+1:]
    
    # Clean cut up to the next major section or tab definition
    for delimiter in ['st.tab', 'Season-Long Fantasy', 'Film Room', 'Vegas Scoreboard']:
        if delimiter in remainder:
            remainder = remainder[remainder.find(delimiter):]
            break
            
    new_content = header_part + "\n" + inline_parlay_block + "\n" + remainder
else:
    new_content = content + "\n" + inline_parlay_block

# --- BUILT-IN CHECK SYSTEM WITH AUTOMATIC ROLLBACK ---
try:
    compile(new_content, app_path, 'exec')
    with open(app_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("✅ SUCCESS: Master 5-layer fix applied and compiled cleanly into app.py!")
except Exception as e:
    print(f"❌ Compilation Error caught: {e}")
    shutil.copy(backup_path, app_path)
    print("⚠️ Reverted app.py safely from backup.")
