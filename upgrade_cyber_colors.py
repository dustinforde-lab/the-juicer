import os

APP_FILE = "app.py"
UI_FILE = "ui_components.py"

NEON_CSS_INJECTION = """
# ==========================================================
# 🎨 NEON OVERDRIVE: MASTER COLOR CSS 
# ==========================================================
st.markdown('''
    <style>
        /* 1. Deep Space Background */
        .stApp {
            background: radial-gradient(circle at 50% 0%, #171d2b 0%, #0b0e14 70%) !important;
        }
        
        /* 2. Cyberpunk Sidebar */
        [data-testid="stSidebar"] {
            background-color: #07090e !important;
            border-right: 2px solid rgba(255, 42, 109, 0.3) !important;
            box-shadow: 5px 0 20px rgba(0, 0, 0, 0.8);
        }
        
        /* 3. The Big Execute Button (Glowing Gradient) */
        .stButton > button {
            background: linear-gradient(90deg, #ff2a6d 0%, #9d4edd 50%, #00e5ff 100%) !important;
            color: #ffffff !important;
            font-weight: 900 !important;
            font-size: 1.1rem !important;
            letter-spacing: 2px !important;
            border: none !important;
            box-shadow: 0 0 20px rgba(255, 42, 109, 0.4), 0 0 40px rgba(0, 229, 255, 0.2) !important;
            transition: all 0.3s ease !important;
            text-transform: uppercase;
        }
        .stButton > button:hover {
            box-shadow: 0 0 30px rgba(0, 255, 136, 0.6), 0 0 60px rgba(0, 229, 255, 0.4) !important;
            transform: scale(1.02) !important;
        }
        
        /* 4. Glowing Tabs */
        .stTabs [data-baseweb="tab-list"] {
            background-color: transparent;
        }
        .stTabs [data-baseweb="tab"] {
            color: #8b949e;
            font-weight: 800;
        }
        .stTabs [aria-selected="true"] {
            color: #00e5ff !important;
            text-shadow: 0 0 10px rgba(0, 229, 255, 0.6) !important;
        }
        
        /* 5. Headers & Dividers */
        hr { border-color: rgba(0, 229, 255, 0.2) !important; }
        h1, h2, h3 { text-shadow: 0 2px 10px rgba(0,0,0,0.5); }
    </style>
''', unsafe_allow_html=True)
"""

def inject_master_css():
    print("=" * 65)
    print("🎨 [COLOR UPGRADE] Injecting Neon Overdrive CSS...")
    print("=" * 65)
    
    with open(APP_FILE, "r", encoding="utf-8") as f:
        code = f.read()
        
    if "NEON OVERDRIVE: MASTER COLOR CSS" not in code:
        # Insert right after page config or at the top
        if "st.set_page_config" in code:
            code = code.replace('st.set_page_config(', 'st.set_page_config(') # Anchor
            parts = code.split('st.set_page_config')
            # Find end of the line
            end_of_line = parts[1].find('\n')
            new_code = parts[0] + 'st.set_page_config' + parts[1][:end_of_line] + '\n' + NEON_CSS_INJECTION + parts[1][end_of_line:]
            
            with open(APP_FILE, "w", encoding="utf-8") as f:
                f.write(new_code)
            print("   ✅ Master CSS injected into app.py!")
        else:
            with open(APP_FILE, "a", encoding="utf-8") as f:
                f.write("\n" + NEON_CSS_INJECTION)
            print("   ✅ Master CSS appended to app.py!")
    else:
        print("   ⚡ CSS already injected.")

def upgrade_card_glows():
    with open(UI_FILE, "r", encoding="utf-8") as f:
        ui_code = f.read()
    
    # Replace the dull box shadow with a dynamic glowing box shadow
    old_shadow = "box-shadow: 0 4px 14px rgba(0,0,0,0.35);"
    new_shadow = "box-shadow: 0 0 20px {color}40, inset 0 0 10px {color}15, 0 4px 15px rgba(0,0,0,0.8);"
    
    if old_shadow in ui_code:
        ui_code = ui_code.replace(old_shadow, new_shadow)
        with open(UI_FILE, "w", encoding="utf-8") as f:
            f.write(ui_code)
        print("   ✅ Parlay Cards upgraded with dynamic tier-colored glows!")
    else:
        print("   ⚡ Card glows already active.")

if __name__ == "__main__":
    inject_master_css()
    upgrade_card_glows()
