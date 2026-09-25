with open("ui_components.py", "r", encoding="utf-8") as f:
    text = f.read()

patch = """
# --- MOBILE-FIRST UI COMPONENTS (ROADMAP #1-10 & #39-45) ---

def apply_mobile_css():
    import streamlit as st
    st.markdown('''
    <style>
        :root {
            --qb: #00f2fe; --rb: #2ed573; --wr: #ff4757; 
            --te: #ffa502; --flex: #a55eea; --dst: #70a1ff;
        }
        
        /* 1. Mobile-First Sticky Header (Roadmap #4) */
        .mobile-header {
            position: sticky;
            top: 0;
            z-index: 9999;
            background: rgba(18, 18, 18, 0.95);
            backdrop-filter: blur(10px);
            padding: 12px 16px;
            border-bottom: 2px solid var(--flex);
            color: white;
            font-family: sans-serif;
            font-weight: bold;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            border-radius: 0 0 8px 8px;
        }
        
        /* 2. Tap-Target Accessibility (Roadmap #7) */
        .stButton>button {
            min-height: 44px !important; 
            min-width: 44px !important;
            border-radius: 8px !important;
        }
        
        /* 3. Reusable Card Component (Roadmap #39-45) */
        .player-card {
            background: rgba(255, 255, 255, 0.05);
            border-left: 4px solid #555;
            border-radius: 6px;
            padding: 12px 16px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        /* Subtle left border accents instead of aggressive background floods */
        .pos-QB { border-left-color: var(--qb); }
        .pos-RB { border-left-color: var(--rb); }
        .pos-WR { border-left-color: var(--wr); }
        .pos-TE { border-left-color: var(--te); }
        .pos-FLEX { border-left-color: var(--flex); }
        .pos-DST { border-left-color: var(--dst); }
        
        /* 4. CSS Media Queries for Mobile Stacking (Roadmap #1, #3) */
        @media (max-width: 600px) {
            .player-card {
                flex-direction: column;
                align-items: flex-start;
                gap: 12px;
            }
            .card-stats {
                width: 100%;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-top: 1px solid rgba(255,255,255,0.1);
                padding-top: 10px;
            }
        }
    </style>
    ''', unsafe_allow_html=True)

def render_player_card(name, pos, proj, line=None, conf_tier="B"):
    import streamlit as st
    p_class = f"pos-{pos}" if pos in ['QB','RB','WR','TE','DST'] else "pos-FLEX"
    line_html = f"<div style='font-size: 13px; color: #aaa;'>Vegas Line: {line}</div>" if line else ""
    
    html = f'''
    <div class="player-card {p_class}">
        <div style="font-weight: 600; font-size: 16px;">
            <span style="opacity: 0.6; font-size: 12px; margin-right: 6px; font-family: monospace;">[{pos}]</span>{name}
        </div>
        <div class="card-stats">
            {line_html}
            <div style="display: flex; gap: 12px; align-items: center;">
                <div style="font-size: 11px; background: rgba(255,255,255,0.1); padding: 3px 8px; border-radius: 4px;">Tier {conf_tier}</div>
                <div style="font-weight: bold; font-size: 17px;">{proj} FP</div>
            </div>
        </div>
    </div>
    '''
    st.markdown(html, unsafe_allow_html=True)
"""

if "apply_mobile_css" not in text:
    with open("ui_components.py", "a", encoding="utf-8") as f:
        f.write("\n" + patch)
    print("✅ Successfully injected Mobile-First CSS and PlayerCard component into ui_components.py")
else:
    print("⚠️ Mobile UI patch already exists in ui_components.py.")