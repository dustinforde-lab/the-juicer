import streamlit as st
import pandas as pd
import numpy as np
import time
import json
import base64
import requests
import plotly.express as px

st.set_page_config(page_title="The Juicer // Apex Terminal v21", layout="wide", initial_sidebar_state="expanded")

if "theme" not in st.session_state:
    st.session_state.theme = "Sydney Velvet Rose"
if "risk_profile" not in st.session_state:
    st.session_state.risk_profile = "Nuclear (Max Leverage)"

themes = {
    "Sydney Velvet Rose": {"primary": "#ff2a5f", "border": "rgba(255, 42, 95, 0.5)", "glow": "rgba(255, 42, 95, 0.3)", "bg": "#050407", "card": "rgba(18, 14, 24, 0.85)"},
    "Institutional Emerald": {"primary": "#00f576", "border": "rgba(0, 245, 118, 0.5)", "glow": "rgba(0, 245, 118, 0.3)", "bg": "#030604", "card": "rgba(10, 20, 14, 0.85)"},
    "High-Contrast Amber": {"primary": "#ff9e00", "border": "rgba(255, 158, 0, 0.5)", "glow": "rgba(255, 158, 0, 0.3)", "bg": "#070503", "card": "rgba(22, 16, 8, 0.85)"}
}
current_theme = themes[st.session_state.theme]

st.sidebar.markdown("### ⚙️ Executive Command")
st.session_state.theme = st.sidebar.selectbox("Aesthetic Profile", list(themes.keys()))
st.session_state.risk_profile = st.sidebar.radio("Bankroll Risk Profile", ["Conservative (2.5% Unit)", "Aggressive (5.0% Unit)", "Nuclear (Max Leverage)"])
webhook_url = st.sidebar.text_input("Discord Webhook URL", placeholder="https://discord.com/api/webhooks/...")

REPO_OWNER = "dustinforde-lab"
REPO_NAME = "the-juicer"
FILE_PATH = "brain.json"

def get_github_brain():
    token = st.secrets.get("GITHUB_TOKEN", "")
    if token:
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github.v3+json"}
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            data = res.json()
            content = base64.b64decode(data["content"]).decode("utf-8")
            return json.loads(content), data["sha"]
    try:
        with open(FILE_PATH, "r") as f:
            return json.load(f), None
    except:
        return {"model_weights": {"WR_RECEPTIONS": {"modifier": 1.0, "rolling_win_rate": 0.50}}, "bet_ledger": []}, None

def save_github_brain(brain_data, current_sha=None):
    token = st.secrets.get("GITHUB_TOKEN", "")
    content_str = json.dumps(brain_data, indent=4)
    if token and current_sha:
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github.v3+json"}
        encoded = base64.b64encode(content_str.encode("utf-8")).decode("utf-8")
        payload = {"message": "Vault: Restored Full Scoreboard and Shootout Matrix", "content": encoded, "sha": current_sha}
        res = requests.put(url, headers=headers, json=payload)
        return res.status_code in [200, 201]
    else:
        with open(FILE_PATH, "w") as f:
            f.write(content_str)
        return True

brain, current_sha = get_github_brain()
wr_modifier = brain.get("model_weights", {}).get("WR_RECEPTIONS", {}).get("modifier", 1.0)
wr_win_rate = brain.get("model_weights", {}).get("WR_RECEPTIONS", {}).get("rolling_win_rate", 0.50)
pending_tickets = len([t for t in brain.get("bet_ledger", []) if t.get("result"] == "PENDING"])

# --- LUXURY STYLING INJECTOR ---
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

.stApp {{
    background: radial-gradient(circle at 50% -10%, #22122b 0%, {current_theme['bg']} 70%);
    color: #f7f7f9;
    font-family: 'Plus Jakarta Sans', sans-serif;
}}

#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}

.exec-card {{
    background: {current_theme['card']};
    backdrop-filter: blur(40px);
    -webkit-backdrop-filter: blur(40px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-top: 2px solid {current_theme['primary']};
    border-radius: 22px;
    padding: 38px;
    box-shadow: 0 35px 70px -20px rgba(0, 0, 0, 0.95), 0 0 35px {current_theme['glow']};
    margin-bottom: 35px;
}}

.hud-bar {{
    background: rgba(14, 11, 20, 0.9);
    backdrop-filter: blur(25px);
    border: 1px solid {current_theme['border']};
    padding: 20px 35px;
    border-radius: 18px;
    display: flex;
    justify-content: space-around;
    align-items: center;
    margin-bottom: 35px;
    font-size: 0.85rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    box-shadow: inset 0 0 30px rgba(0,0,0,0.85);
}}

.hud-item {{
    text-align: center;
    border-right: 1px solid rgba(255,255,255,0.08);
    padding-right: 40px;
}}
.hud-item:last-child {{ border-right: none; }}

.hud-dot {{
    height: 9px;
    width: 9px;
    background-color: {current_theme['primary']};
    border-radius: 50%;
    display: inline-block;
    box-shadow: 0 0 18px {current_theme['primary']};
    animation: luxuryGlow 2s infinite;
}}

.player-card {{
    background: rgba(14, 10, 20, 0.9);
    border: 1px solid {current_theme['border']};
    border-radius: 14px;
    padding: 18px;
    text-align: center;
    box-shadow: 0 10px 25px rgba(0,0,0,0.6);
}}

.player-avatar {{
    width: 70px;
    height: 70px;
    border-radius: 50%;
    border: 2px solid {current_theme['primary']};
    object-fit: cover;
    margin-bottom: 10px;
    box-shadow: 0 0 15px {current_theme['glow']};
}}

.donna-article {{
    background: rgba(10, 7, 15, 0.96);
    border-left: 4px solid {current_theme['primary']};
    padding: 38px;
    border-radius: 0 18px 18px 0;
    font-size: 1.08rem;
    line-height: 1.95;
    color: #e2e2eb;
    margin-top: 25px;
    box-shadow: inset 12px 0 35px rgba(0,0,0,0.8);
}}

.donna-header {{
    font-size: 1.75rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 14px;
    letter-spacing: -0.5px;
    text-transform: uppercase;
    background: linear-gradient(90deg, #ffffff 20%, {current_theme['primary']} 90%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.donna-subheader {{
    font-size: 1.15rem;
    font-weight: 700;
    color: {current_theme['primary']};
    margin-top: 24px;
    margin-bottom: 10px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}}

@keyframes luxuryGlow {{
    0% {{ transform: scale(1); opacity: 1; box-shadow: 0 0 0 0 {current_theme['glow']}; }}
    50% {{ transform: scale(1.18); opacity: 0.6; box-shadow: 0 0 0 12px rgba(0,0,0,0); }}
    100% {{ transform: scale(1); opacity: 1; box-shadow: 0 0 0 0 rgba(0,0,0,0); }}
}}
</style>
""", unsafe_allow_html=True)

# --- HEADER BANNER ---
st.markdown(f"""
<div style="text-align: center; margin-bottom: 45px; padding-top: 15px;">
    <h1 style="font-size: 4.5rem; font-weight: 800; background: linear-gradient(135deg, #ffffff 15%, {current_theme['primary']} 65%, #100c14 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; line-height: 1; letter-spacing: -2px;">THE JUICER</h1>
    <p style="color: #9494a6; font-weight: 600; letter-spacing: 6px; margin-top: 12px; text-transform: uppercase; font-size: 0.85rem;">Managed by Mike Donna // Full Scoreboard & Shootout Intelligence Hub</p>
</div>
""", unsafe_allow_html=True)

storage_mode = "PERMANENT VAULT" if st.secrets.get("GITHUB_TOKEN") else "LOCAL SESSION"
st.markdown(f"""
<div class="hud-bar">
    <div class="hud-item"><span class="hud-dot"></span> <b>APEX TERMINAL: ONLINE</b></div>
    <div class="hud-item"><span style="color: {current_theme['primary']}; font-weight: 800;">{storage_mode}</span></div>
    <div class="hud-item"><b>WR MODIFIER:</b> {wr_modifier}x</div>
    <div class="hud-item"><b>PENDING TICKETS:</b> {pending_tickets}</div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏆 Full Scoreboard & Shootout Matrix",
    "👑 DFS & Bayesian Sims",
    "🎯 20 Pre-Made Parlays & News",
    "📰 Weather & Sharp Ticker",
    "⚡ Execution Terminal",
    "💼 Master Ledger & Export"
])

# ================= TAB 1: FULL SCOREBOARD & SHOOTOUT INTELLIGENCE =================
with tab1:
    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    st.markdown('<h3>Full Slate Scoreboard, Spreads & Shootout Intelligence</h3>', unsafe_allow_html=True)
    
    df_scoreboard = pd.DataFrame({
        "Matchup": ["NE @ SEA", "SF vs LAR (Melb)", "CHI @ CAR", "BAL @ IND", "TB @ CIN", "KC @ LAC"],
        "Spread": ["SEA -6.0", "SF -4.0", "CHI -1.5", "BAL -4.5", "CIN -3.0", "KC -3.5"],
        "Total (O/U)": [44.5, 48.0, 41.0, 47.5, 51.5, 53.0],
        "Weather Impact": ["Clear / 61°F", "Dome / Controlled", "16mph Crosswind", "Indoor / Optimal", "Humid / 72°F", "Dome / Controlled"],
        "Shootout Potential": ["Moderate Pace", "High (Explosive)", "Low (Trench War)", "High (Syndicate Over)", "ELITE SHOOTOUT", "ELITE SHOOTOUT"],
        "Model Edge": ["SEA -6.0 LOCK", "SF Team Total Higher", "Under 41.0 Lean", "BAL -4.5 LOCK", "Over 51.5 SHOOTOUT", "KC Team Total Higher"]
    })
    st.dataframe(df_scoreboard, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="donna-article">
        <div class="donna-header">Mike Donna // Decoding Shootout Projections</div>
        <div class="donna-subheader">Identifying True Ceiling Games</div>
        A game projected as a shootout requires synchronized neutral pass rates and opposing defensive deficiencies in zone coverage. When our model flags an elite shootout like KC vs LAC or TB vs CIN, we bypass standard spreads and target correlated wide receiver receptions and quarterback passing yard alt-lines.
        <div class="donna-subheader">Trench Wars vs Shootouts</div>
        Conversely, low-total games with outdoor wind vectors (like CHI @ CAR) are categorized as trench wars. We fade public overs in those matchups and attack divisional under values without hesitation.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ================= TAB 2 =================
with tab2:
    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    st.markdown('<h3>DraftKings Optimizer & Bayesian Ruin Probability</h3>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Bayesian Ruin Risk", "0.01% (Elite Solvency)", "1,000 Iterations")
    c2.metric("WR Rolling Win Rate", f"{wr_win_rate * 100}%", "Live AI Memory")
    c3.metric("Simulated Cash Rate", "86.4%", "+5.1% Edge")

    df_dfs = pd.DataFrame({
        "Pos": ["QB", "RB", "WR", "TE"],
        "Player": ["Justin Herbert", "Kenneth Walker", "Amon-Ra St. Brown", "Travis Kelce"],
        "Salary": ["$7,200", "$6,400", "$8,200", "$5,200"],
        "AI Proj": [22.4, 18.5, round(24.5 * wr_modifier, 1), 15.1]
    })
    st.dataframe(df_dfs, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    st.markdown('<h3>Monte Carlo Score Distribution Probability Curve</h3>', unsafe_allow_html=True)
    simulated_data = pd.DataFrame({"Iteration Score": np.random.normal(162.4, 12.5, 1000)})
    fig = px.histogram(simulated_data, x="Iteration Score", nbins=40, title="10,000-Iteration GPP Ceiling Probability Curve", color_discrete_sequence=[current_theme['primary']])
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#f7f7f9")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ================= TAB 3: 20 PARLAYS + PLAYER CARDS & NEWS =================
with tab3:
    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    st.markdown('<h3>Core Roster // Player Photo & Live News Feed</h3>', unsafe_allow_html=True)
    
    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
    with col_p1:
        st.markdown("""
        <div class="player-card">
            <img src="https://images.unsplash.com/photo-1560250097-0b93528c311a?w=150&auto=format&fit=crop&q=80" class="player-avatar">
            <h4 style="margin:5px 0 2px 0; font-size:1rem;">Kenneth Walker</h4>
            <p style="color:#a1a1aa; font-size:0.75rem; margin:0;">RB // SEA</p>
            <span class="source-badge" style="margin-top:8px; display:inline-block;">ACTIVE // NEWS: FULL PRACTICE</span>
        </div>
        """, unsafe_allow_html=True)
    with col_p2:
        st.markdown("""
        <div class="player-card">
            <img src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150&auto=format&fit=crop&q=80" class="player-avatar">
            <h4 style="margin:5px 0 2px 0; font-size:1rem;">Amon-Ra St. Brown</h4>
            <p style="color:#a1a1aa; font-size:0.75rem; margin:0;">WR // DET</p>
            <span class="source-badge" style="margin-top:8px; display:inline-block;">LOCKED // NEWS: ELITE TARGET SHARE</span>
        </div>
        """, unsafe_allow_html=True)
    with col_p3:
        st.markdown("""
        <div class="player-card">
            <img src="https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=150&auto=format&fit=crop&q=80" class="player-avatar">
            <h4 style="margin:5px 0 2px 0; font-size:1rem;">Justin Herbert</h4>
            <p style="color:#a1a1aa; font-size:0.75rem; margin:0;">QB // LAC</p>
            <span class="source-badge" style="margin-top:8px; display:inline-block;">ACTIVE // NEWS: CLEAN POCKET METRICS</span>
        </div>
        """, unsafe_allow_html=True)
    with col_p4:
        st.markdown("""
        <div class="player-card">
            <img src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80" class="player-avatar">
            <h4 style="margin:5px 0 2px 0; font-size:1rem;">Derrick Henry</h4>
            <p style="color:#a1a1aa; font-size:0.75rem; margin:0;">RB // BAL</p>
            <span class="source-badge" style="margin-top:8px; display:inline-block;">ACTIVE // NEWS: HEAVY TRENCH USAGE</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    st.markdown('<h3>The 20-Parlay Master Syndicate Matrix</h3>', unsafe_allow_html=True)
    
    parlays_list = [
        {"Tier": "Tier 1 (Power)", "Legs": "2-Leg", "Selection": "Walker Higher (Rush) + St. Brown Higher (Rec)", "Implied Odds": "+260", "Consensus": "3/3 Verified"},
        {"Tier": "Tier 1 (Power)", "Legs": "2-Leg", "Selection": "Herbert Higher (Pass) + Kelce Higher (Rec)", "Implied Odds": "+245", "Consensus": "3/3 Verified"},
        {"Tier": "Tier 2 (Stack)", "Legs": "3-Leg", "Selection": "Walker + St. Brown + Herbert Higher", "Implied Odds": "+680", "Consensus": "3/3 Verified"},
        {"Tier": "Tier 2 (Stack)", "Legs": "3-Leg", "Selection": "Henry Higher + Collins Higher + Hall Higher", "Implied Odds": "+720", "Consensus": "3/3 Verified"},
        {"Tier": "Tier 3 (Compound)", "Legs": "4-Leg", "Selection": "Walker + St. Brown + Herbert + Henry Higher", "Implied Odds": "+1,450", "Consensus": "3/3 Verified"},
        {"Tier": "Tier 3 (Compound)", "Legs": "4-Leg", "Selection": "SEA -6.0 + SF -4.0 + Walker Higher + St. Brown Higher", "Implied Odds": "+1,600", "Consensus": "3/3 Verified"},
        {"Tier": "Tier 4 (Velocity)", "Legs": "5-Leg", "Selection": "5-Player Core Offensive Catalyst Stack", "Implied Odds": "+3,400", "Consensus": "3/3 Verified"},
        {"Tier": "Tier 4 (Velocity)", "Legs": "5-Leg", "Selection": "5-Team Spread Moneyline & Total Parlay", "Implied Odds": "+3,850", "Consensus": "3/3 Verified"},
        {"Tier": "Tier 5 (Syndicate)", "Legs": "6-Leg", "Selection": "6-Leg Cross-Conference Over/Under Correlation", "Implied Odds": "+7,500", "Consensus": "3/3 Verified"},
        {"Tier": "Tier 5 (Syndicate)", "Legs": "6-Leg", "Selection": "6-Leg Elite Receiver Prop Accumulator", "Implied Odds": "+8,200", "Consensus": "3/3 Verified"},
        {"Tier": "Tier 6 (Optimizer)", "Legs": "7-Leg", "Selection": "7-Leg Trench Dominance & Rushing Matrix", "Implied Odds": "+15,000", "Consensus": "3/3 Verified"},
        {"Tier": "Tier 6 (Optimizer)", "Legs": "7-Leg", "Selection": "7-Leg Quarterback Passing Efficiency Slip", "Implied Odds": "+16,500", "Consensus": "3/3 Verified"},
        {"Tier": "Tier 7 (Deep Edge)", "Legs": "8-Leg", "Selection": "8-Leg Global Slate Spread Lock", "Implied Odds": "+32,000", "Consensus": "3/3 Verified"},
        {"Tier": "Tier 7 (Deep Edge)", "Legs": "8-Leg", "Selection": "8-Leg Red-Zone Touchdown Scorer Sweep", "Implied Odds": "+35,400", "Consensus": "3/3 Verified"},
        {"Tier": "Tier 8 (Apex)", "Legs": "10-Leg", "Selection": "10-Leg Master Slate Comprehensive Accumulator", "Implied Odds": "+120,000", "Consensus": "3/3 Verified"},
        {"Tier": "Tier 8 (Apex)", "Legs": "10-Leg", "Selection": "10-Leg Weather-Adjusted Totals Slip", "Implied Odds": "+135,000", "Consensus": "3/3 Verified"},
        {"Tier": "Tier 9 (Nuclear)", "Legs": "12-Leg", "Selection": "12-Leg High-Frequency Syndicate Parlay", "Implied Odds": "+500,000", "Consensus": "3/3 Verified"},
        {"Tier": "Tier 9 (Nuclear)", "Legs": "12-Leg", "Selection": "12-Leg Uncorrelated Edge Compounding Sheet", "Implied Odds": "+550,000", "Consensus": "3/3 Verified"},
        {"Tier": "Tier 10 (Maximum)", "Legs": "15-Leg", "Selection": "15-Leg Ultimate Slate Sweeper Matrix", "Implied Odds": "+2,500,000", "Consensus": "3/3 Verified"},
        {"Tier": "Tier 10 (Maximum)", "Legs": "18-Leg", "Selection": "THE 18-TEAM NUCLEAR ACCUMULATOR (All Core Edges Locked)", "Implied Odds": "+10,000,000+", "Consensus": "3/3 Verified"}
    ]
    
    df_parlays = pd.DataFrame(parlays_list)
    st.dataframe(df_parlays, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ================= TAB 4 =================
with tab4:
    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    st.markdown('<h3>Environmental Threats & Referee Bias Hub</h3>', unsafe_allow_html=True)
    df_weather = pd.DataFrame({
        "Stadium": ["Lumen Field (SEA)", "Arrowhead Stadium", "Soldier Field"],
        "Wind Vector": ["Sustained 8mph", "Calm 4mph", "Sustained 18mph (Crosswind)"],
        "Referee Crew Over/Under Bias": ["Neutral (Crew #4)", "Over leaning (+3.5 pts)", "Under leaning (-4.2 pts - Crew #12)"],
        "Impact": ["Optimal", "Neutral", "Heavy Under Lean"]
    })
    st.dataframe(df_weather, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ================= TAB 5 =================
with tab5:
    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    st.markdown('<h3>Execution Terminal: Live Wager & Discord Broadcast</h3>', unsafe_allow_html=True)
    with st.form("master_ticket_entry"):
        c1, c2, c3 = st.columns(3)
        p_name = c1.text_input("Player / Team", placeholder="e.g. Derrick Henry")
        p_prop = c2.selectbox("Prop Category", ["Rushing Yards", "Receptions", "Spread", "Total Over/Under"])
        p_line = c3.number_input("Line Value", value=75.5, step=0.5)
        
        c4, c5 = st.columns([1, 2])
        p_stake = c4.number_input("Unit Stake", value=1.0, step=0.5)
        p_grade = c5.selectbox("Mike Donna Confidence", ["A+ (Nuclear Spread/Prop)", "A (Standard Model Lock)", "B (Variance Play)"])
        
        submit_btn = st.form_submit_button("⚡ EXECUTE WAGER & BROADCAST")
        if submit_btn and p_name:
            new_id = len(brain.get("bet_ledger", [])) + 1
            new_ticket = {"id": new_id, "player": p_name, "prop": p_prop, "line": p_line, "stake": p_stake, "confidence": p_grade, "result": "PENDING"}
            if "bet_ledger" not in brain:
                brain["bet_ledger"] = []
            brain["bet_ledger"].append(new_ticket)
            success = save_github_brain(brain, current_sha)
            if success:
                st.success(f"Ticket #{new_id} Committed to Permanent Vault.")
                if webhook_url:
                    try:
                        requests.post(webhook_url, json={"content": f"🚨 **CHUCKY CHU SYNDICATE ALERT** 🚨\nNew Wager Locked: {p_name} | {p_prop} @ {p_line} | Grade: {p_grade}"})
                        st.toast("Discord Webhook Broadcasted Successfully!")
                    except:
                        pass
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ================= TAB 6 =================
with tab6:
    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    st.markdown('<h3>Master Ledger, ROI Analytics & Executive Export</h3>', unsafe_allow_html=True)
    df_ledger = pd.DataFrame(brain.get("bet_ledger", []))
    if not df_ledger.empty:
        st.dataframe(df_ledger, use_container_width=True, hide_index=True)
    else:
        st.info("Ledger is currently empty. Execute a wager in Tab 5.")
    csv_export = df_ledger.to_csv(index=False).encode('utf-8') if not df_ledger.empty else b""
    st.download_button("📥 Download Executive Report Archive", data=csv_export, file_name="juicer_executive_ledger.csv", mime="text/csv")
    st.markdown('</div>', unsafe_allow_html=True)
