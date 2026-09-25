import os, ast

UI_FILE = "ui_components.py"

UPGRADED_CARD_FUNCTION = """

# --- INTELLIGENCE-ENRICHED PARLAY CARD RENDERER ---
def render_enhanced_parlay_card(ticket_id, tier, odds, color, legs, source, updated_at, confidence_score=None):
    import streamlit as st
    
    score_display = ""
    if confidence_score:
        score_color = "#00ff88" if confidence_score >= 85 else ("#00e5ff" if confidence_score >= 75 else "#ffaa00")
        score_display = f"<span style='background: #111622; border: 1px solid {score_color}; color: {score_color}; font-size: 0.72rem; font-weight: 800; padding: 2px 8px; border-radius: 12px;'>🎯 {confidence_score}/100 CONFIDENCE</span>"
        
    has_sharp = any("Deebo" in l.get("player", "") or "Javonte" in l.get("player", "") for l in legs)
    sharp_badge = "<span style='background: rgba(255, 42, 109, 0.15); border: 1px solid #ff2a6d; color: #ff2a6d; font-size: 0.72rem; font-weight: 800; padding: 2px 8px; border-radius: 12px; margin-left: 6px;'>🔥 +EV SHARP</span>" if has_sharp else ""

    legs_html = ""
    for leg in legs:
        p_name = leg.get("player", "Unknown")
        team = leg.get("team", "")
        stat = leg.get("stat", "")
        legs_html += f'''
        <div style="padding: 6px 0; border-top: 1px solid rgba(255,255,255,0.06); display: flex; justify-content: space-between; align-items: center;">
            <span style="color: #00e5ff; font-weight: 700; font-size: 0.88rem;">🏈 {p_name} <span style="color:#8b949e; font-size:0.75rem;">({team})</span></span>
            <span style="color: #e6edf3; font-weight: 600; font-size: 0.85rem;">{stat}</span>
        </div>
        '''

    card_html = f'''
    <div style="background: #151a26; border-radius: 10px; padding: 16px; border: 1px solid #212838; border-left: 5px solid {color}; margin-bottom: 16px; box-shadow: 0 4px 14px rgba(0,0,0,0.35);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <span style="font-weight: 800; color: #ffffff; font-size: 0.95rem;">{ticket_id}</span>
            <span style="font-weight: 900; color: #00ff88; font-size: 1.15rem;">{odds}</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <span style="font-size: 0.75rem; color: #8b949e;">[{source}] Generated: {updated_at}</span>
            <div>{score_display}{sharp_badge}</div>
        </div>
        {legs_html}
    </div>
    '''
    st.markdown(card_html, unsafe_allow_html=True)
"""

def inject_enhanced_cards():
    print("=" * 65)
    print("🎨 [PHASE 3: STEP 1] Injecting Intelligence Card Badges...")
    print("=" * 65)
    
    with open(UI_FILE, "r", encoding="utf-8-sig") as f:
        existing = f.read()
        
    if "def render_enhanced_parlay_card(" not in existing:
        with open(UI_FILE, "a", encoding="utf-8") as f:
            f.write(UPGRADED_CARD_FUNCTION)
        print("   [OK] Appended render_enhanced_parlay_card() to ui_components.py")
    else:
        print("   [NOTE] render_enhanced_parlay_card() already installed.")

def run_self_test():
    with open(UI_FILE, "r", encoding="utf-8-sig") as f:
        tree = ast.parse(f.read())
    funcs = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    assert "render_enhanced_parlay_card" in funcs, "AST Failure: Card function missing."
    print("✅ CARD BADGES READY: Component cleanly compiled into UI module.\n")

if __name__ == "__main__":
    inject_enhanced_cards()
    run_self_test()
