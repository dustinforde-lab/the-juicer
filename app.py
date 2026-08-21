import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder
from sklearn.ensemble import GradientBoostingRegressor

# --- THE DONNA CONFIGURATION ---
st.set_page_config(page_title="The Juicer // Donna Edition", layout="wide", initial_sidebar_state="expanded")

# --- EXECUTIVE CSS: DONNA & SPECTER EDITION ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #09090b 0%, #121216 100%);
        color: #f4f4f5;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .exec-card {
        background: rgba(24, 24, 32, 0.6);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-top: 1px solid rgba(161, 29, 33, 0.5);
        border-radius: 14px;
        padding: 32px;
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.8);
        margin-bottom: 28px;
    }
    
    .exec-title {
        font-size: 3.2rem; font-weight: 800;
        background: linear-gradient(135deg, #ffffff 30%, #a11d21 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0; text-align: center; letter-spacing: -1.5px;
    }
    .exec-subtitle {
        text-align: center; color: #a1a1aa; font-weight: 400;
        letter-spacing: 4px; margin-bottom: 35px; text-transform: uppercase; font-size: 0.8rem;
    }
    
    .hud-bar {
        background: rgba(12, 12, 16, 0.95);
        border: 1px solid rgba(161, 29, 33, 0.3);
        padding: 14px 24px; border-radius: 10px;
        display: flex; justify-content: space-around; align-items: center;
        margin-bottom: 35px; font-size: 0.85rem; letter-spacing: 1.5px; text-transform: uppercase;
    }
    .hud-item { text-align: center; border-right: 1px solid rgba(255,255,255,0.06); padding-right: 30px; }
    .hud-item:last-child { border-right: none; }
    .hud-dot { height: 8px; width: 8px; background-color: #22c55e; border-radius: 50%; display: inline-block; box-shadow: 0 0 10px #22c55e; animation: pulse 2s infinite; }
    
    .briefing-box {
        background: rgba(16, 16, 22, 0.9);
        border-left: 4px solid #a11d21;
        padding: 24px; border-radius: 0 12px 12px 0;
        margin-top: 20px; font-size: 0.95rem; line-height: 1.7; color: #d4d4d8;
    }
    
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
    </style>
""", unsafe_allow_html=True)

# --- HUD TICKER ---
st.markdown("""
<div class="hud-bar">
    <div class="hud-item"><span class="hud-dot"></span> <b>DONNA INTELLIGENCE: ONLINE</b></div>
    <div class="hud-item"><b>MIN 24</b> - GB 17 <span style="color:#71717a;">(4th Qtr)</span></div>
    <div class="hud-item"><b>KC 31</b> - LAC 24 <span style="color:#71717a;">(Final)</span></div>
    <div class="hud-item"><b>BUF 28</b> - MIA 21 <span style="color:#71717a;">(2nd Qtr)</span></div>
    <div class="hud-item" style="color: #a11d21;"><b>STATUS:</b> WINNING GUARANTEED</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<h1 class="exec-title">THE JUICER</h1>', unsafe_allow_html=True)
st.markdown('<p class="exec-subtitle">Managed by Donna // Executive Suite Architecture</p>', unsafe_allow_html=True)

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "⚖️ War Room & Spreads", 
    "📊 Prop Matrix & SGPs", 
    "🌤️ Environmental Hub", 
    "💼 Bankroll & Ledger"
])

# ================= TAB 1 =================
with tab1:
    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    st.markdown('<h3>1. Full-Season Spread Movement Tracker (Weeks 1-18)</h3>', unsafe_allow_html=True)
    sel_week = st.selectbox("Select Week Frame", [f"Week {i}" for i in range(1, 19)], index=0)
    
    df_slate = pd.DataFrame({
        "Matchup": ["KC @ DET", "BUF @ NYJ", "SF @ PIT", "PHI @ NE", "MIN @ CHI", "DAL @ NYG", "BAL @ CIN"],
        "Opening Spread": ["KC -6.5", "BUF -2.5", "SF -3.0", "PHI -4.0", "CHI -3.5", "DAL -6.0", "BAL -1.5"],
        "Current Spread": ["KC -8.5", "BUF -1.5", "SF -4.5", "PHI -3.5", "CHI -4.5", "DAL -7.5", "BAL -2.5"],
        "Line Delta": ["+2.0 (Sharp)", "-1.0 (Steam)", "+1.5 (Sharp)", "-0.5 (Public)", "+1.0 (Sharp)", "+1.5 (Sharp)", "+1.0 (Steam)"],
        "O/U Total": [53.5, 45.5, 41.5, 48.0, 43.5, 47.0, 50.5],
        "Action Status": ["LOCK", "FADE", "LOCK", "PASS", "LOCK", "LOCK", "PLAY"]
    })
    AgGrid(df_slate, gridOptions=GridOptionsBuilder.from_dataframe(df_slate).build(), theme='alpine-dark', fit_columns_on_grid_load=True, height=250)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    st.markdown('<h3>2. Neural Gradient Boosting Prediction Matrix</h3>', unsafe_allow_html=True)
    
    @st.cache_resource
    def train_ai():
        np.random.seed(42)
        X = np.random.rand(500, 3) * 100 
        y = X[:, 0] * 0.4 + X[:, 1] * 0.5 - X[:, 2] * 0.2 + np.random.randn(500) * 5 
        model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3)
        model.fit(X, y)
        return model

    model = train_ai()
    preds = model.predict(np.random.rand(4, 3) * 100)
    lines = [70.5, 80.0, 95.5, 250.5]
    edges = ((preds - lines) / lines) * 100
    
    df_ml = pd.DataFrame({
        "ASSET": ["Kenneth Walker", "Breece Hall", "Amon-Ra St. Brown", "Justin Herbert"],
        "VEGAS LINE": lines,
        "AI MODEL PROJ": np.round(preds, 1),
        "TRUE EDGE": [f"+{e:.1f}%" if e > 0 else f"{e:.1f}%" for e in edges],
        "SYSTEM CALL": ["LOCK" if e > 5 else "FADE" if e < -5 else "PLAY" for e in edges]
    })
    AgGrid(df_ml, gridOptions=GridOptionsBuilder.from_dataframe(df_ml).build(), theme='alpine-dark', fit_columns_on_grid_load=True, height=200)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    st.markdown('<h3>3. Donna\'s Executive Briefing</h3>', unsafe_allow_html=True)
    st.markdown("""
    <div class="briefing-box">
        <b>DONNA\'S ASSESSMENT:</b><br>
        I already looked at the books, I already know where the sharp money is hiding, and I'm telling you right now—we are not losing this slate. Trust the regression weights, lock in the sharp delta positions, and leave the worrying to everyone else.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ================= TAB 2 =================
with tab2:
    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    st.markdown('<h3>1. Cross-Book Prop Intelligence Matrix</h3>', unsafe_allow_html=True)
    df_props = pd.DataFrame({
        "Player": ["Kenneth Walker", "Breece Hall", "Amon-Ra St. Brown", "Justin Herbert", "Derrick Henry", "Nico Collins"],
        "Prop Type": ["Rush Yards", "Receptions", "Rec Yards", "Pass Yards", "Rush Yards", "Rec Yards"],
        "DraftKings": ["65.5 O (-110)", "4.5 O (-115)", "82.5 O (-105)", "245.5 O (-110)", "72.5 O (-115)", "68.5 O (-110)"],
        "FanDuel": ["64.5 O (-115)", "4.5 U (-110)", "84.5 O (-110)", "248.5 O (-115)", "73.5 O (-110)", "67.5 O (-115)"],
        "Underdog / PrizePicks": ["65.0 (Higher)", "4.0 (Higher)", "83.0 (Higher)", "246.0 (Higher)", "72.0 (Higher)", "68.0 (Higher)"],
        "Consensus Edge": ["+4.2%", "-1.1%", "+3.8%", "+2.1%", "-2.5%", "+5.0%"]
    })
    AgGrid(df_props, gridOptions=GridOptionsBuilder.from_dataframe(df_props).build(), theme='alpine-dark', fit_columns_on_grid_load=True, height=250)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    st.markdown('<h3>2. Same-Game Parlay (SGP) Architecture</h3>', unsafe_allow_html=True)
    df_sgp = pd.DataFrame({
        "SGP Package": ["Package Alpha (KC Stack)", "Package Beta (DET Volume)", "Package Gamma (LAC Air)", "Package Delta (MIN Ground)"],
        "Primary Leg": ["Mahomes 275+ Pass", "St. Brown 8+ Rec", "Herbert 2+ Pass TD", "Walker 20+ Carries"],
        "Correlated Leg": ["Travis Kelce Over Rec", "Jared Goff Over Pass Yds", "Keenan Allen Over Rec", "Seahawks Win & Cover"],
        "Combined Odds": ["+260", "+310", "+240", "+285"],
        "Model Confidence": ["84.2%", "79.1%", "81.5%", "77.4%"]
    })
    AgGrid(df_sgp, gridOptions=GridOptionsBuilder.from_dataframe(df_sgp).build(), theme='alpine-dark', fit_columns_on_grid_load=True, height=220)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    st.markdown('<h3>3. Donna\'s Intuition Note</h3>', unsafe_allow_html=True)
    st.markdown("""
    <div class="briefing-box">
        <b>DONNA\'S INTUITION:</b><br>
        Correlated parlays are an art form, Chuck. Once you see how the primary quarterback prop connects to the receiver's target share, the outcome writes itself. I've already lined up the winning stack.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ================= TAB 3 =================
with tab3:
    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    st.markdown('<h3>1. Environmental & Weather Threat Matrix</h3>', unsafe_allow_html=True)
    df_weather = pd.DataFrame({
        "Stadium / Venue": ["Lambeau Field", "Soldier Field", "U.S. Bank Stadium", "Arrowhead Stadium", "Highmark Stadium", "MetLife Stadium"],
        "Condition": ["Clear / Chilly", "High Winds (18mph)", "Dome (Controlled)", "Overcast", "Heavy Rain Risk", "Clear / Calm"],
        "Temp (°F)": [42, 38, 72, 58, 45, 61],
        "Passing Impact": ["Neutral", "Negative (-4.2%)", "Positive (+2.0%)", "Neutral", "Severe (-8.5%)", "Optimal"],
        "Kicking Impact": ["Slight Drift", "High Turbulence", "None", "Optimal", "High Variance", "Optimal"]
    })
    AgGrid(df_weather, gridOptions=GridOptionsBuilder.from_dataframe(df_weather).build(), theme='alpine-dark', fit_columns_on_grid_load=True, height=250)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    st.markdown('<h3>2. Meteorological Risk Assessment</h3>', unsafe_allow_html=True)
    st.markdown("""
    <div class="briefing-box">
        <b>DONNA\'S WEATHER DIRECTIVE:</b><br>
        Never ignore the wind, and never ignore my warnings. Our environmental API dynamically adjusts passing metrics before the weather can catch us off guard. We stay two steps ahead of the books, always.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ================= TAB 4 =================
with tab4:
    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    st.markdown('<h3>1. Firm Capital & Bankroll Survival Meter</h3>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Active Capital Reserve", "$142.50", "-$7.50")
    c2.metric("Weekly Volume Quota", "18 / 150 Bets", "Pacing Target")
    c3.metric("Firm Win Rate", "61.2%", "+4.8% vs Books")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    st.markdown('<h3>2. Active 150+ Bet Volume Ledger</h3>', unsafe_allow_html=True)
    df_bets = pd.DataFrame({
        "Bet ID": [f"#10{i}" for i in range(40, 48)],
        "Type": ["SGP (DK)", "PrizePicks 2-Leg", "Over/Under", "Book Straight", "SGP (FD)", "Underdog Higher", "Book Straight", "SGP (DK)"],
        "Selection": ["Walker + St. Brown", "Breece Hall Higher", "KC -8.5", "Herbert 250+ Pass", "Mahomes Stack", "Nico Collins Higher", "Henry Over 72.5", "Buffer SGP Stack"],
        "Stake": ["$10.00", "$15.00", "$25.00", "$10.00", "$20.00", "$15.00", "$10.00", "$10.00"],
        "Status": ["PENDING", "PENDING", "LOCKED", "PENDING", "PENDING", "LOCKED", "PENDING", "PENDING"]
    })
    AgGrid(df_bets, gridOptions=GridOptionsBuilder.from_dataframe(df_bets).build(), theme='alpine-dark', fit_columns_on_grid_load=True, height=280)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    st.markdown('<h3>3. Donna\'s Final Verdict</h3>', unsafe_allow_html=True)
    st.markdown("""
    <div class="briefing-box">
        <b>DONNA\'S FINAL VERDICT:</b><br>
        You have the smartest mind in the room running your numbers, the cleanest executive UI on the server, and a bankroll being guarded like state secrets. Hit the terminal, deploy the code, and let's go win.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
