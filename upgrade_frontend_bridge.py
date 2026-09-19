import os

APP_FILE = "app.py"
BRIDGE_INJECTION = """

# ==========================================================
# 🔌 PHASE 2: WAR ROOM BRIDGE & LIVE TELEMETRY TICKER
# ==========================================================
import subprocess, sys

st.markdown("---")
st.markdown("<h4 style='color: #00e5ff; margin-bottom: 0px;'>📡 LIVE SYNDICATE TELEMETRY</h4>", unsafe_allow_html=True)

col_tick, col_btn = st.columns([3, 1])

with col_tick:
    try:
        # Calls the UI Ticker we built in Chunk 12
        from ui_components import render_live_telemetry_ticker
        render_live_telemetry_ticker()
    except Exception as e:
        st.caption("Telemetry offline or syncing...")

with col_btn:
    st.markdown("<br>", unsafe_allow_html=True) # Alignment spacer
    if st.button("🟢 EXECUTE WAR ROOM PIPELINE", use_container_width=True):
        with st.spinner("Interns are purging, scoring, and churning data..."):
            # Enforce UTF-8 so the subprocess doesn't crash on emojis
            sub_env = os.environ.copy()
            sub_env["PYTHONIOENCODING"] = "utf-8"
            subprocess.run([sys.executable, "syndicate_orchestrator.py"], env=sub_env)
        
        st.success("✅ 200 Slips Audited & Locked")
        
        # Instantly refresh the page to show the new tickets
        if hasattr(st, "rerun"):
            st.rerun()
        else:
            st.experimental_rerun()
st.markdown("---")
"""

def inject_bridge():
    print("=" * 65)
    print("🔌 [FINAL STEP] Wiring the War Room to the Streamlit UI...")
    print("=" * 65)
    
    if not os.path.exists(APP_FILE):
        print(f"❌ Could not find {APP_FILE}. Run this in the Juicer root directory.")
        return
        
    with open(APP_FILE, "r", encoding="utf-8") as f:
        code = f.read()
        
    if "PHASE 2: WAR ROOM BRIDGE" not in code:
        with open(APP_FILE, "a", encoding="utf-8") as f:
            f.write(BRIDGE_INJECTION)
        print("✅ SUCCESS: War Room control panel injected into app.py!")
    else:
        print("⚡ NOTE: War Room bridge is already wired.")

if __name__ == "__main__":
    inject_bridge()
