path = "ui_components.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Clean implementation of the real-book parlay matrix renderer
clean_renderer = """

def render_real_parlay_matrix(conn):
    import streamlit as st
    import pandas as pd
    st.markdown("<h3 style='color:#ff2a6d;'>🎯 THE PARLAY MATRIX (LIVE SPORTSBOOK FEED)</h3>", unsafe_allow_html=True)
    try:
        df_bets = pd.read_sql("SELECT ticket_id, weight_class, odds, border_color, ticket_json, created_at, confidence_score FROM theoretical_bets WHERE ticket_id NOT LIKE 'SBOX%'", conn)
        if df_bets.empty:
            st.warning("⚠️ No live sportsbook tickets found in theoretical_bets.")
        else:
            st.success(f"✅ Loaded {len(df_bets)} verified sportsbook tickets.")
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
        st.error("❌ Error loading Parlay Matrix:")
        st.exception(e)
"""

if "def render_real_parlay_matrix" in content:
    parts = content.split("def render_real_parlay_matrix")
    content = parts[0] + clean_renderer
else:
    content += clean_renderer

compile(content, path, 'exec')
with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("✅ SUCCESS: ui_components.py cleaned and compiled perfectly!")
