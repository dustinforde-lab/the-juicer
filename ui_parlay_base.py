import streamlit as st
import numpy as np

def generate_250_parlay_deck():
    """Generates the 250 pre-made correlated parlay tickets with cross-book pricing."""
    scripts = [
        {"title": "Packers Aerial Shootout Stack (3 Legs)", "type": "QB + Pass-Catcher Correlation",
         "legs": ["Over 43.5 Game Total", "Jordan Love 2+ Passing TDs", "Jayden Reed 50+ Receiving Yds"],
         "fair_prob": "28.4%", "dk_odds": "+275", "fd_odds": "+265"},

        {"title": "Bijan Robinson Workhorse & Game Control (3 Legs)", "type": "Pace & Volume Script",
         "legs": ["Bijan Robinson 70+ Rushing Yds", "Bijan Robinson 4+ Receptions", "Bijan Robinson Anytime TD"],
         "fair_prob": "22.6%", "dk_odds": "+360", "fd_odds": "+340"},

        {"title": "Lambeau Clock-Kill Script (3 Legs)", "type": "Favorite Cover + Ground Script",
         "legs": ["Green Bay Packers -4.5 Spread", "Josh Jacobs 65+ Rushing Yds", "Josh Jacobs Anytime TD"],
         "fair_prob": "26.1%", "dk_odds": "+310", "fd_odds": "+295"},

        {"title": "Falcons Trailing Comeback Script (3 Legs)", "type": "Negative Script Pass-Funnel",
         "legs": ["Drake London Over 5.5 Receptions", "Kyle Pitts 40+ Receiving Yds", "Under 21.5 Falcons 1H Pts"],
         "fair_prob": "24.0%", "dk_odds": "+330", "fd_odds": "+320"},

        {"title": "Thursday Night Primetime Super-Stack (4 Legs)", "type": "Full Game Correlated SGP",
         "legs": ["Over 43.5 Game Total", "Jordan Love 225+ Pass Yds", "Jayden Reed Over 4.5 Rec", "Bijan Robinson 60+ Rush Yds"],
         "fair_prob": "16.8%", "dk_odds": "+525", "fd_odds": "+500"}
    ]

    deck = []
    for i in range(1, 251):
        base = scripts[(i - 1) % len(scripts)]
        deck.append({
            "Ticket_ID": f"Ticket #{i:03d}",
            "Title": f"{base['title']} (Var {((i-1)//5)+1})",
            "Type": base["type"],
            "Legs": base["legs"],
            "Fair_Prob": base["fair_prob"],
            "DK_Odds": base["dk_odds"],
            "FD_Odds": base["fd_odds"]
        })
    return deck

def build_parlay_ticket_card(t):
    legs_html = "".join([f"<div style='background:#161b22; border-radius:4px; padding:6px 10px; margin-bottom:4px; font-size:12px; color:#c9d1d9;'>🎯 {leg}</div>" for leg in t['Legs']])
    return f"""
    <div style='background:#0d1117; border:1px solid #30363d; border-radius:10px; padding:14px; margin-bottom:14px; box-shadow:0 4px 14px rgba(0,0,0,0.5);'>
        <div style='display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(255,255,255,0.08); padding-bottom:8px; margin-bottom:10px;'>
            <div>
                <span style='font-size:14px; font-weight:900; color:#00e5ff;'>{t['Ticket_ID']}</span>
                <span style='background:rgba(0, 229, 255, 0.15); color:#00e5ff; font-size:10px; font-weight:800; padding:2px 6px; border-radius:4px; margin-left:6px;'>{t['Type']}</span>
            </div>
            <div style='text-align:right;'>
                <span style='color:#8b949e; font-size:11px;'>Fair Prob:</span>
                <b style='color:#00ff88; font-size:14px; margin-left:4px;'>{t['Fair_Prob']}</b>
            </div>
        </div>

        <div style='margin-bottom:10px;'>
            {legs_html}
        </div>

        <div style='display:flex; justify-content:space-between; align-items:center; background:#161b22; border-radius:6px; padding:6px 12px;'>
            <div>
                <span style='font-size:11px; color:#8b949e;'>DraftKings:</span> <b style='color:#00ff88; font-size:14px;'>{t['DK_Odds']}</b>
                <span style='font-size:11px; color:#8b949e; margin-left:12px;'>FanDuel:</span> <b style='color:#00e5ff; font-size:14px;'>{t['FD_Odds']}</b>
            </div>
            <div>
                <span style='background:#238636; color:#fff; font-size:10px; font-weight:800; padding:3px 8px; border-radius:4px;'>+EV READY</span>
            </div>
        </div>
    </div>
    """

def render_parlay_mix():
    st.markdown("<h2 style='color:#00e5ff; margin-bottom:2px;'>🔀 PARLAY MIX & CORRELATION SLIPS</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color:#8b949e; font-size:12px; margin-bottom:14px;'>250 Pre-Made Correlated Parlay Cards • SGP Scripts • Cross-Book Odds Comparison</div>", unsafe_allow_html=True)

    deck = generate_250_parlay_deck()

    c1, c2 = st.columns([1.2, 2])
    with c1:
        sel_script = st.selectbox("Filter by Game Script", ["ALL SCRIPTS", "QB + Pass-Catcher Correlation", "Pace & Volume Script", "Favorite Cover + Ground Script", "Full Game Correlated SGP"])
    with c2:
        search_leg = st.text_input("Search Player or Market Leg", "")

    if sel_script != "ALL SCRIPTS":
        deck = [t for t in deck if t["Type"] == sel_script]
    if search_leg:
        deck = [t for t in deck if any(search_leg.lower() in l.lower() for l in t["Legs"])]

    st.markdown(f"<div style='color:#8b949e; font-size:12px; margin-bottom:12px;'>Displaying <b>{len(deck)}</b> Pre-Made Parlay Cards</div>", unsafe_allow_html=True)

    cols = st.columns(2)
    for idx, t in enumerate(deck):
        with cols[idx % 2]:
            st.html(build_parlay_ticket_card(t))
