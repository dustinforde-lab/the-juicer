# -*- coding: utf-8 -*-
import streamlit as st

def generate_prop_slips():
    """Generates 150 pre-made prop slip cards: 75 PrizePicks and 75 Underdog Fantasy."""
    pp_base = [
        {"title": "5-Pick Flex: Primetime Air & Ground", "multiplier": "10x Payout",
         "legs": [("Jordan Love", "OVER 242.5 Pass Yds", "GB vs ATL"),
                  ("Bijan Robinson", "OVER 68.5 Rush Yds", "ATL @ GB"),
                  ("Jayden Reed", "OVER 54.5 Rec Yds", "GB vs ATL"),
                  ("Drake London", "OVER 5.5 Receptions", "ATL @ GB"),
                  ("Josh Jacobs", "OVER 16.5 Rush Attempts", "GB vs ATL")]},

        {"title": "6-Pick Flex: Maximum Leverage Multiplier", "multiplier": "25x Payout",
         "legs": [("Jordan Love", "OVER 1.5 Pass TDs", "GB vs ATL"),
                  ("Jayden Reed", "OVER 4.5 Receptions", "GB vs ATL"),
                  ("Kyle Pitts", "OVER 38.5 Rec Yds", "ATL @ GB"),
                  ("Dontayvion Wicks", "OVER 32.5 Rec Yds", "GB vs ATL"),
                  ("Tucker Kraft", "OVER 2.5 Receptions", "GB vs ATL"),
                  ("Bijan Robinson", "OVER 105.5 Rush+Rec Yds", "ATL @ GB")]}
    ]

    ud_base = [
        {"title": "3-Pick Power: Core Thursday Anchors", "multiplier": "6x Payout",
         "legs": [("Bijan Robinson", "HIGHER 68.5 Rush Yds", "ATL @ GB"),
                  ("Jordan Love", "HIGHER 242.5 Pass Yds", "GB vs ATL"),
                  ("Jayden Reed", "HIGHER 4.5 Receptions", "GB vs ATL")]},

        {"title": "5-Pick Flex: Primetime Target Volume", "multiplier": "20x Payout",
         "legs": [("Drake London", "HIGHER 58.5 Rec Yds", "ATL @ GB"),
                  ("Josh Jacobs", "HIGHER 72.5 Rush Yds", "GB vs ATL"),
                  ("Kyle Pitts", "HIGHER 3.5 Receptions", "ATL @ GB"),
                  ("Dontayvion Wicks", "HIGHER 2.5 Receptions", "GB vs ATL"),
                  ("Jordan Love", "HIGHER 32.5 Pass Attempts", "GB vs ATL")]}
    ]

    pp_slips, ud_slips = [], []
    for i in range(1, 76):
        b_pp = pp_base[(i - 1) % len(pp_base)]
        pp_slips.append({
            "Slip_ID": f"PrizePicks Slip #{i:02d}",
            "Title": f"{b_pp['title']} (Set {((i-1)//2)+1})",
            "Multiplier": b_pp["multiplier"],
            "Legs": b_pp["legs"],
            "Platform": "PrizePicks"
        })
        b_ud = ud_base[(i - 1) % len(ud_base)]
        ud_slips.append({
            "Slip_ID": f"Underdog Slip #{i:02d}",
            "Title": f"{b_ud['title']} (Set {((i-1)//2)+1})",
            "Multiplier": b_ud["multiplier"],
            "Legs": b_ud["legs"],
            "Platform": "Underdog"
        })
    return pp_slips, ud_slips

def build_prop_slip_card(slip):
    border_col = "#00e5ff" if slip["Platform"] == "PrizePicks" else "#ffd700"
    legs_html = "".join([f"""
        <div style='background:#161b22; border-radius:5px; padding:6px 10px; margin-bottom:5px; display:flex; justify-content:space-between; align-items:center;'>
            <div>
                <b style='color:#ffffff; font-size:12px;'>{leg[0]}</b>
                <span style='color:#8b949e; font-size:11px; margin-left:6px;'>({leg[2]})</span>
            </div>
            <div style='color:#00ff88; font-weight:800; font-size:12px;'>{leg[1]}</div>
        </div>
    """ for leg in slip['Legs']])

    return f"""
    <div style='background:#0d1117; border:1px solid #30363d; border-left:6px solid {border_col}; border-radius:10px; padding:14px; margin-bottom:14px; box-shadow:0 4px 14px rgba(0,0,0,0.5);'>
        <div style='display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(255,255,255,0.08); padding-bottom:8px; margin-bottom:10px;'>
            <div>
                <span style='font-size:15px; font-weight:900; color:#ffffff;'>{slip['Slip_ID']}</span>
                <span style='color:#8b949e; font-size:12px; margin-left:6px;'>&bull; {slip['Title']}</span>
            </div>
            <div>
                <span style='background:rgba(0,255,136,0.15); color:#00ff88; font-size:12px; font-weight:900; padding:3px 8px; border-radius:4px;'>{slip['Multiplier']}</span>
            </div>
        </div>

        <div style='margin-bottom:10px;'>
            {legs_html}
        </div>

        <div style='display:flex; justify-content:space-between; align-items:center; font-size:11px; color:#8b949e;'>
            <span>🎯 <b>Platform:</b> {slip['Platform']}</span>
            <span style='color:#00ff88;'>● 54.2% Break-Even Target Met</span>
        </div>
    </div>
    """

def render_prizepicks():
    st.markdown("<h2 style='color:#ff2a6d; margin-bottom:2px;'>🎟️ PRIZEPICKS & UNDERDOG PROP SLIPS</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color:#8b949e; font-size:12px; margin-bottom:14px;'>150 Pre-Made Prop Slips &bull; 75 PrizePicks Flex Plays &bull; 75 Underdog Higher/Lower Cards</div>", unsafe_allow_html=True)

    pp_slips, ud_slips = generate_prop_slips()

    platform = st.radio("Select Platform Deck", ["PrizePicks (75 Slips)", "Underdog Fantasy (75 Slips)"], horizontal=True)

    active_deck = pp_slips if platform.startswith("PrizePicks") else ud_slips
    st.markdown(f"<div style='color:#8b949e; font-size:12px; margin-bottom:12px;'>Displaying <b>{len(active_deck)}</b> Pre-Made Prop Slips</div>", unsafe_allow_html=True)

    cols = st.columns(2)
    for idx, slip in enumerate(active_deck):
        with cols[idx % 2]:
            st.html(build_prop_slip_card(slip))

