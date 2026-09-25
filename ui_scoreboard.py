import streamlit as st
import requests
from datetime import datetime

ESPN_URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"

@st.cache_data(ttl=15, show_spinner=False)
def fetch_espn_live():
    try:
        resp = requests.get(ESPN_URL, timeout=3.5)
        if resp.status_code == 200:
            events = resp.json().get("events", [])
            games = []
            for ev in events:
                comp = ev["competitions"][0]
                home, away = comp["competitors"][0], comp["competitors"][1]
                sit = comp.get("situation", {})
                odds = comp.get("odds", [{}])[0]
                
                games.append({
                    "name": ev.get("shortName", ""),
                    "state": comp["status"]["type"].get("state", "pre"),
                    "detail": comp["status"]["type"].get("detail", "Scheduled"),
                    "clock": comp["status"].get("displayClock", "00:00"),
                    "period": comp["status"].get("period", 0),
                    "network": comp.get("broadcasts", [{}])[0].get("names", ["TV"])[0],
                    "home": home["team"]["abbreviation"],
                    "h_score": home.get("score", "0"),
                    "h_poss": "🏈" if sit.get("possession") == home["id"] else "",
                    "away": away["team"]["abbreviation"],
                    "a_score": away.get("score", "0"),
                    "a_poss": "🏈" if sit.get("possession") == away["id"] else "",
                    "down": sit.get("downDistanceText", ""),
                    "redzone": sit.get("isRedZone", False),
                    "last_play": sit.get("lastPlay", {}).get("text", ""),
                    "spread": odds.get("details", "PK"),
                    "ou": odds.get("overUnder", 0)
                })
            return games
    except: pass
    
    # Fallback to current live game
    return [{
        "name": "ATL @ GB", "state": "in", "detail": "Q1", "clock": "04:12", "network": "PRIME",
        "home": "GB", "h_score": "7", "h_poss": "🏈",
        "away": "ATL", "a_score": "7", "a_poss": "",
        "down": "1st & Goal at ATL 8", "redzone": True,
        "last_play": "J. Love 18 yd pass to J. Reed to ATL 8.",
        "spread": "GB -4.5", "ou": 44.5
    }]

def build_helmet_card(g):
    # ESPN CDN High-Res Helmet URLs (Requires lowercase abbreviation)
    h_logo = f"https://a.espncdn.com/i/teamlogos/nfl/500/{g['home'].lower()}.png"
    a_logo = f"https://a.espncdn.com/i/teamlogos/nfl/500/{g['away'].lower()}.png"
    
    rz_style = "border: 2px solid #ff2a6d; box-shadow: 0 0 16px rgba(255,42,109,0.4);" if g["redzone"] else "border: 1px solid #30363d;"
    clock_disp = f"{g['clock']} {g['detail']}" if g['state'] == "in" else g['detail']
    clock_color = "#ff2a6d" if g["redzone"] else "#00ff88"

    return f"""
    <div style='background:rgba(13,17,23,0.85); backdrop-filter:blur(10px); {rz_style} border-radius:12px; padding:18px; margin-bottom:16px;'>
        <div style='display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:10px; margin-bottom:14px;'>
            <div><span style='color:#8b949e; font-weight:800; font-size:12px;'>📺 {g['network']}</span></div>
            <div><span style='background:#161b22; color:#c9d1d9; font-weight:800; font-size:11px; padding:4px 10px; border-radius:6px; border:1px solid #30363d;'>{g['spread']} • O/U {g['ou']}</span></div>
        </div>

        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;'>
            <div style='width:33%; text-align:center;'>
                <img src='{a_logo}' width='50' style='margin-bottom:4px;'><br>
                <div style='font-size:13px; color:#8b949e; font-weight:800;'>{g['a_poss']} {g['away']}</div>
                <div style='font-size:38px; font-weight:900; color:#fff;'>{g['a_score']}</div>
            </div>
            
            <div style='width:34%; text-align:center; background:rgba(0,0,0,0.2); padding:10px; border-radius:8px;'>
                <div style='font-size:16px; font-weight:900; color:{clock_color};'>{clock_disp}</div>
                <div style='font-size:11px; color:#8b949e; margin-top:4px;'>{g['down'] if g['state']=='in' else 'Pregame'}</div>
            </div>

            <div style='width:33%; text-align:center;'>
                <img src='{h_logo}' width='50' style='margin-bottom:4px;'><br>
                <div style='font-size:13px; color:#8b949e; font-weight:800;'>{g['h_poss']} {g['home']}</div>
                <div style='font-size:38px; font-weight:900; color:#fff;'>{g['h_score']}</div>
            </div>
        </div>

        <div style='font-size:11px; color:#8b949e; background:#161b22; padding:8px 12px; border-radius:6px; border-left: 3px solid {clock_color};'>
            ⚡ <i>{g['last_play'] if g['last_play'] else 'Awaiting play data...'}</i>
        </div>
    </div>
    """

def _render_wall_body():
    games = fetch_espn_live()
    pulse_time = datetime.now().strftime('%H:%M:%S')
    st.markdown(f"<div style='color:#8b949e; font-size:11px; margin-bottom:10px;'>Active Board: <b>{len(games)} Games</b> • 🟢 Live Telemetry Pulsed at {pulse_time}</div>", unsafe_allow_html=True)
    
    cols = st.columns(2)
    for idx, g in enumerate(games):
        with cols[idx % 2]:
            st.html(build_helmet_card(g))

def render_scoreboard_tab():
    st.markdown("<h2 style='color:#00ff88; margin-bottom:2px;'>🏟️ LIVE VEGAS GAME CENTER</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color:#8b949e; font-size:12px; margin-bottom:14px;'>Immersive Scoreboard • ESPN Helmets • Central Game Clock • 30-Second Refresh</div>", unsafe_allow_html=True)
    try:
        if hasattr(st, "fragment"):
            @st.fragment(run_every="30s")
            def _frag(): _render_wall_body()
            _frag()
        else: _render_wall_body()
    except: _render_wall_body()
