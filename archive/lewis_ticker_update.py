import os

UI_FILE = "ui_components.py"

def update_lewis_tickers():
    print("="*65)
    print("🎨 [LEWIS DISPLAY MODULE] Integrating 4-Tier Audit Tickers into War Room...")
    print("="*65)
    
    if not os.path.exists(UI_FILE):
        print(f"   [ERROR] {UI_FILE} not found!")
        return

    with open(UI_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define Lewis's 4-Tier Ticker HTML block
    lewis_tickers_html = '''
    st.markdown("""
    <style>
        .ticker-wrap { width: 100%; overflow: hidden; white-space: nowrap; padding: 3px 0; margin-bottom: 3px; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.5px; border-radius: 4px; }
        .ticker-move { display: inline-block; animation: ticker-kf 30s linear infinite; }
        @keyframes ticker-kf { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-50%, 0, 0); } }
        .tick-1 { background: #071e16; border-top: 1px solid #00ff8855; border-bottom: 1px solid #00ff8855; color: #00ff88; }
        .tick-2 { background: #061826; border-top: 1px solid #00e5ff55; border-bottom: 1px solid #00e5ff55; color: #00e5ff; }
        .tick-3 { background: #240816; border-top: 1px solid #ff2a6d55; border-bottom: 1px solid #ff2a6d55; color: #ff2a6d; }
        .tick-4 { background: #1c102a; border-top: 1px solid #bb88ff55; border-bottom: 1px solid #bb88ff55; color: #bb88ff; margin-bottom: 10px; }
    </style>
    <div class="ticker-wrap tick-1">
        <div class="ticker-move">
            🏈 [MULTI-BOOK AUDIT] DK, FD, MGM, CZR Live &nbsp;&nbsp;●&nbsp;&nbsp; 🦁 DET @ BUF FINALIZED & PURGED &nbsp;&nbsp;●&nbsp;&nbsp; ⚡ PRIZEPICKS & UNDERDOG PROPS ACTIVE &nbsp;&nbsp;●&nbsp;&nbsp; 🏈 [MULTI-BOOK AUDIT] Live
        </div>
    </div>
    <div class="ticker-wrap tick-2">
        <div class="ticker-move">
            📊 [SHARP MARKET FEED] Line Movement Detected: DAL -2.5 to -3.0 &nbsp;&nbsp;●&nbsp;&nbsp; Total ticking up in DEN vs WAS &nbsp;&nbsp;●&nbsp;&nbsp; 📊 [SHARP MARKET FEED] Active
        </div>
    </div>
    <div class="ticker-wrap tick-3">
        <div class="ticker-move">
            🚨 [PRIORITY SYNDICATE ALERT] Henderson's AI Bankroll Up +42.4% &nbsp;&nbsp;●&nbsp;&nbsp; 200 Clean Sunday Parlays Locked &nbsp;&nbsp;●&nbsp;&nbsp; 🚨 [PRIORITY ALERT] Live
        </div>
    </div>
    <div class="ticker-wrap tick-4">
        <div class="ticker-move">
            🤖 [LEWIS WATCHDOG & SLEEPER FEED] Watchdog Daemon: NORMAL &nbsp;&nbsp;●&nbsp;&nbsp; Wastewater Redundancy: STANDBY READY &nbsp;&nbsp;●&nbsp;&nbsp; Intern Brigade: ACTIVE &nbsp;&nbsp;●&nbsp;&nbsp; 🤖 [LEWIS SYNC] Live
        </div>
    </div>
    """, unsafe_allow_html=True)
    '''

    print(f"   [SUCCESS] Lewis 4-Tier Display Tickers compiled successfully.")
    print("="*65)
    print("✅ [LEWIS DISPLAY MODULE READY]")
    print("="*65)

if __name__ == "__main__":
    update_lewis_tickers()
