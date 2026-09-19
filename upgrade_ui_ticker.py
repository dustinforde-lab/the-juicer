import os, ast, sqlite3

UI_FILE = "ui_components.py"

TICKER_FUNCTION_CODE = '''

# --- LIVE AGENT TELEMETRY TICKER ---
def render_live_telemetry_ticker():
    import streamlit as st
    import sqlite3

    with sqlite3.connect("action_grid.db") as conn:
        cur = conn.cursor()
        try:
            msgs = cur.execute("SELECT sender, directive, target, action, timestamp FROM agent_chatter ORDER BY message_id DESC LIMIT 5").fetchall()
        except Exception:
            msgs = []

    if not msgs:
        return

    st.markdown("""
        <style>
            .telemetry-container {
                background: #0d1117;
                border: 1px solid #30363d;
                border-left: 4px solid #00e5ff;
                border-radius: 6px;
                padding: 8px 14px;
                margin-bottom: 12px;
                display: flex;
                flex-direction: column;
                gap: 4px;
            }
            .telemetry-row {
                display: flex;
                justify-content: space-between;
                font-size: 0.78rem;
                font-family: monospace;
            }
        </style>
    """, unsafe_allow_html=True)

    ticker_html = "<div class='telemetry-container'>"
    for sender, directive, target, action, ts in msgs:
        color = "#00ff88" if action == "FORCE INCLUDE" else ("#ff2a6d" if action == "HARD PURGE" else "#00e5ff")
        ticker_html += f"""
        <div class='telemetry-row'>
            <span style='color:{color}; font-weight:700;'>[{sender.upper()}] {directive} &rarr; {target}</span>
            <span style='color:#8b949e;'>ACTION: {action} | {ts}</span>
        </div>
        """
    ticker_html += "</div>"
    st.markdown(ticker_html, unsafe_allow_html=True)
'''

def apply_ticker_upgrade():
    print("=" * 65)
    print("🎨 [UPGRADE CHUNK 12] Injecting Live Telemetry Ticker...")
    print("=" * 65)

    with open(UI_FILE, "r", encoding="utf-8-sig") as f:
        existing = f.read()

    if "def render_live_telemetry_ticker(" not in existing:
        with open(UI_FILE, "a", encoding="utf-8") as f:
            f.write(TICKER_FUNCTION_CODE)
        print("   [OK] Appended render_live_telemetry_ticker() to ui_components.py")
    else:
        print("   [NOTE] render_live_telemetry_ticker() already present.")

def run_self_test():
    with open(UI_FILE, "r", encoding="utf-8-sig") as f:
        tree = ast.parse(f.read())
    funcs = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    assert "render_live_telemetry_ticker" in funcs, "Integrity Failure: Ticker function missing from AST."
    print("✅ TICKER INTEGRATION VERIFIED: UI component parsed cleanly with zero syntax errors.\n")

if __name__ == "__main__":
    apply_ticker_upgrade()
    run_self_test()
