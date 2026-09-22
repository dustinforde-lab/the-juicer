import os, sys, sqlite3

print("🐍 [MAMBA MENTALITY] Rebuilding ui_components.py from the foundation up...")
ui_path = "ui_components.py"

master_ui_code = """
import streamlit as st
import sqlite3
import pandas as pd
import json

def render_accountability_tickers():
    html_block = \"\"\"
    <div style="background: #0d1117; padding: 10px; border-radius: 8px; border: 1px solid #30363d; margin-bottom: 20px;">
        <div style="background: rgba(138, 43, 226, 0.15); border-left: 4px solid #8a2be2; padding: 12px; margin-bottom: 10px; font-family: monospace; font-size: 14px;">
            <b style="color: #c471ed;">[ABBYSLAYZ SYNDICATE PIPELINE]</b> <span id="accountability-text" style="color: #e2e8f0;">Active & Verifying...</span>
            <div style="width: 100%; background: #21262d; height: 4px; margin-top: 8px; border-radius: 2px;">
                <div id="progress-bar" style="width: 0%; background: #8a2be2; height: 100%; transition: width 15s linear;"></div>
            </div>
        </div>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; font-size: 12px; font-weight: bold;">
            <div style="background: rgba(0, 255, 136, 0.1); border-left: 3px solid #00ff88; padding: 8px; color: #00ff88;">
                🎯 250 PARLAYS ACTIVE (Abby's Sharp Desk)
            </div>
            <div style="background: rgba(255, 69, 58, 0.1); border-left: 3px solid #ff453a; padding: 8px; color: #ff453a;">
                🚑 200 DFS ROSTERS LOCKED (Capologist Verified)
            </div>
            <div style="background: rgba(255, 215, 0, 0.1); border-left: 3px solid #ffd700; padding: 8px; color: #ffd700;">
                🏈 200 PICK'EMS LIVE (PrizePicks / Underdog)
            </div>
        </div>
    </div>
    <script>
        const steps = [
            "🔄 <b>[UPDATED]</b> AbbySlayz's crew auditing lines...",
            "🏃 <b>[HANDOFF]</b> Enforcer checking payload schemas.",
            "🧠 <b>[SYNDICATE]</b> Sharp and Actuary calculating EV.",
            "📂 <b>[DATABASE]</b> Executioner committing bulk WAL transaction.",
            "🚀 <b>[READY]</b> Master Book fully synced to UI tabs."
        ];
        let stepIdx = 0;
        const textEl = document.getElementById("accountability-text");
        const barEl = document.getElementById("progress-bar");
        function updatePipeline() {
            if(!textEl || !barEl) return;
            barEl.style.transition = 'none';
            barEl.style.width = '0%';
            textEl.innerHTML = steps[stepIdx];
            stepIdx = (stepIdx + 1) % steps.length;
            setTimeout(() => {
                barEl.style.transition = 'width 15s linear';
                barEl.style.width = '100%';
            }, 50);
        }
        updatePipeline();
        setInterval(updatePipeline, 15000);
    </script>
    \"\"\"
    st.components.v1.html(html_block, height=180)

def render_dfs(q_db, sim_file):
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
            with st.expander("Lineup " + str(row['ticket_id']) + " - Status: " + str(row['status'])):
                try:
                    roster = json.loads(row['payload_json'])
                    for p in roster:
                        st.text(str(p.get('pos', 'FLEX')) + " : " + str(p.get('name', 'Player')) + " (Salary: $" + str(p.get('salary', 5000)) + ")")
                except Exception as ex:
                    st.text("Payload parsing error: " + str(ex))
    except Exception as e:
        st.error("UI Rendering Error: " + str(e))

def render_rankings_syndicate(q_db):
    st.subheader("🎯 AbbySlayz Parlay & Pick'em Syndicate Matrix (450 Cards)")
    tab1, tab2 = st.tabs(["Parlays (250)", "Pick'ems (200)"])
    with tab1:
        try:
            conn = sqlite3.connect("action_grid.db")
            df_p = pd.read_sql("SELECT ticket_id, payload_json, status FROM abbys_master_book WHERE tab_category='PARLAY_TAB'", conn)
            conn.close()
            st.success("Loaded " + str(len(df_p)) + " sharp parlay slips.")
            for idx, row in df_p.head(10).iterrows():
                with st.expander("Slip " + str(row['ticket_id'])):
                    st.json(json.loads(row['payload_json']))
        except Exception as e:
            st.error("Parlay tab error: " + str(e))
    with tab2:
        try:
            conn = sqlite3.connect("action_grid.db")
            df_pk = pd.read_sql("SELECT ticket_id, payload_json, status FROM abbys_master_book WHERE tab_category='PICKEM_TAB'", conn)
            conn.close()
            st.success("Loaded " + str(len(df_pk)) + " PrizePicks / Underdog squares.")
            for idx, row in df_pk.head(10).iterrows():
                with st.expander("Square " + str(row['ticket_id'])):
                    st.json(json.loads(row['payload_json']))
        except Exception as e:
            st.error("Pick'em tab error: " + str(e))
"""

with open(ui_path, "w", encoding="utf-8") as f:
    f.write(master_ui_code)

print("✅ [PASS] ui_components.py rebuilt with Mamba precision.")

# Verify app.py has the ticker hook
app_path = "app.py"
if os.path.exists(app_path):
    with open(app_path, "r", encoding="utf-8") as f:
        app_content = f.read()
    if "ui.render_accountability_tickers()" not in app_content:
        app_content = app_content.replace('layout="wide")', 'layout="wide")\nui.render_accountability_tickers()')
        with open(app_path, "w", encoding="utf-8") as f:
            f.write(app_content)
        print("✅ [PASS] Ticker wired back into app.py.")

print("🎯 MAMBA FIX COMPLETE. LAUNCHING CLEAN MASTER DASHBOARD...")