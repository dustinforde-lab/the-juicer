import sqlite3, os, re

print("🚨 EXECUTING ACCOUNTABILITY PROTOCOL...")

# 1. PURGE THE GHOST DATA FROM THE DATABASE
try:
    conn = sqlite3.connect("action_grid.db")
    c = conn.cursor()
    # Erase Lewis's fake parlay data
    c.execute("DELETE FROM theoretical_bets WHERE ticket_id LIKE 'SLIP-%' OR ticket_json LIKE '%Starter Prop%' OR ticket_json LIKE '%Core Alpha%'")
    # Erase Dom's bad classic lineups to force a clean rebuild
    c.execute("DELETE FROM dfs_classic_lineups")
    conn.commit()
    conn.close()
    print("✅ DATABASE PURGED: Lewis's fake parlay tickets and Dom's broken lineups have been exterminated.")
except Exception as e:
    print(f"⚠️ DB Purge Issue: {e}")

# 2. INJECT THE ACCOUNTABILITY TICKER INTO UI_COMPONENTS
ui_path = "ui_components.py"
with open(ui_path, "r", encoding="utf-8", errors="ignore") as f:
    ui_content = f.read()

# Remove old ticker functions to prevent conflicts
ui_content = re.sub(r"def render_accountability_tickers\(.*?(?=def |\Z)", "", ui_content, flags=re.DOTALL)

ticker_code = """
def render_accountability_tickers():
    import streamlit as st
    
    # Custom HTML/JS for the 15-second Accountability Loop & Category Tickers
    html_block = \"\"\"
    <div style="background: #0d1117; padding: 10px; border-radius: 8px; border: 1px solid #30363d; margin-bottom: 20px;">
        <!-- PURPLE ACCOUNTABILITY TICKER -->
        <div style="background: rgba(138, 43, 226, 0.15); border-left: 4px solid #8a2be2; padding: 12px; margin-bottom: 10px; font-family: monospace; font-size: 14px;">
            <b style="color: #c471ed;">[INTERNAL AFFAIRS PIPELINE]</b> <span id="accountability-text" style="color: #e2e8f0;">Initializing tracking...</span>
            <div style="width: 100%; background: #21262d; height: 4px; margin-top: 8px; border-radius: 2px;">
                <div id="progress-bar" style="width: 0%; background: #8a2be2; height: 100%; transition: width 15s linear;"></div>
            </div>
        </div>
        
        <!-- THE 3 DATA TICKERS -->
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; font-size: 12px; font-weight: bold;">
            <div style="background: rgba(0, 255, 136, 0.1); border-left: 3px solid #00ff88; padding: 8px; color: #00ff88;">
                🎯 BETTING FEED: Awaiting live sharp action...
            </div>
            <div style="background: rgba(255, 69, 58, 0.1); border-left: 3px solid #ff453a; padding: 8px; color: #ff453a;">
                🚑 INJURY WARD: Awaiting Mike's intelligence...
            </div>
            <div style="background: rgba(255, 215, 0, 0.1); border-left: 3px solid #ffd700; padding: 8px; color: #ffd700;">
                🏈 SCORING FEED: Awaiting live game telemetry...
            </div>
        </div>
    </div>

    <script>
        const steps = [
            "🔄 <b>[UPDATED]</b> Interns are working...",
            "🏃 <b>[HANDOFF]</b> Intern brings raw information to Lewis.",
            "🧠 <b>[LEWIS]</b> Lewis talks to the information and evaluates it.",
            "📂 <b>[HANDOFF]</b> Lewis gets done with it, gives it to Mike.",
            "📊 <b>[MIKE]</b> Mike looks at it and evaluates projections.",
            "🗣️ <b>[WAR ROOM]</b> Mike and Donna talk, hash out their shit.",
            "🚀 <b>[DEPLOY]</b> Mike and Donna send finalized slate down the pipeline."
        ];
        
        let stepIdx = 0;
        const textEl = document.getElementById("accountability-text");
        const barEl = document.getElementById("progress-bar");
        
        function updatePipeline() {
            // Reset progress bar
            barEl.style.transition = 'none';
            barEl.style.width = '0%';
            
            // Update text
            textEl.innerHTML = steps[stepIdx];
            stepIdx = (stepIdx + 1) % steps.length;
            
            // Start progress bar animation
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
"""

with open(ui_path, "w", encoding="utf-8") as f:
    f.write(ui_content.strip() + "\n\n" + ticker_code)

# 3. WIRE IT INTO APP.PY
app_path = "app.py"
with open(app_path, "r", encoding="utf-8") as f:
    app_content = f.read()

if "ui.render_accountability_tickers()" not in app_content:
    # Inject it right under the page config
    app_content = app_content.replace('layout="wide")', 'layout="wide")\nui.render_accountability_tickers()')
    with open(app_path, "w", encoding="utf-8") as f:
        f.write(app_content)

print("✅ UI OVERRIDE: Accountability Ticker injected to front page.")