import os, ast, sqlite3

UI_FILE = "ui_components.py"
DB_FILE = "action_grid.db"

HUB_FUNCTION_CODE = '''

# --- UNDERDOG PROP HUB COMPONENT ---
def render_underdog_hub():
    import streamlit as st
    import sqlite3, json
    
    st.markdown("<h2 style=\"color:#00e5ff; margin-bottom:4px;\">⚡ Underdog Fantasy Prop Hub</h2>", unsafe_allow_html=True)
    st.caption("Pre-calculated Pick'em slips mapped to official Underdog multiplier curves.")

    with sqlite3.connect("action_grid.db") as conn:
        cur = conn.cursor()
        try:
            rows = cur.execute("SELECT slip_id, entry_type, payout_mult, legs_count, props_json, source, created_at FROM underdog_slips").fetchall()
        except Exception:
            rows = []

    if not rows:
        st.warning("⚠️ No Underdog entries found. Run upgrade_underdog_hub.py first.")
        return

    tier_options = ["ALL"] + sorted(list(set(r[1] for r in rows)))
    selected_tier = st.selectbox("Select Multiplier Class", tier_options, key="ud_hub_tier_select")
    
    active_slips = [r for r in rows if selected_tier == "ALL" or r[1] == selected_tier]
    st.write(f"Showing **{len(active_slips)}** active entries:")

    cols = st.columns(2)
    for idx, (sid, etype, mult, lcnt, pjson, src, ts) in enumerate(active_slips[:40]):
        props = json.loads(pjson)
        card_html = f"""
        <div style="background:#151922; border-left: 4px solid #ff2a6d; border-radius:8px; padding:12px; margin-bottom:12px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-weight:700; color:#fff; font-size:0.9rem;">{sid}</span>
                <span style="font-weight:800; color:#00ff88; font-size:1.0rem;">{mult}</span>
            </div>
            <div style="font-size:0.75rem; color:#8b949e; margin-bottom:8px;">{src} • {ts}</div>
            {''.join([f'<div style="font-size:0.85rem; padding:4px 0; border-top:1px solid #21262d;"><span style="color:#00e5ff;">{p.get("icon","⚡")} {p["player"]} ({p["team"]})</span>: <span style="color:#e6edf3;">{p["stat"]}</span></div>' for p in props])}
        </div>
        """
        with cols[idx % 2]:
            st.markdown(card_html, unsafe_allow_html=True)
'''

def apply_ui_upgrade():
    print("=" * 65)
    print("🎨 [UPGRADE CHUNK 3] Wiring Underdog Hub & Sourced UI Components...")
    print("=" * 65)

    if not os.path.exists(UI_FILE):
        print(f"❌ Error: {UI_FILE} not found.")
        return

    with open(UI_FILE, "r", encoding="utf-8") as f:
        existing_code = f.read()

    if "def render_underdog_hub(" not in existing_code:
        with open(UI_FILE, "a", encoding="utf-8") as f:
            f.write(HUB_FUNCTION_CODE)
        print("   [OK] Appended render_underdog_hub() cleanly to ui_components.py")
    else:
        print("   [NOTE] render_underdog_hub() is already wired in ui_components.py")

def run_self_test():
    print("\n🧪 [SELF-CHECK GATE] Verifying AST syntax and database bindings...")
    with open(UI_FILE, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())
    funcs = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    assert "render_underdog_hub" in funcs, "Integrity Failure: render_underdog_hub() not registered in AST."
    print("   • [PASS] ui_components.py compiled cleanly with zero syntax errors.")

    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        ud_count = cur.execute("SELECT COUNT(*) FROM underdog_slips").fetchone()[0]
        bet_count = cur.execute("SELECT COUNT(*) FROM theoretical_bets WHERE source IS NOT NULL").fetchone()[0]
        assert ud_count > 0, "Binding Failure: No records found in underdog_slips."
        assert bet_count > 0, "Binding Failure: theoretical_bets missing bookmaker sources."
    print(f"   • [PASS] Database linkages active: {ud_count} Underdog slips, {bet_count} sourced bets.")
    print("\n✅ CHUNK 3 COMPLETE: UI component wired, verified, and ready.\n")

if __name__ == "__main__":
    apply_ui_upgrade()
    run_self_test()
