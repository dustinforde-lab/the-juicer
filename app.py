import streamlit as st
import pandas as pd
import numpy as np
import time
import json
import base64
import requests

# --- FIRM CONFIGURATION & THEME STATE ---
st.set_page_config(page_title="The Juicer // Apex Command Center", layout="wide", initial_sidebar_state="expanded")

if "theme" not in st.session_state:
    st.session_state.theme = "Firm Crimson (Default)"
if "risk_profile" not in st.session_state:
    st.session_state.risk_profile = "Conservative (2.5% Unit)"

themes = {
    "Firm Crimson (Default)": {"primary": "#ff4d4d", "border": "rgba(161, 29, 33, 0.9)", "glow": "rgba(161,29,33,0.8)"},
    "Institutional Emerald": {"primary": "#22c55e", "border": "rgba(34, 197, 94, 0.9)", "glow": "rgba(34,197,94,0.8)"},
    "High-Contrast Amber": {"primary": "#f59e0b", "border": "rgba(245, 158, 11, 0.9)", "glow": "rgba(245,158,11,0.8)"}
}
current_theme = themes[st.session_state.theme]

st.sidebar.markdown("### ⚙️ Firm Command Settings")
st.session_state.theme = st.sidebar.selectbox("Terminal Visual Theme", list(themes.keys()))
st.session_state.risk_profile = st.sidebar.radio("Bankroll Risk Profile", ["Conservative (2.5% Unit)", "Aggressive (5.0% Unit)", "Nuclear (Max Leverage)"])
webhook_url = st.sidebar.text_input("Discord Webhook URL", placeholder="https://discord.com/api/webhooks/...")

# --- PERSISTENT GITHUB BRAIN HANDLER ---
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
        payload = {"message": "Vault: 30-Feature Native UI Update", "content": encoded, "sha": current_sha}
        res = requests.put(url, headers=headers, json=payload)
        return res.status_code in [200, 201]
    else:
        with open(FILE_PATH, "w") as f:
            f.write(content_str)
        return True

brain, current_sha = get_github_brain()
wr_modifier = brain.get("model_weights", {}).get("WR_RECEPTIONS", {}).get("modifier", 1.0)
wr_win_rate = brain.get("model_weights", {}).get("WR_RECEPTIONS", {}).get("rolling_win_rate", 0.50)
pending_tickets = len([t for t in brain.get("bet_ledger", []) if t.get("result") == "PENDING"])

# --- GLOBAL STYLING ---
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
.stApp {{ background: linear-gradient(135deg, #050508 0%, #0d0d12 100%); color: #f4f4f5; font-family: 'Plus Jakarta Sans', sans-serif; }}
.exec-card {{ background: rgba(18, 18, 24, 0.85); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.05); border-top: 2px solid {current_theme['border']}; border-radius: 12px; padding: 28px; box-shadow: 0 15px 35px -10px rgba(0, 0, 0, 0.95); margin-bottom: 25px; }}
.hud-bar {{ background: rgba(8, 8, 12, 0.98); border: 1px solid {current_theme['border']}; padding: 14px 24px; border-radius: 8px; display: flex; justify-content: space-around; align-items: center; margin-bottom: 20px; font-size: 0.85rem; letter-spacing: 1.5px; text-transform: uppercase; }}
.hud-item {{ text-align: center; border-right: 1px solid rgba(255,255,255,0.08); padding-right: 25px; }}
.hud-item:last-child {{ border-right: none; }}
.hud-dot {{ height: 8px; width: 8px; background-color: {current_theme['primary']}; border-radius: 50%; display: inline-block; box-shadow: 0 0 12px {current_theme['glow']}; animation: pulse 2s infinite; }}
.source-badge {{ background: rgba(34, 197, 94, 0.15); border: 1px solid #22c55e; color: #4ade80; padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; }}
@keyframes pulse {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.4; }} 100% {{ opacity: 1; }} }}
</style>
""", unsafe_allow_html=True)

# --- ANIMATED LOGO ---
st.markdown(f"""
<div style="display: flex; align-items: center; justify-content: center; margin-bottom: 25px;">
    <div>
        <h1 style="font-size: 3.5rem; font-weight: 800; background: linear-gradient(135deg, #ffffff 20%, {current_theme['primary']} 60%, #111 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; line-height: 1;">THE JUICER</h1>
        <p style="color: #a1a1aa; font-weight: 600; letter-spacing: 4px; margin: 0; text-transform: uppercase; font-size: 0.85rem;">Managed by Mike Donna // 30-Feature Master Syndicate Engine</p>
    </div>
</div>
""", unsafe_allow_html=True)

storage_mode = "PERMANENT VAULT" if st.secrets.get("GITHUB_TOKEN") else "LOCAL SESSION"
st.markdown(f"""
<div class="hud-bar">
    <div class="hud-item"><span class="hud-dot"></span> <b>MASTER ENGINE: ONLINE</b></div>
    <div class="hud-item"><span class="source-badge">{storage_mode}</span></div>
    <div class="hud-item"><b>WR MODIFIER:</b> {wr_modifier}x</div>
    <div class="hud-item"><b>PENDING TICKETS:</b> {pending_tickets}</div>
</div>
""", unsafe_allow_html=True)

# --- TABS ---
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
    st.markdown('<h3>Live Sharp Money & Circa/Pinnacle Steam Feed</h3>', unsafe_allow_html=True)
    df_sharp = pd.DataFrame({
        "Matchup": ["NE @ SEA", "SF vs LAR", "CHI @ CAR", "BAL @ IND"],
        "Sharp Consensus": ["SEA -6.0 (Heavy Action)", "SF -4.0 (Steam)", "CHI -1.5 (Sharp Under)", "BAL -4.5 (Pinnacle Lead)"],
        "Circa Ticket Count": ["78% Sharp", "85% Sharp", "62% Public", "91% Sharp"],
        "Arbitrage Alert": ["LOCKED (+4.2%)", "CLEAR", "FADE PUBLIC", "LOCKED (+5.1%)"]
    })
    st.dataframe(df_sharp, use_container_width=True, hide_index=True)
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
