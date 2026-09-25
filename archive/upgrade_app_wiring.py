import os, ast, glob

APP_FILE = "app.py"

def wire_app_navigation():
    print("=" * 65)
    print("🔌 [UPGRADE CHUNK 4] Wiring Underdog Hub to Main Application...")
    print("=" * 65)

    if not os.path.exists(APP_FILE):
        print(f"❌ Error: {APP_FILE} not found.")
        return

    with open(APP_FILE, "r", encoding="utf-8-sig") as f:
        code = f.read()

    if "render_underdog_hub" not in code:
        injection = """

# --- [AUTO-INJECTED] UNDERDOG HUB NAVIGATION ---
import ui_components
import streamlit as st

st.sidebar.markdown("---")
if st.sidebar.checkbox("⚡ Show Underdog Prop Hub", value=False, key="chk_show_ud_hub"):
    ui_components.render_underdog_hub()
"""
        with open(APP_FILE, "a", encoding="utf-8") as f:
            f.write(injection)
        print("   [OK] Underdog Hub toggle injected into app.py sidebar.")
    else:
        print("   [NOTE] Underdog Hub is already wired into app.py.")

def final_system_audit():
    print("\n🧪 [FINAL SYSTEM AUDIT] Sweeping entire project for syntax errors...")
    scripts = glob.glob("*.py")
    error_count = 0
    for script in scripts:
        try:
            with open(script, "r", encoding="utf-8-sig") as f:
                ast.parse(f.read())
            print(f"   • [PASS] {script}")
        except Exception as e:
            print(f"   • [FAIL] {script} -> {e}")
            error_count += 1
            
    if error_count == 0:
        print("\n✅ SYSTEM GREEN: Zero syntax errors detected across the codebase.")
    else:
        print(f"\n⚠️ SYSTEM HALTED: Detected {error_count} broken files. Check logs.")

if __name__ == "__main__":
    wire_app_navigation()
    final_system_audit()
