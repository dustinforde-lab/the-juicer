import re
import shutil
import py_compile
import os

print("=" * 65)
print("🔧 [HOTFIX] Removing Whitespace Indentation from Card HTML...")
print("=" * 65)

# --- 1. Fix ui_components.py ---
if os.path.exists("ui_components.py"):
    shutil.copyfile("ui_components.py", "ui_components_backup_pre_htmlfix.py")
    with open("ui_components.py", "r", encoding="utf-8", errors="ignore") as f:
        comp_content = f.read()

    # Remove any existing render_stamped_parlay_card implementations
    comp_content = re.sub(r'def render_stamped_parlay_card\(.*', '', comp_content, flags=re.DOTALL).rstrip()

    clean_card_func = """

def render_stamped_parlay_card(ticket_id, tier, odds, border_color, legs_json, source, created_at):
    import json
    try:
        legs = json.loads(legs_json)
    except Exception:
        legs = []
        
    sb_color = "#17e6a1" if "DraftKings" in source else "#107aca" if "FanDuel" in source else "#fdb927" if "MGM" in source.upper() else "#8b949e"
    sb_logo = "👑" if "DraftKings" in source else "🛡️" if "FanDuel" in source else "🦁" if "MGM" in source.upper() else "⚡"
    
    legs_html = ""
    for leg in legs:
        stat_low = leg.get('stat', '').lower()
        pos = "QB" if "pass" in stat_low else "WR" if "rec" in stat_low else "RB" if "rush" in stat_low else "FLEX"
        pos_color = "#00e5ff" if pos == "QB" else "#ffaa00" if pos == "WR" else "#00ff88"
        
        legs_html += f'''<div style="display: flex; align-items: center; background: #121824; margin-top: 8px; padding: 12px; border-radius: 8px; border-left: 4px solid {pos_color};">
<div style="flex-grow: 1;">
<div style="font-weight: 800; color: #e6edf3; font-size: 1.1rem;">{leg.get('player', '')}</div>
<div style="font-size: 0.9rem; color: #8b949e; margin-top: 4px; font-weight: 600;">{leg.get('team', '')} | {leg.get('stat', '')}</div>
</div>
</div>'''
        
    html = f'''<div style="background: linear-gradient(145deg, #171d2b 0%, #0b0e14 100%); border: 1px solid {border_color}40; border-top: 4px solid {border_color}; border-radius: 12px; padding: 18px; margin-bottom: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
<div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #212838; padding-bottom: 12px; margin-bottom: 12px;">
<div>
<span style="color: {border_color}; font-weight: 900; font-size: 0.85rem; letter-spacing: 2px;">{tier}</span><br>
<span style="color: #8b949e; font-size: 0.75rem; font-family: monospace;">{ticket_id}</span>
</div>
<div style="text-align: right;">
<span style="color: #fff; font-weight: 900; font-size: 1.5rem;">{odds}</span><br>
<span style="color: {sb_color}; font-size: 0.85rem; font-weight: 800; letter-spacing: 0.5px;">{sb_logo} {source.upper()}</span>
</div>
</div>
{legs_html}
<div style="margin-top: 18px; padding-top: 12px; border-top: 1px dashed #212838; display: flex; justify-content: space-between; align-items: center;">
<span style="color: #6e7681; font-size: 0.75rem; font-family: monospace; font-weight: 600;">🕒 LINE LOCKED: {created_at}</span>
</div>
</div>'''
    return html
"""
    with open("ui_components.py", "w", encoding="utf-8") as f:
        f.write(comp_content + clean_card_func)
    
    py_compile.compile("ui_components.py", doraise=True)
    print("   ✅ ui_components.py updated and verified.")

# --- 2. Sanitize Donna's t2 cards in app.py to prevent indentation fallback ---
if os.path.exists("app.py"):
    with open("app.py", "r", encoding="utf-8", errors="ignore") as f:
        app_code = f.read()
    
    # Ensure st.markdown in t2 strips line indentation before rendering
    if "st.markdown(card, unsafe_allow_html=True)" in app_code and "clean_card =" not in app_code:
        app_code = app_code.replace(
            "st.markdown(card, unsafe_allow_html=True)",
            "clean_card = '\\n'.join(line.strip() for line in card.splitlines())\n                    st.markdown(clean_card, unsafe_allow_html=True)"
        )
        with open("app.py", "w", encoding="utf-8") as f:
            f.write(app_code)
        py_compile.compile("app.py", doraise=True)
        print("   ✅ app.py (t2) sanitized against markdown code block triggers.")

print("=" * 65)
print("🟢 HOTFIX COMPLETE: HTML indentation cleared.")
print("=" * 65)
