import os

APP_FILE = "app.py"

def embed_tickers_into_app():
    print("="*65)
    print("🔧 [APP PATCHER] Embedding Lewis's 4-Tier Tickers into app.py...")
    print("="*65)
    
    if not os.path.exists(APP_FILE):
        print(f"   [ERROR] {APP_FILE} not found!")
        return

    with open(APP_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # The new 4-tier ticker block managed by Lewis
    four_tier_html = '''st.markdown("""
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
""", unsafe_allow_html=True)'''

    # If an older single ticker exists, replace it; otherwise append after master slate selectbox
    if 'ticker-wrap' in content:
        # Simple replacement of old ticker blocks
        parts = content.split('st.markdown("""\n<div class="ticker-wrap')
        if len(parts) > 1:
            prefix = parts[0]
            # Find where the old ticker markdown ends
            remainder = parts[1]
            end_idx = remainder.find('""", unsafe_allow_html=True)') + len('""", unsafe_allow_html=True)')
            suffix = remainder[end_idx:]
            new_content = prefix + four_tier_html + suffix
        else:
            new_content = content
    else:
        new_content = content + "\n" + four_tier_html

    with open(APP_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print("   [SUCCESS] app.py successfully patched with Lewis's 4-Tier Tickers.")
    print("="*65)
    print("✅ [APP PATCH COMPLETE]")
    print("="*65)

if __name__ == "__main__":
    embed_tickers_into_app()
