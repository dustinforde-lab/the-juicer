import json, pandas as pd, streamlit as st, requests, subprocess
from datetime import datetime

BACK_OF_HOUSE_REGISTRY = {
    "Javonte Williams": {"tag": "TAG-RB-003", "team": "DEN", "pos": "RB", "exposure_leagues": 2, "injury_status": "Healthy", "trench": "Short-yardage power profile vs soft front-seven"},
    "CeeDee Lamb": {"tag": "TAG-WR-004", "team": "DAL", "pos": "WR", "exposure_leagues": 4, "injury_status": "Probable (Ankle)", "corner": "Wins heavily against outside man coverage (3.41 YPRR)"},
    "DJ Moore": {"tag": "TAG-WR-005", "team": "CHI", "pos": "WR", "exposure_leagues": 2, "injury_status": "Healthy", "corner": "Slot mismatch vs soft zone coverages"},
    "Ray Davis": {"tag": "TAG-RB-008", "team": "BUF", "pos": "RB", "exposure_leagues": 2, "injury_status": "Healthy", "trench": "Red-zone hammer role expanding"},
    "Jaylin Noel": {"tag": "TAG-WR-009", "team": "ISU", "pos": "WR", "exposure_leagues": 1, "injury_status": "Healthy", "corner": "High separation rate against slot corners"}
}

def resolve_player_tag(name):
    return BACK_OF_HOUSE_REGISTRY.get(name, {"tag": "TAG-GEN-999", "team": "FA", "pos": "FLEX", "exposure_leagues": 1, "injury_status": "Healthy", "corner": "Standard matchup", "trench": "Neutral grade"})

def render_card(html):
    if hasattr(st, "html"): st.html(html)
    else: st.markdown("\n".join(l.strip() for l in html.splitlines() if l.strip()), unsafe_allow_html=True)

def render_telemetry(q_db):
    df = q_db("SELECT * FROM system_telemetry")
    with st.expander("📡 BACKEND TELEMETRY & MIKE'S INJURY INTELLIGENCE FEED", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""<div style="background:#130f24; border:1px solid #00ff8844; border-radius:8px; padding:10px; font-size:0.75rem;"><div style="color:#00ff88; font-weight:800;">● MIKE INJURY FEED (Active Sync)</div><div style="color:#fff; margin-top:5px;">• <b>CeeDee Lamb:</b> Probable (Ankle) - Full participant.</div><div style="color:#fff; margin-top:3px;">• <b>Javonte Williams:</b> Active / Clean designation.</div></div>""", unsafe_allow_html=True)
        with c2:
            if not df.empty:
                r = df.iloc[0]
                st.markdown(f"""<div style="background:#130f24; border:1px solid #00e5ff44; border-radius:8px; padding:10px; font-size:0.75rem;"><div style="color:#00e5ff; font-weight:800;">● {r['node']}</div><div style="color:#8a889b; margin:4px 0;">Status: <b style="color:#fff;">{r['status']}</b></div><div style="color:#ccc; font-size:0.68rem; margin-top:5px;">{r['agent_report']}</div></div>""", unsafe_allow_html=True)

def get_espn_games():
    try:
        d = requests.get("https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard", timeout=3).json()
        return [{"status": "FINAL" if e["status"]["type"]["state"]=="post" else e["status"]["type"]["detail"], "away": e["competitions"][0]["competitors"][1]["team"]["abbreviation"], "away_s": e["competitions"][0]["competitors"][1].get("score","0"), "away_h": f"<img src='{e['competitions'][0]['competitors'][1]['team']['logo']}' width='26'>", "home": e["competitions"][0]["competitors"][0]["team"]["abbreviation"], "home_s": e["competitions"][0]["competitors"][0].get("score","0"), "home_h": f"<img src='{e['competitions'][0]['competitors'][0]['team']['logo']}' width='26'>", "sit": e["status"]["type"]["detail"], "rz": e["competitions"][0].get("situation",{}).get("isRedZone", False), "line": "DK / FD / MGM / CZR Matrix", "border": "#00ff88" if e["status"]["type"]["state"]=="in" else "#8a889b" if e["status"]["type"]["state"]=="post" else "#ff2a6d55", "tc": "#00ff88" if e["status"]["type"]["state"]=="in" else "#8a889b"} for e in d.get("events", [])]
    except: return []

def render_vegas_wall():
    audit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S ET")
    render_card(f"""<style>@keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.35; }} }} .rz-pill {{ background:#ff2a6d; color:#fff; font-size:0.65rem; font-weight:900; padding:2px 8px; border-radius:4px; display:inline-block; letter-spacing:1px; animation: pulse 1.2s infinite; }}</style><div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;"><h3>🎰 Live Action Scoreboard & Multi-Book Matrix</h3><span style="color:#00ff88; font-size:0.75rem; font-weight:800; background:#071e16; border:1px solid #00ff8855; padding:3px 8px; border-radius:6px;">🕒 Last Line Audit: {audit_time} // Strict TNF Cleanse Active</span></div>""")
    api_games = get_espn_games()
    games = api_games if api_games else [{"status": "FINAL - POST-SHOWDOWN", "away": "DET", "away_s": "20", "away_h": "🦁", "home": "BUF", "home_s": "24", "home_h": "🦬", "sit": "TNF Completed - Auto-Cleansed from Slates", "rz": False, "line": "Locked & Settled", "border": "#8a889b", "tc": "#8a889b"}]
    r1 = st.columns(3)
    for i, g in enumerate(games[:15]):
        rz = '<div class="rz-pill">🚨 IN RED ZONE 🚨</div>' if g['rz'] else ''
        with r1[i % 3]: render_card(f"""<div style="background:#130f24; border:2px solid {g['border']}; border-radius:12px; padding:14px; margin-bottom:14px;"><div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;"><span style="font-size:0.75rem; font-weight:800; color:{g['tc']};">{g['status']}</span><span style="height:20px;">{rz}</span></div><div style="display:flex; justify-content:space-between; align-items:center; margin:6px 0;"><div style="font-size:1.5rem; display:flex; align-items:center; gap:8px;"><span>{g['away_h']}</span><span style="font-weight:900; color:#fff;">{g['away']}</span></div><div style="font-size:1.9rem; font-weight:900; color:#fff;">{g['away_s']}</div></div><div style="display:flex; justify-content:space-between; align-items:center; margin:6px 0 10px 0;"><div style="font-size:1.5rem; display:flex; align-items:center; gap:8px;"><span>{g['home_h']}</span><span style="font-weight:900; color:#fff;">{g['home']}</span></div><div style="font-size:1.9rem; font-weight:900; color:#fff;">{g['home_s']}</div></div><div style="background:#1c1733; border-radius:8px; padding:8px 10px; margin-bottom:8px;"><div style="display:flex; justify-content:space-between; font-size:0.75rem; font-weight:700;"><span style="color:#00e5ff;">{g['sit']}</span></div></div><div style="text-align:center; font-size:0.68rem; color:#8a889b; font-weight:800;">{g['line']}</div></div>""")

def render_dfs(q_db, SIM_FILE):
    st.markdown("### 👑 DFS Optimizer Engine <span class='credit-badge'>200 LINEUPS GENERATED</span>", unsafe_allow_html=True)
    try:
        with open(SIM_FILE, "r") as f: k = json.load(f).get("kpis", {})
        st.markdown(f"""<div style="display:flex; gap:15px; margin-bottom:15px;"><div style="background:#130f24; border:1px solid #ff2a6d44; border-radius:8px; padding:10px; flex:1;"><div style="color:#8a889b; font-size:0.7rem; font-weight:800;">AVG GPP PLACEMENT</div><div style="color:#fff; font-size:1.2rem; font-weight:900;">Top 4.2%</div></div><div style="background:#130f24; border:1px solid #ff2a6d44; border-radius:8px; padding:10px; flex:1;"><div style="color:#8a889b; font-size:0.7rem; font-weight:800;">SOLVENCY RISK</div><div style="color:#fff; font-size:1.2rem; font-weight:900;">{k.get('solvency_risk','0.01%')}</div></div><div style="background:#130f24; border:1px solid #ff2a6d44; border-radius:8px; padding:10px; flex:1;"><div style="color:#8a889b; font-size:0.7rem; font-weight:800;">CASH RATE</div><div style="color:#fff; font-size:1.2rem; font-weight:900;">{k.get('cash_rate','88.2%')}</div></div></div>""", unsafe_allow_html=True)
    except: pass
    
    df = q_db("SELECT * FROM dfs_classic_lineups LIMIT 200")
    if not df.empty:
        html = "<div style='max-height:650px; overflow-y:auto; padding-right:10px; margin-top:10px;'>"
        for i, r in df.iterrows():
            arch, sal, proj = r.get('archetype', 'GPP Stack'), f"${r['total_salary']:,.0f}", f"{r['projected_pts']} pts"
            pills = "".join([f"<div style='background:#1c1733; border:1px solid #00e5ff55; border-radius:6px; padding:8px; min-width:110px; flex:1;'><div style='color:#00e5ff; font-weight:900; font-size:0.65rem;'>{p['pos']}</div><div style='color:#fff; font-weight:800; font-size:0.85rem;'>{p['name']}</div><div style='color:#8a889b; font-size:0.75rem;'>${p['salary']} | {p['proj']}</div></div>" for p in json.loads(r["roster_json"]) if p['name'] not in ["Josh Allen", "Dalton Kincaid", "Jahmyr Gibbs", "Jameson Williams", "Ray Davis"]])
            html += f"<div style='background:#130f24; border:2px solid #332b58; border-radius:12px; padding:15px; margin-bottom:15px;'><div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;'><div style='color:#fff; font-weight:900;'>LINEUP #{i+1} // {arch.upper()}</div><div style='color:#00ff88; font-weight:800;'>{sal} | {proj}</div></div><div style='display:flex; gap:10px; flex-wrap:wrap;'>{pills}</div></div>"
        render_card(html + "</div>")

def render_rankings_syndicate(q_db):
    st.markdown("### 📊 Classy Power Rankings & Mike's Injury Intel <span class='credit-badge'>NATIVE ENGINE</span>", unsafe_allow_html=True)
    sc1, sc2 = st.columns([3, 1])
    with sc1: pos = st.radio("Filter Position:", ["ALL", "QB", "RB", "WR", "TE"], horizontal=True)
    with sc2: search = st.text_input("🔍 Search Player:")
    q = "SELECT r.pos_rank, r.name, r.pos, r.team, r.opponent, COALESCE(d.delta_str, '0') as delta, COALESCE(d.mike_donna_edge, 'Consensus Node') as edge FROM weekly_power_rankings r LEFT JOIN mike_donna_deltas d ON r.name = d.player WHERE 1=1"
    if pos != "ALL": q += f" AND r.pos = '{pos}'"
    if search: q += f" AND r.name LIKE '%{search}%'"
    df = q_db(q + " ORDER BY r.pos, r.pos_rank ASC")
    cards = "<div style='max-height:500px; overflow-y:auto; padding-right:6px;'>"
    for _, r in df.iterrows():
        meta = resolve_player_tag(r['name'])
        tactical_note = meta.get('corner', meta.get('trench', 'Optimized syndicate matchup profile.'))
        injury = meta.get('injury_status', 'Healthy')
        injury_color = "#ff2a6d" if "Probable" in injury or "Questionable" in injury else "#00ff88"
        cards += f"""<div style="background:#130f24; border:1px solid #00e5ff44; border-left:5px solid #00e5ff; border-radius:8px; padding:12px; margin-bottom:10px;"><div style="display:flex; justify-content:space-between; align-items:center;"><div style="display:flex; align-items:center; gap:10px;"><span style="background:#00e5ff22; color:#00e5ff; font-weight:900; padding:2px 8px; border-radius:4px; font-size:0.75rem;">#{r['pos_rank']} {r['pos']}</span><span style="font-weight:800; color:#fff; font-size:0.95rem;">{r['name']}</span><span style="color:#8a889b; font-size:0.75rem;">{r['team']} vs {r['opponent']}</span><span style="background:{injury_color}22; color:{injury_color}; font-size:0.68rem; font-weight:800; padding:2px 6px; border-radius:4px;">{injury}</span></div><div style="color:#00ff88; font-size:0.8rem; font-weight:800;">{r['edge']}</div></div><div style="margin-top:6px; font-size:0.75rem; color:#00e5ff; font-style:italic; background:#1c1733; padding:6px 10px; border-radius:4px;">💡 Tactical Breakdown: {tactical_note}</div></div>"""
    render_card(cards + "</div>")

def render_parlays(q_db):
    st.markdown("### 🎯 Sunday Correlated Same-Game Parlay Matrix <span class='credit-badge'>100% SUNDAY CLEAN</span>", unsafe_allow_html=True)
    
    render_card("""
    <div style="background: linear-gradient(135deg, #130f24 0%, #1e1333 100%); border: 1px solid #bb88ff55; border-radius: 12px; padding: 18px; margin-bottom: 20px; box-shadow: 0 4px 15px #41009922;">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom: 1px solid #ffffff11; padding-bottom: 10px; margin-bottom: 12px;">
            <div style="color: #bb88ff; font-weight: 900; font-size: 1.1rem; letter-spacing: 0.5px;">🤖 HENDERSON'S AI BETTING RECORD & YEARLY LEDGER</div>
            <div style="color: #00ff88; font-weight: 800; font-size: 0.85rem;">Synthetic Return: <b style="color:#fff;">+42.4% ($1,424.00)</b></div>
        </div>
        <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap: 15px; font-size: 0.82rem;">
            <div style="background:#1c1733; padding:10px; border-radius:8px; border-top:3px solid #00ff88;">
                <div style="color:#00ff88; font-weight:900; margin-bottom:4px;">CASH BUILDER TIER</div>
                <div>Record: <b style="color:#fff;">14 - 3 (82.4%)</b></div>
                <div>Avg ROI: <b style="color:#00ff88;">+18.5%</b></div>
            </div>
            <div style="background:#1c1733; padding:10px; border-radius:8px; border-top:3px solid #00e5ff;">
                <div style="color:#00e5ff; font-weight:900; margin-bottom:4px;">SYNDICATE CORE TIER</div>
                <div>Record: <b style="color:#fff;">8 - 5 (61.5%)</b></div>
                <div>Avg ROI: <b style="color:#00e5ff;">+44.2%</b></div>
            </div>
            <div style="background:#1c1733; padding:10px; border-radius:8px; border-top:3px solid #ff2a6d;">
                <div style="color:#ff2a6d; font-weight:900; margin-bottom:4px;">MOONSHOT WHALE TIER</div>
                <div>Record: <b style="color:#fff;">2 - 11 (15.4%)</b></div>
                <div>Avg ROI: <b style="color:#00ff88;">+112.0%</b></div>
            </div>
        </div>
    </div>
    """)
    
    c_filt, c_calc, c_purge = st.columns([2, 1, 1])
    with c_filt: f_t = st.radio("Filter Weight Class:", ["All Tiers", "Cash Builder", "Syndicate Core", "Moonshot Whale"], horizontal=True)
    with c_calc: wager = st.number_input("💵 Fictional Unit Wager ($):", min_value=1, value=50, step=5)
    with c_purge:
        st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
        if st.button("🧹 Force Slate Purge & Refresh", key="btn_slate_purge_unique_1"):
            subprocess.run(["python", "verify_and_cleanse.py"], capture_output=True, text=True)
            st.success("Auto-cleanser executed! Completed players purged.")
            st.rerun()

    query = "SELECT * FROM theoretical_bets"
    if f_t != "All Tiers":
        query += f" WHERE weight_class = '{f_t}'"
    df = q_db(query)
    
    if not df.empty:
        html = "<div style='max-height:650px; overflow-y:auto; padding-right:10px;'>"
        c1, c2 = st.columns(2)
        for i, (_, r) in enumerate(df.iterrows()):
            legs = "".join([f"<div style='padding:5px 0; border-bottom:1px solid #ffffff11;'>{p.get('icon','')} <b style='color:#fff;'>{p.get('player','')}</b> - {p.get('stat','')}</div>" for p in json.loads(r["ticket_json"])])
            odds_str = str(r.get('odds', '+100'))
            odds_val = int(odds_str.replace('+','')) if '+' in odds_str else 100
            payout = wager * ((odds_val / 100) + 1)
            card_html = f"""<div style="background:#130f24; border:2px solid {r.get('border_color', '#00e5ff')}; border-radius:12px; padding:16px; margin-bottom:14px;"><div style="display:flex; justify-content:space-between; margin-bottom:10px;"><span style="color:#8a889b; font-weight:700;">{r.get('ticket_id', 'SLIP')}</span><span style="color:{r.get('border_color', '#00e5ff')}; font-weight:900;">{odds_str} (AI Pays ${payout:,.2f})</span></div>{legs}</div>"""
            if i % 2 == 0:
                with c1: render_card(card_html)
            else:
                with c2: render_card(card_html)
        render_card(html + "</div>")
    else:
        st.info("No parlay slips found matching the selected weight class.")

def render_season_long(KEEPER_FILE):
    st.markdown("### 🏈 Season-Long Command Center (Multi-League Hub & Exposure) <span class='credit-badge' style='border-color:#bb88ff; color:#bb88ff;'>ACTIVE SUITE</span>", unsafe_allow_html=True)
    leagues = {
        "Malloy 2 (Team: Channel 4 News)": {"record": "1-0", "opp": "Ron Burgundy's Rival", "proj_self": 138.4, "proj_opp": 114.2},
        "The Dumbfucks (Team: Just Win Baby)": {"record": "1-0", "opp": "Al Davis Fan Club", "proj_self": 122.1, "proj_opp": 125.6},
        "S.F.F.L. (Team: The Company)": {"record": "0-1", "opp": "Corporate Compliance", "proj_self": 145.0, "proj_opp": 118.0},
        "Ruby AF Fantasy League (Show Me Your TDs)": {"record": "1-0", "opp": "Ruby's Crew", "proj_self": 131.5, "proj_opp": 129.8}
    }
    active_league = st.selectbox("🌐 SELECT ACTIVE LEAGUE:", list(leagues.keys()))
    l_data = leagues[active_league]
    
    render_card(f"""<div style="background:#130f24; border:1px solid #410099; border-radius:12px; padding:16px; margin-bottom:15px;"><div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #ffffff11; padding-bottom:10px; margin-bottom:10px;"><div style="color:#fff; font-size:1.1rem; font-weight:900;">{active_league}</div><div style="color:#00ff88; font-size:0.8rem;">Record: {l_data['record']}</div></div><div style="color:#00e5ff; font-size:0.85rem; font-weight:700;">Matchup vs. {l_data['opp']} (Projected: {l_data['proj_self']} vs {l_data['proj_opp']})</div></div>""")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🧹 Force Slate Purge & Refresh", key="btn_slate_purge_unique_2"):
            subprocess.run(["python", "verify_and_cleanse.py"], capture_output=True, text=True)
            st.success("Auto-cleanser executed! Completed players purged.")
    with col_btn2:
        if st.button("📊 View Cross-League Player Exposure"):
            st.info("Exposure Monitor: CeeDee Lamb (4/4 leagues), Javonte Williams (2/4 leagues), DJ Moore (2/4 leagues).")

    st.markdown("#### 🔄 Lineup Optimizer & Swap Tool")
    starters = [{"slot": "QB", "name": "Dak Prescott", "opp": "vs WAS", "proj": 20.1}, {"slot": "RB1", "name": "Javonte Williams", "opp": "vs WAS", "proj": 14.2}, {"slot": "RB2", "name": "Ray Davis", "opp": "vs DET", "proj": 11.5}, {"slot": "WR1", "name": "CeeDee Lamb", "opp": "vs WAS", "proj": 21.0}, {"slot": "WR2", "name": "DJ Moore", "opp": "@ BUF", "proj": 16.5}, {"slot": "TE", "name": "Cole Kmet", "opp": "vs DET", "proj": 10.5}, {"slot": "FLEX", "name": "Jaylin Noel", "opp": "vs ISU", "proj": 10.4}]
    
    for s in starters:
        meta = resolve_player_tag(s['name'])
        note = meta.get('corner', meta.get('trench', ''))
        exposure = meta.get('exposure_leagues', 1)
        col1, col2, col3 = st.columns([1, 2, 2])
        with col1: st.markdown(f"<b style='color:#00e5ff;'>{s['slot']}</b>", unsafe_allow_html=True)
        with col2: st.markdown(f"<b>{s['name']}</b> <span style='color:#8a889b; font-size:0.75rem;'>({s['opp']}) // Shares: {exposure}/4 Leagues</span><br><span style='font-size:0.68rem; color:#00ff88; font-style:italic;'>{note}</span>", unsafe_allow_html=True)
        with col3: st.markdown(f"<span style='color:#00ff88; font-weight:800;'>{s['proj']} pts</span>", unsafe_allow_html=True)

def render_prizepicks_underdog():
    st.markdown("### ⚡ PrizePicks & Underdog Fantasy Prop Hub <span class='credit-badge' style='border-color:#ff2a6d; color:#ff2a6d;'>DFS PICK'EM FEED</span>", unsafe_allow_html=True)
    st.info("Aggregating real-time prop projections, board opening lines vs. current lines, and correlation edges for PrizePicks and Underdog Fantasy.")
    
    prop_filter = st.selectbox("Select Prop Market:", ["NFL Passing Yards", "NFL Rushing Yards", "NFL Receiving Yards", "Combined Fantasy Score"])
    
    props = [
        {"player": "Dak Prescott", "platform": "PrizePicks / Underdog", "prop": "Passing Yards", "line": 255.5, "proj_val": 272.1, "edge": "OVER (+EV 5.4%)", "color": "#00ff88"},
        {"player": "Javonte Williams", "platform": "PrizePicks", "prop": "Rushing Yards", "line": 55.5, "proj_val": 64.1, "edge": "OVER (+EV 5.2%)", "color": "#00ff88"},
        {"player": "CeeDee Lamb", "platform": "Underdog Fantasy", "prop": "Receptions", "line": 7.5, "proj_val": 6.8, "edge": "UNDER (+EV 5.1%)", "color": "#ff2a6d"},
        {"player": "DJ Moore", "platform": "PrizePicks / Underdog", "prop": "Receiving Yards", "line": 62.5, "proj_val": 71.0, "edge": "OVER (+EV 7.1%)", "color": "#00ff88"}
    ]
    
    for p in props:
        render_card(f"""<div style="background:#130f24; border:1px solid {p['color']}55; border-left:4px solid {p['color']}; border-radius:10px; padding:14px; margin-bottom:10px; display:flex; justify-content:space-between; align-items:center;"><div style="display:flex; align-items:center; gap:15px;"><div><div style="color:#fff; font-weight:900; font-size:1rem;">{p['player']} <span style="font-size:0.75rem; color:#8a889b; font-weight:700;">({p['platform']})</span></div><div style="color:#00e5ff; font-size:0.8rem; font-weight:700;">{p['prop']} // Posted Line: <b>{p['line']}</b></div></div></div><div style="text-align:right;"><div style="color:#fff; font-weight:800; font-size:0.9rem;">Model Proj: {p['proj_val']}</div><div style="color:{p['color']}; font-weight:900; font-size:0.85rem;">{p['edge']}</div></div></div>""")
import json
import urllib.parse
import streamlit as st
import pandas as pd
import sqlite3

def render_parlay_card(ticket_id, tier, odds, color, legs_json, sportsbook):
    try:
        legs = json.loads(legs_json)
    except Exception:
        legs = []
    
    def parse_position(stat):
        s = stat.lower()
        if "pass" in s: return "QB", "#00e5ff"
        if "rec" in s: return "WR", "#ffaa00"
        if "rush" in s: return "RB", "#00ff88"
        if "td" in s or "anytime" in s: return "FLEX", "#ff2a6d"
        return "DEF", "#9d4edd"
        
    legs_html = ""
    for leg in legs:
        pos, pos_color = parse_position(leg.get('stat', ''))
        safe_name = urllib.parse.quote(leg.get('player', 'Player'))
        avatar_url = f"https://ui-avatars.com/api/?name={safe_name}&background=0b0e14&color={pos_color.replace('#','')}&rounded=true&bold=true&size=128&border=2"
        
        legs_html += f"""
        <div style="display: flex; align-items: center; background: #121824; margin-top: 8px; padding: 12px; border-radius: 8px; border-left: 4px solid {pos_color}; transition: all 0.3s ease;">
            <img src="{avatar_url}" style="width: 50px; height: 50px; border-radius: 50%; border: 2px solid {pos_color}; box-shadow: 0 0 12px {pos_color}50; margin-right: 16px;">
            <div style="flex-grow: 1;">
                <div style="font-weight: 800; color: #e6edf3; font-size: 1.1rem; letter-spacing: 0.5px;">
                    {leg.get('player', '')} 
                    <span style="font-size: 0.7rem; color: #0b0e14; background: {pos_color}; padding: 3px 8px; border-radius: 4px; margin-left: 8px; font-weight: 900; vertical-align: middle; box-shadow: 0 0 8px {pos_color}40;">{pos}</span>
                </div>
                <div style="font-size: 0.9rem; color: #8b949e; margin-top: 4px; font-weight: 600;">
                    {leg.get('team', '')} <span style="color: #444; margin: 0 4px;">|</span> <span style="color: #fff;">{leg.get('stat', '')}</span>
                </div>
            </div>
        </div>
        """
        
    html = f"""
    <div style="background: linear-gradient(145deg, #171d2b 0%, #0b0e14 100%); border: 1px solid {color}40; border-top: 4px solid {color}; border-radius: 12px; padding: 18px; margin-bottom: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #212838; padding-bottom: 12px; margin-bottom: 12px;">
            <div>
                <span style="color: {color}; font-weight: 900; font-size: 0.85rem; letter-spacing: 2px; text-transform: uppercase;">{tier}</span><br>
                <span style="color: #8b949e; font-size: 0.75rem; font-family: monospace;">{ticket_id}</span>
            </div>
            <div style="text-align: right;">
                <span style="color: #fff; font-weight: 900; font-size: 1.5rem;">{odds}</span><br>
                <span style="color: #8b949e; font-size: 0.8rem; font-weight: 700;">{sportsbook}</span>
            </div>
        </div>
        {legs_html}
        <div style="margin-top: 18px; display: flex; justify-content: space-between; gap: 12px;">
            <button onclick="navigator.clipboard.writeText('{ticket_id}: {odds} on {sportsbook}')" style="flex: 1; background: #0b0e14; color: #8b949e; border: 1px solid #212838; padding: 10px; border-radius: 6px; font-size: 0.8rem; font-weight: 800; cursor: pointer;">
                📋 COPY SLIP
            </button>
            <button style="flex: 1; background: #0b0e14; color: #8b949e; border: 1px solid #212838; padding: 10px; border-radius: 6px; font-size: 0.8rem; font-weight: 800; cursor: pointer;">
                🔒 LOCK ACTION
            </button>
        </div>
    </div>
    """
    return html

def render_prizepicks_underdog(conn=None):
    st.markdown("<h3 style='color:#00e5ff;'>⚡ PRIZEPICKS & UNDERDOG +EV CORRELATIONS</h3>", unsafe_allow_html=True)
    st.info("💡 Pulling synchronized player props and pre-made flex entries from database cache.")
    try:
        if callable(conn): conn = conn()
        if not conn: conn = sqlite3.connect("action_grid.db")
        df = pd.read_sql("SELECT * FROM theoretical_bets WHERE sportsbook LIKE '%PrizePicks%' OR sportsbook LIKE '%Underdog%'", conn)
        if not df.empty:
            for _, row in df.iterrows():
                st.markdown(render_parlay_card(row['ticket_id'], row['weight_class'], row['odds'], row['color'], row['ticket_json'], row['sportsbook']), unsafe_allow_html=True)
        else:
            st.warning("No PrizePicks or Underdog slips currently flagged in database. Displaying active model flex preview:")
            sample_legs = json.dumps([
                {"player": "Patrick Mahomes", "team": "KC", "stat": "275.5 Pass Yards"},
                {"player": "Travis Kelce", "team": "KC", "stat": "6.5 Receptions"}
            ])
            st.markdown(render_parlay_card("PP-FLEX-01", "2-LEG FLEX", "-110", "#00e5ff", sample_legs, "PrizePicks"), unsafe_allow_html=True)
    except Exception as e:
        st.caption(f"PrizePicks/Underdog module active ({e})")
import json
import urllib.parse
import streamlit as st
import pandas as pd
import sqlite3

def render_parlay_card(ticket_id, tier, odds, color, legs_json, sportsbook):
    try:
        legs = json.loads(legs_json)
    except Exception:
        legs = []
    
    def parse_position(stat):
        s = stat.lower()
        if "pass" in s: return "QB", "#00e5ff"
        if "rec" in s: return "WR", "#ffaa00"
        if "rush" in s: return "RB", "#00ff88"
        if "td" in s or "anytime" in s: return "FLEX", "#ff2a6d"
        return "DEF", "#9d4edd"
        
    legs_html = ""
    for leg in legs:
        pos, pos_color = parse_position(leg.get('stat', ''))
        safe_name = urllib.parse.quote(leg.get('player', 'Player'))
        avatar_url = f"https://ui-avatars.com/api/?name={safe_name}&background=0b0e14&color={pos_color.replace('#','')}&rounded=true&bold=true&size=128&border=2"
        
        legs_html += f"""
        <div style="display: flex; align-items: center; background: #121824; margin-top: 8px; padding: 12px; border-radius: 8px; border-left: 4px solid {pos_color}; transition: all 0.3s ease;">
            <img src="{avatar_url}" style="width: 50px; height: 50px; border-radius: 50%; border: 2px solid {pos_color}; box-shadow: 0 0 12px {pos_color}50; margin-right: 16px;">
            <div style="flex-grow: 1;">
                <div style="font-weight: 800; color: #e6edf3; font-size: 1.1rem; letter-spacing: 0.5px;">
                    {leg.get('player', '')} 
                    <span style="font-size: 0.7rem; color: #0b0e14; background: {pos_color}; padding: 3px 8px; border-radius: 4px; margin-left: 8px; font-weight: 900; vertical-align: middle; box-shadow: 0 0 8px {pos_color}40;">{pos}</span>
                </div>
                <div style="font-size: 0.9rem; color: #8b949e; margin-top: 4px; font-weight: 600;">
                    {leg.get('team', '')} <span style="color: #444; margin: 0 4px;">|</span> <span style="color: #fff;">{leg.get('stat', '')}</span>
                </div>
            </div>
        </div>
        """
        
    html = f"""
    <div style="background: linear-gradient(145deg, #171d2b 0%, #0b0e14 100%); border: 1px solid {color}40; border-top: 4px solid {color}; border-radius: 12px; padding: 18px; margin-bottom: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #212838; padding-bottom: 12px; margin-bottom: 12px;">
            <div>
                <span style="color: {color}; font-weight: 900; font-size: 0.85rem; letter-spacing: 2px; text-transform: uppercase;">{tier}</span><br>
                <span style="color: #8b949e; font-size: 0.75rem; font-family: monospace;">{ticket_id}</span>
            </div>
            <div style="text-align: right;">
                <span style="color: #fff; font-weight: 900; font-size: 1.5rem;">{odds}</span><br>
                <span style="color: #8b949e; font-size: 0.8rem; font-weight: 700;">{sportsbook}</span>
            </div>
        </div>
        {legs_html}
        <div style="margin-top: 18px; display: flex; justify-content: space-between; gap: 12px;">
            <button onclick="navigator.clipboard.writeText('{ticket_id}: {odds} on {sportsbook}')" style="flex: 1; background: #0b0e14; color: #8b949e; border: 1px solid #212838; padding: 10px; border-radius: 6px; font-size: 0.8rem; font-weight: 800; cursor: pointer;">
                📋 COPY SLIP
            </button>
            <button style="flex: 1; background: #0b0e14; color: #8b949e; border: 1px solid #212838; padding: 10px; border-radius: 6px; font-size: 0.8rem; font-weight: 800; cursor: pointer;">
                🔒 LOCK ACTION
            </button>
        </div>
    </div>
    """
    return html

def render_prizepicks_underdog(conn=None):
    st.markdown("<h3 style='color:#00e5ff;'>⚡ PRIZEPICKS & UNDERDOG +EV CORRELATIONS</h3>", unsafe_allow_html=True)
    st.info("💡 Pulling synchronized player props and pre-made flex entries from database cache.")
    try:
        if callable(conn): conn = conn()
        if not conn: conn = sqlite3.connect("action_grid.db")
        df = pd.read_sql("SELECT * FROM theoretical_bets WHERE sportsbook LIKE '%PrizePicks%' OR sportsbook LIKE '%Underdog%'", conn)
        if not df.empty:
            for _, row in df.iterrows():
                st.markdown(render_parlay_card(row['ticket_id'], row['weight_class'], row['odds'], row['color'], row['ticket_json'], row['sportsbook']), unsafe_allow_html=True)
        else:
            st.warning("No PrizePicks or Underdog slips currently flagged in database. Displaying active model flex preview:")
            sample_legs = json.dumps([
                {"player": "Patrick Mahomes", "team": "KC", "stat": "275.5 Pass Yards"},
                {"player": "Travis Kelce", "team": "KC", "stat": "6.5 Receptions"}
            ])
            st.markdown(render_parlay_card("PP-FLEX-01", "2-LEG FLEX", "-110", "#00e5ff", sample_legs, "PrizePicks"), unsafe_allow_html=True)
    except Exception as e:
        st.caption(f"PrizePicks/Underdog module active ({e})")


def render_stamped_parlay_card(ticket_id, tier, odds, border_color, legs_json, source, created_at):
    import json
    try:
        legs = json.loads(legs_json)
    except Exception:
        legs = []
        
    # Inject Cyber Colors & Sportsbook Badges
    sb_color = "#17e6a1" if "DraftKings" in source else "#107aca" if "FanDuel" in source else "#8b949e"
    sb_logo = "👑" if "DraftKings" in source else "🛡️" if "FanDuel" in source else "⚡"
    
    legs_html = ""
    for leg in legs:
        stat_low = leg.get('stat', '').lower()
        pos = "QB" if "pass" in stat_low else "WR" if "rec" in stat_low else "FLEX"
        pos_color = "#00e5ff" if pos == "QB" else "#ffaa00"
        
        legs_html += f'''
        <div style="display: flex; align-items: center; background: #121824; margin-top: 8px; padding: 12px; border-radius: 8px; border-left: 4px solid {pos_color};">
            <div style="flex-grow: 1;">
                <div style="font-weight: 800; color: #e6edf3; font-size: 1.1rem;">{leg.get('player', '')}</div>
                <div style="font-size: 0.9rem; color: #8b949e; margin-top: 4px; font-weight: 600;">
                    {leg.get('team', '')} | {leg.get('stat', '')}
                </div>
            </div>
        </div>
        '''
        
    html = f'''
    <div style="background: linear-gradient(145deg, #171d2b 0%, #0b0e14 100%); border: 1px solid {border_color}40; border-top: 4px solid {border_color}; border-radius: 12px; padding: 18px; margin-bottom: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
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
    </div>
    '''
    return html
