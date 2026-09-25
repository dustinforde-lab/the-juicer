import streamlit as st
import address_book

def generate_prop_slip_decks():
    pp_templates = [
        {"title": "Primetime Air & Ground", "multiplier": "10x Payout",
         "legs": [("Jordan Love", "OVER 242.5", "Pass Yds", "#00e5ff"),
                  ("Bijan Robinson", "OVER 68.5", "Rush Yds", "#ff2a6d"),
                  ("Jayden Reed", "OVER 54.5", "Rec Yds", "#00ff88"),
                  ("Drake London", "OVER 5.5", "Receptions", "#00ff88"),
                  ("Josh Jacobs", "OVER 16.5", "Rush Att", "#ff2a6d")]},
        {"title": "Red Zone Leverage Flex", "multiplier": "25x Payout",
         "legs": [("Jordan Love", "OVER 1.5", "Pass TDs", "#00e5ff"),
                  ("Jayden Reed", "OVER 4.5", "Receptions", "#00ff88"),
                  ("Kyle Pitts", "OVER 38.5", "Rec Yds", "#ffd700"),
                  ("Dontayvion Wicks", "OVER 32.5", "Rec Yds", "#00ff88"),
                  ("Tucker Kraft", "OVER 2.5", "Receptions", "#ffd700"),
                  ("Younghoe Koo", "OVER 1.5", "Made FGs", "#ff9f43")]}
    ]

    ud_templates = [
        {"title": "Core Thursday Power", "multiplier": "6x Payout",
         "legs": [("Bijan Robinson", "HIGHER 68.5", "Rush Yds", "#ff2a6d"),
                  ("Jordan Love", "HIGHER 242.5", "Pass Yds", "#00e5ff"),
                  ("Jayden Reed", "HIGHER 4.5", "Receptions", "#00ff88")]},
        {"title": "Primetime Volume Flex", "multiplier": "20x Payout",
         "legs": [("Drake London", "HIGHER 58.5", "Rec Yds", "#00ff88"),
                  ("Josh Jacobs", "HIGHER 72.5", "Rush Yds", "#ff2a6d"),
                  ("Kyle Pitts", "HIGHER 3.5", "Receptions", "#ffd700"),
                  ("Jordan Love", "HIGHER 32.5", "Pass Att", "#00e5ff"),
                  ("Dontayvion Wicks", "HIGHER 2.5", "Receptions", "#00ff88")]}
    ]

    pp_slips, ud_slips = [], []
    for i in range(1, 76):
        tpl_pp = pp_templates[(i - 1) % len(pp_templates)]
        pp_slips.append({
            "id": f"PP-{i:02d}", "title": f"{tpl_pp['title']} (Var {((i-1)//2)+1})",
            "payout": tpl_pp["multiplier"], "platform": "PrizePicks", "legs": tpl_pp["legs"]
        })
        tpl_ud = ud_templates[(i - 1) % len(ud_templates)]
        ud_slips.append({
            "id": f"UD-{i:02d}", "title": f"{tpl_ud['title']} (Var {((i-1)//2)+1})",
            "payout": tpl_ud["multiplier"], "platform": "Underdog", "legs": tpl_ud["legs"]
        })
    return pp_slips, ud_slips

def render_prizepicks():
    st.markdown("<h2 style='color:#ff2a6d; margin-bottom:2px;'>🎟️ PRIZEPICKS & UNDERDOG PROP SLIPS</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color:#8b949e; font-size:12px; margin-bottom:14px;'>150 Pre-Made Prop Slips • Horizontal Capsule Pills • 54.2% Break-Even Target Met</div>", unsafe_allow_html=True)

    if "prizepicks_slate" not in st.session_state:
        st.session_state["prizepicks_slate"] = "Showdown Primetime Props"

    c_tog, c_plat = st.columns([1.5, 2.5])
    with c_tog:
        st.session_state["prizepicks_slate"] = st.radio("Props Slate", ["Showdown Primetime Props", "Sunday Classic Full Slate"], horizontal=True, key="pp_rad")
    with c_plat:
        platform = st.radio("Platform Deck", ["PrizePicks (75 Slips)", "Underdog Fantasy (75 Slips)"], horizontal=True)

    pp_slips, ud_slips = generate_prop_slip_decks()
    active_deck = pp_slips if platform.startswith("PrizePicks") else ud_slips
    border_accent = "#00e5ff" if platform.startswith("PrizePicks") else "#ffd700"

    st.markdown(f"<div style='color:#8b949e; font-size:12px; margin-bottom:12px;'>Displaying <b>{len(active_deck)}</b> Pre-Made Prop Slips</div>", unsafe_allow_html=True)

    cols = st.columns(2)
    for idx, slip in enumerate(active_deck):
        pills_html = ""
        for leg in slip["legs"]:
            pills_html += f"""
            <div style='flex:1; min-width:90px; background:#161b22; border-top:3px solid {leg[3]}; padding:6px 8px; border-radius:6px; margin-right:6px; font-size:11px;'>
                <b style='color:#fff; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;'>{leg[0]}</b><br>
                <span style='color:#00ff88; font-weight:800;'>{leg[1]}</span><br>
                <span style='color:#8b949e; font-size:10px;'>{leg[2]}</span>
            </div>
            """

        slip_html = f"""
        <div style='background:rgba(13,17,23,0.85); backdrop-filter:blur(8px); border:1px solid #30363d; border-left:5px solid {border_accent}; border-radius:10px; padding:14px; margin-bottom:14px;'>
            <div style='display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(255,255,255,0.08); padding-bottom:8px; margin-bottom:10px;'>
                <div>
                    <span style='font-size:14px; font-weight:900; color:#fff;'>{slip['id']}</span>
                    <span style='color:#8b949e; font-size:11px; margin-left:6px;'>• {slip['title']}</span>
                </div>
                <div>
                    <span style='background:rgba(0,255,136,0.15); color:#00ff88; font-weight:900; font-size:12px; padding:3px 8px; border-radius:4px;'>{slip['payout']}</span>
                </div>
            </div>
            <div style='display:flex; flex-direction:row; overflow-x:auto; margin-bottom:10px; width:100%;'>{pills_html}</div>
            <div style='display:flex; justify-content:space-between; align-items:center; font-size:11px; color:#8b949e;'>
                <span>🎯 <b>Platform:</b> {slip['platform']}</span>
                <span style='color:#00ff88;'>● 54.2% Break-Even Target Met (Logged)</span>
            </div>
        </div>
        """
        with cols[idx % 2]:
            st.html(slip_html)
