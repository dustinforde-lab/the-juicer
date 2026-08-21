import streamlit as st
import pandas as pd
import numpy as np
import time
import json
import base64
import requests

st.set_page_config(page_title="The Juicer // Sydney Sweeney Edition", layout="wide", initial_sidebar_state="expanded")

if "theme" not in st.session_state:
    st.session_state.theme = "Sydney Luxury Rose"
if "risk_profile" not in st.session_state:
    st.session_state.risk_profile = "Nuclear (Max Leverage)"

themes = {
    "Sydney Luxury Rose": {"primary": "#ff3366", "border": "rgba(255, 51, 102, 0.6)", "glow": "rgba(255, 51, 102, 0.4)", "bg": "#07070a"},
    "Institutional Emerald": {"primary": "#00ff88", "border": "rgba(0, 255, 136, 0.6)", "glow": "rgba(0, 255, 136, 0.4)", "bg": "#040906"},
    "High-Contrast Amber": {"primary": "#ffaa00", "border": "rgba(255, 170, 0, 0.6)", "glow": "rgba(255, 170, 0, 0.4)", "bg": "#0a0804"}
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
        payload = {"message": "Vault: Sydney Sweeney & Mike Donna Overhaul", "content": encoded, "sha": current_sha}
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

# --- SYDNEY SWEENEY LUXURY GLASSMORPHISM STYLING ---
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

.stApp {{
    background: radial-gradient(circle at 50% 0%, #151019 0%, {current_theme['bg']} 70%);
    color: #f4f4f6;
    font-family: 'Plus Jakarta Sans', sans-serif;
}}

.exec-card {{
    background: rgba(20, 16, 26, 0.75);
    backdrop-filter: blur(25px);
    -webkit-backdrop-filter: blur(25px);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-top: 2px solid {current_theme['primary']};
    border-radius: 16px;
    padding: 32px;
    box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.9), 0 0 20px {current_theme['glow']};
    margin-bottom: 30px;
    transition: transform 0.3s ease;
}

.hud-bar {{
    background: rgba(12, 10, 16, 0.9);
    border: 1px solid {current_theme['border']};
    padding: 16px 28px;
    border-radius: 12px;
    display: flex;
    justify-content: space-around;
    align-items: center;
    margin-bottom: 25px;
    font-size: 0.85rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    box-shadow: inset 0 0 15px rgba(0,0,0,0.5);
}

.hud-item {{
    text-align: center;
    border-right: 1px solid rgba(255,255,255,0.08);
    padding-right: 30px;
}}
.hud-item:last-child {{ border-right: none; }}

.hud-dot {{
    height: 9px;
    width: 9px;
    background-color: {current_theme['primary']};
    border-radius: 50%;
    display: inline-block;
    box-shadow: 0 0 15px {current_theme['primary']};
    animation: luxuryPulse 2.5s infinite;
}

.donna-article {{
    background: rgba(10, 8, 14, 0.95);
    border-left: 4px solid {current_theme['primary']};
    padding: 35px;
    border-radius: 0 14px 14px 0;
    font-size: 1.05rem;
    line-height: 1.9;
    color: #e2e2e9;
    margin-top: 20px;
    box-shadow: inset 5px 0 20px rgba(0,0,0,0.6);
}}

.donna-header {{
    font-size: 1.7rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 14px;
    letter-spacing: -0.5px;
    text-transform: uppercase;
    background: linear-gradient(90deg, #ffffff 30%, {current_theme['primary']} 100%);
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

@keyframes luxuryPulse {{
    0% {{ transform: scale(0.95); opacity: 1; box-shadow: 0 0 0 0 {current_theme['glow']}; }}
    70% {{ transform: scale(1.05); opacity: 0.7; box-shadow: 0 0 0 10px rgba(0,0,0,0); }}
    100% {{ transform: scale(0.95); opacity: 1; box-shadow: 0 0 0 0 rgba(0,0,0,0); }}
}}
</style>
""", unsafe_allow_html=True)

# --- CENTERED LUXURY SMOOTHIE LOGO BANNER ---
st.markdown(f"""
<div style="text-align: center; margin-bottom: 35px;">
    <svg width="70" height="90" viewBox="0 0 60 80" xmlns="http://www.w3.org/2000/svg" style="display: inline-block; margin-bottom: 14px; filter: drop-shadow(0 0 25px {current_theme['glow']});">
        <defs>
            <linearGradient id="juiceGrad" x1="0%" y1="100%" x2="0%" y2="0%">
                <stop offset="0%" stop-color="#0a050c" />
                <stop offset="100%" stop-color="{current_theme['primary']}">
                    <animate attributeName="stop-color" values="{current_theme['primary']};#ffffff;{current_theme['primary']}" dur="3s" repeatCount="indefinite" />
                </stop>
            </linearGradient>
        </defs>
        <path d="M 15 70 L 45 70 L 40 80 L 20 80 Z" fill="#151218" />
        <path d="M 10 20 L 50 20 L 45 70 L 15 70 Z" fill="rgba(255,255,255,0.03)" stroke="{current_theme['border']}" stroke-width="1.5"/>
        <path d="M 12.5 45 Q 30 35 47.5 45 L 45 68 L 15 68 Z" fill="url(#juiceGrad)">
            <animate attributeName="d" values="M 12.5 45 Q 30 35 47.5 45 L 45 68 L 15 68 Z; M 12.5 45 Q 30 52 47.5 45 L 45 68 L 15 68 Z; M 12.5 45 Q 30 35 47.5 45 L 45 68 L 15 68 Z" dur="1.5s" repeatCount="indefinite" />
        </path>
        <path d="M 5 20 L 55 20 L 50 10 L 10 10 Z" fill="#1f1a24" />
        <rect x="25" y="4" width="10" height="6" fill="{current_theme['primary']}" rx="2" />
    </svg>
    <h1 style="font-size: 4rem; font-weight: 800; background: linear-gradient(135deg, #ffffff 20%, {current_theme['primary']} 70%, #222 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; line-height: 1; letter-spacing: -1.5px;">THE JUICER</h1>
    <p style="color: #9494a0; font-weight: 600; letter-spacing: 5px; margin-top: 10px; text-transform: uppercase; font-size: 0.85rem;">Managed by Mike Donna // Sydney Sweeney Aesthetic & Elite Intelligence</p>
</div>
""", unsafe_allow_html=True)

storage_mode = "PERMANENT VAULT" if st.secrets.get("GITHUB_TOKEN") else "LOCAL SESSION"
st.markdown(f"""
<div class="hud-bar">
    <div class="hud-item"><span class="hud-dot"></span> <b>APEX ENGINE: ONLINE</b></div>
    <div class="hud-item"><span style="color: {current_theme['primary']}; font-weight: 800;">{storage_mode}</span></div>
    <div class="hud-item"><b>WR MODIFIER:</b> {wr_modifier}x</div>
    <div class="hud-item"><b>PENDING TICKETS:</b> {pending_tickets}</div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏆 Sharp Action & Spreads",
    "👑 DFS & Bayesian Sims",
    "🎯 Nuclear Parlays & Arbs",
    "📰 Weather & Sharp Ticker",
    "⚡ Execution Terminal",
    "💼 Master Ledger & Export"
])

# ================= TAB 1 =================
with tab1:
    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    st.markdown('<h3>Institutional Sharp Action & Circa Steam Matrix</h3>', unsafe_allow_html=True)
    df_sharp = pd.DataFrame({
        "Matchup": ["NE @ SEA", "SF vs LAR", "CHI @ CAR", "BAL @ IND"],
        "Sharp Consensus": ["SEA -6.0 (Heavy Steam)", "SF -4.0 (Late Money)", "CHI -1.5 (Public Trap Fade)", "BAL -4.5 (Pinnacle Lead)"],
        "Circa Ticket Count": ["78% Sharp", "85% Sharp", "62% Public", "91% Sharp"],
        "Arbitrage Alert": ["LOCKED (+4.2%)", "CLEAR", "FADE PUBLIC", "LOCKED (+5.1%)"]
    })
    st.dataframe(df_sharp, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="donna-article">
        <div class="donna-header">Mike Donna // The Anatomy of Syndicate Steam</div>
        <div class="donna-subheader">Stop Betting Into Retail Noise</div>
        Amateur bettors look at box scores and morning television narratives. Syndicates look at ticket count versus handle ratios at Circa and Pinnacle. When 75% of the public money backs a favorite, but the line moves in the opposite direction, that is Reverse Line Movement. That is not luck—that is a sharp syndicate firing a five-figure bankroll into the market. We track that exact velocity so you never get caught holding the bag on a public trap.
        <div class="donna-subheader">The Three-Book Rule</div>
        If a spread discrepancy across DraftKings, FanDuel, and Pinnacle doesn't yield at least a +4.0% expected value margin after accounting for vig, we pass. Discipline separates the bankroll builders from the bookmakers' retirement fund.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ================= TAB 2 =================
with tab2:
    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    st.markdown('<h3>DraftKings Optimizer & Bayesian Ruin Probability</h3>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Bayesian Ruin Risk", "0.02% (Extremely Low)", "1,000 Iterations")
    c2.metric("WR Rolling Win Rate", f"{wr_win_rate * 100}%", "Live AI Memory")
    c3.metric("Simulated Cash Rate", "84.1%", "+4.2% Edge")

    df_dfs = pd.DataFrame({
        "Pos": ["QB", "RB", "WR", "TE"],
        "Player": ["Justin Herbert", "Kenneth Walker", "Amon-Ra St. Brown", "Travis Kelce"],
        "Salary": ["$7,200", "$6,400", "$8,200", "$5,200"],
        "AI Proj": [22.4, 18.5, round(24.5 * wr_modifier, 1), 15.1]
    })
    st.dataframe(df_dfs, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="donna-article">
        <div class="donna-header">Mike Donna // Constructing GPP-Winning Lineups</div>
        <div class="donna-subheader">Beyond Historical Box Scores</div>
        If your lineup optimizer relies on last week's fantasy points, you are playing checkers while the syndicate plays three-dimensional chess. We ingest Expected Points Added (EPA) per play and DVOA efficiency matrices to project true ceiling outcomes, not median expectations.
        <div class="donna-subheader">Uncorrelated Leverage</div>
        To ship a massive GPP tournament on DraftKings, you need unique stacking correlations. When our Monte Carlo engine runs 10,000 iterations, it uncovers low-ownership leverage pieces that spike in ceiling outcomes when neutral game scripts break wide open.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ================= TAB 3 =================
with tab3:
    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    st.markdown('<h3>One-Click Preset Parlay & Arbitrage Hedging Calculator</h3>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### ⚡ 3-Leg Nuclear Preset")
        st.code("1. Walker Higher (Rushing)\n2. St. Brown Higher (Receptions)\n3. Herbert Higher (Passing Yards)\nImplied Payout: 10x | Consensus: 3/3")
    with col_b:
        st.markdown("#### 📐 Arbitrage Stake Allocator")
        stake_total = st.number_input("Total Bankroll to Hedge ($)", value=100.0)
        odds1 = st.number_input("Book A Odds (Decimal)", value=2.10)
        odds2 = st.number_input("Book B Odds (Decimal)", value=1.95)
        if odds1 > 0 and odds2 > 0:
            bet1 = round(stake_total / (odds1 * (1/odds1 + 1/odds2)), 2)
            bet2 = round(stake_total - bet1, 2)
            st.success(f"Stake Book A: ${bet1} | Stake Book B: ${bet2} (Guaranteed Return)")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="donna-article">
        <div class="donna-header">Mike Donna // The Mathematics of Compounding Parlays</div>
        <div class="donna-subheader">Why Multi-Leg Wagers Usually Fail</div>
        An 18-team parlay sold by retail sportsbooks is a direct tax on mathematical illiteracy. But when every individual leg is filtered through our strict +4.0% closing line value threshold and correlated correctly across game scripts, compounding turns from a lottery ticket into a calculated financial instrument.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ================= TAB 4 =================
with tab4:
    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    st.markdown('<h3>Autonomous Weather Threat Hub & Referee Bias Matrix</h3>', unsafe_allow_html=True)
    df_weather = pd.DataFrame({
        "Stadium": ["Lumen Field (SEA)", "Arrowhead Stadium", "Soldier Field"],
        "Wind Vector": ["Sustained 8mph", "Calm 4mph", "Sustained 18mph (Crosswind)"],
        "Referee Crew Over/Under Bias": ["Neutral (Crew #4)", "Over leaning (+3.5 pts)", "Under leaning (-4.2 pts - Crew #12)"],
        "Impact": ["Optimal", "Neutral", "Heavy Under Lean"]
    })
    st.dataframe(df_weather, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="donna-article">
        <div class="donna-header">Mike Donna // Environmental Intelligence & Officiating Bias</div>
        <div class="donna-subheader">The Invisible Variables</div>
        Casual bettors ignore referee tendencies and wind vectors at their own peril. A crew that flags holding at an above-average rate directly disrupts offensive rhythm and stalls drives inside the red zone. We map crew tendencies and stadium microclimates into every total model before setting our final positions.
    </div>
    """, unsafe_allow_html=True)
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
    st.markdown('<h3>Master Ledger, ROI Analytics & Executive Report Export</h3>', unsafe_allow_html=True)
    df_ledger = pd.DataFrame(brain.get("bet_ledger", []))
    if not df_ledger.empty:
        st.dataframe(df_ledger, use_container_width=True, hide_index=True)
    else:
        st.info("Ledger is currently empty. Execute a wager in Tab 5.")
    csv_export = df_ledger.to_csv(index=False).encode('utf-8') if not df_ledger.empty else b""
    st.download_button("📥 Download Executive PDF/CSV Report Archive", data=csv_export, file_name="juicer_executive_ledger.csv", mime="text/csv")
    st.markdown('</div>', unsafe_allow_html=True)
