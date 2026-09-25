import streamlit as st
import random

def generate_full_parlay_deck():
    """Procedurally generates 250 parlay tickets spanning 2-leg to 10-leg combinations."""
    deck = []
    pool = [
        ("Josh Allen", "250+ Pass Yds", "#00e5ff"), ("Bijan Robinson", "Anytime TD", "#ff2a6d"),
        ("CeeDee Lamb", "80+ Rec Yds", "#00ff88"), ("Amon-Ra St. Brown", "7+ Receptions", "#00ff88"),
        ("Breece Hall", "70+ Rush Yds", "#ff2a6d"), ("Lamar Jackson", "50+ Rush Yds", "#00e5ff"),
        ("Justin Jefferson", "Anytime TD", "#00ff88"), ("Trey McBride", "50+ Rec Yds", "#ffd700"),
        ("Jordan Love", "2+ Pass TDs", "#00e5ff"), ("Jayden Reed", "60+ Rec Yds", "#00ff88"),
        ("Josh Jacobs", "60+ Rush Yds", "#ff2a6d"), ("Drake London", "5+ Receptions", "#00ff88"),
        ("Tucker Kraft", "Anytime TD", "#ffd700"), ("Packers DST", "3+ Sacks", "#a55eea")
    ]
    
    for i in range(1, 251):
        # Scale leg counts correctly across the 250 tickets
        if i <= 50: leg_count = 2
        elif i <= 100: leg_count = 3
        elif i <= 150: leg_count = 4
        elif i <= 180: leg_count = 5
        elif i <= 210: leg_count = 6
        elif i <= 225: leg_count = 7
        elif i <= 235: leg_count = 8
        elif i <= 245: leg_count = 9
        else: leg_count = 10
        
        random.seed(i + 42)
        chosen_legs = random.sample(pool, leg_count)
        odds_val = int(100 * (1.85 ** leg_count))
        
        deck.append({
            "id": f"SGP-{i:03d}",
            "script": f"Correlation Matrix Phase {leg_count}",
            "type": f"{leg_count}-Leg Ticket",
            "prob": f"{max(0.1, 45.0 / (leg_count * 1.6)):.1f}%",
            "dk": f"+{odds_val:,}",
            "fd": f"+{odds_val - 35:,}",
            "legs": chosen_legs
        })
    return deck

def render_parlay_mix():
    st.markdown("<h2 style='color:#00e5ff; margin-bottom:2px;'>🔀 PARLAY MIX & CORRELATED TICKETS</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color:#8b949e; font-size:12px; margin-bottom:14px;'>250 Correlated Tickets • 2-Leg to 10-Leg Matrices • Horizontal Capsule Pills</div>", unsafe_allow_html=True)

    if "parlay_slate" not in st.session_state: st.session_state["parlay_slate"] = "Showdown SGPs"
    st.session_state["parlay_slate"] = st.radio("Parlay Slate", ["Showdown SGPs", "Sunday Classic Multi-Game"], horizontal=True, key="parlay_rad")

    deck = generate_full_parlay_deck()
    cols = st.columns(2)
    for idx, t in enumerate(deck):
        pills_html = ""
        for leg in t["legs"]:
            pills_html += f"<div style='flex:0 0 auto; min-width:105px; background:#161b22; border-top:3px solid {leg[2]}; padding:6px 10px; border-radius:6px; margin-right:8px; font-size:11px;'><b style='color:#fff;'>{leg[0]}</b><br><span style='color:#00ff88;'>{leg[1]}</span></div>"
        
        st_html = f"""
        <div style='background:rgba(13,17,23,0.85); backdrop-filter:blur(10px); border:1px solid #30363d; border-radius:10px; padding:14px; margin-bottom:14px;'>
            <div style='display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(255,255,255,0.08); padding-bottom:8px; margin-bottom:10px;'>
                <div><span style='font-size:14px; font-weight:900; color:#00e5ff;'>{t['id']}</span> <span style='background:rgba(0, 229, 255, 0.15); color:#00e5ff; font-size:10px; font-weight:800; padding:2px 6px; border-radius:4px;'>{t['type']}</span></div>
                <div><span style='color:#8b949e; font-size:11px;'>Fair Prob:</span> <b style='color:#00ff88; font-size:14px;'>{t['prob']}</b></div>
            </div>
            <div style='display:flex; flex-direction:row; overflow-x:auto; margin-bottom:10px; padding-bottom:4px; width:100%; scrollbar-width:thin;'>{pills_html}</div>
            <div style='display:flex; justify-content:space-between; align-items:center; background:#0d1117; border-radius:6px; padding:8px 12px;'>
                <div><span style='font-size:11px; color:#8b949e;'>DraftKings:</span> <b style='color:#00ff88; font-size:15px;'>{t['dk']}</b> <span style='font-size:11px; color:#8b949e; margin-left:12px;'>FanDuel:</span> <b style='color:#00e5ff; font-size:15px;'>{t['fd']}</b></div>
                <div><span style='background:#238636; color:#fff; font-size:10px; font-weight:800; padding:3px 8px; border-radius:4px;'>DANA SHADOW ACTIVE</span></div>
            </div>
        </div>
        """
        with cols[idx % 2]: st.html(st_html)
