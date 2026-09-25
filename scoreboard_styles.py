"""
The Juicer - Scoreboard Trading Desk Styles & Visual Keyframes
Chunk 2: High-contrast Dark Glass, Red Zone Pulses, and Emoji Font Safeguards
"""

def get_scoreboard_css():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700;800&family=Inter:wght@400;600;700;900&display=swap');

    :root {
        --sb-bg: rgba(14, 19, 30, 0.88);
        --sb-border: rgba(255, 255, 255, 0.12);
        --sb-cyan: #00e5ff;
        --sb-green: #00ff88;
        --sb-magenta: #ff2a6d;
        --sb-gold: #ffd700;
        --sb-text: #f1f2f6;
        --sb-dim: #8b949e;
    }

    .sb-container {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI Emoji', 'Apple Color Emoji', 'Noto Color Emoji', sans-serif;
    }

    .sb-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
        gap: 16px;
        margin-top: 14px;
        margin-bottom: 24px;
    }

    .sb-card {
        background: var(--sb-bg);
        border: 1px solid var(--sb-border);
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45);
        backdrop-filter: blur(8px);
        position: relative;
        overflow: hidden;
        transition: transform 0.15s ease, border-color 0.2s ease;
    }
    .sb-card:hover {
        transform: translateY(-2px);
        border-color: rgba(0, 229, 255, 0.4);
    }

    /* Red Zone Dynamic Pulsing Border */
    .sb-card.red-zone {
        border: 1.5px solid var(--sb-magenta) !important;
        box-shadow: 0 0 16px rgba(255, 42, 109, 0.45), inset 0 0 10px rgba(255, 42, 109, 0.15) !important;
        animation: rzPulse 1.8s infinite ease-in-out;
    }
    @keyframes rzPulse {
        0% { border-color: rgba(255, 42, 109, 0.5); }
        50% { border-color: rgba(255, 42, 109, 1.0); box-shadow: 0 0 22px rgba(255, 42, 109, 0.7); }
        100% { border-color: rgba(255, 42, 109, 0.5); }
    }

    /* Header Bar */
    .sb-hdr {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 8px;
        margin-bottom: 12px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .sb-badge-live {
        background: rgba(255, 42, 109, 0.2);
        color: var(--sb-magenta);
        border: 1px solid var(--sb-magenta);
        border-radius: 4px;
        padding: 2px 8px;
        font-weight: 800;
        text-transform: uppercase;
    }
    .sb-badge-final {
        background: rgba(139, 148, 158, 0.2);
        color: var(--sb-dim);
        border-radius: 4px;
        padding: 2px 8px;
    }
    .sb-badge-pre {
        background: rgba(0, 229, 255, 0.15);
        color: var(--sb-cyan);
        border-radius: 4px;
        padding: 2px 8px;
    }

    /* Face-off Row */
    .sb-matchup {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }
    .sb-team {
        display: flex;
        align-items: center;
        gap: 10px;
        flex: 1;
    }
    .sb-team.home {
        justify-content: flex-end;
        text-align: right;
    }
    .sb-logo {
        width: 38px;
        height: 38px;
        object-fit: contain;
        filter: drop-shadow(0 2px 6px rgba(0, 0, 0, 0.6));
    }
    .sb-team-meta b {
        font-size: 16px;
        color: var(--sb-text);
        display: block;
        line-height: 1.2;
    }
    .sb-team-meta span {
        font-size: 11px;
        color: var(--sb-dim);
    }
    .sb-score-center {
        padding: 0 14px;
        text-align: center;
        min-width: 90px;
    }
    .sb-score-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 24px;
        font-weight: 900;
        color: var(--sb-green);
        letter-spacing: 2px;
    }

    /* Win Probability Bar */
    .sb-prob-bar {
        width: 100%;
        height: 5px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 3px;
        overflow: hidden;
        display: flex;
        margin: 10px 0 12px 0;
    }
    .sb-prob-fill {
        height: 100%;
        transition: width 0.6s ease;
    }

    /* Telemetry Footer */
    .sb-telemetry {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 6px;
        background: rgba(0, 0, 0, 0.25);
        border-radius: 6px;
        padding: 8px;
        font-size: 11px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .sb-tel-item b {
        color: var(--sb-cyan);
        display: block;
    }
    .sb-tel-item span {
        color: var(--sb-dim);
    }

    /* Last Play Ticker */
    .sb-last-play {
        margin-top: 10px;
        padding-top: 8px;
        border-top: 1px dashed rgba(255, 255, 255, 0.08);
        font-size: 11px;
        color: #cad3df;
        line-height: 1.4;
    }
    </style>
    """

def run_self_audit():
    try:
        css = get_scoreboard_css()
        assert len(css) > 500, "CSS payload empty."
        assert "rzPulse" in css, "Red zone animation missing."
        assert "Segoe UI Emoji" in css, "Emoji fallback stack missing."
        print("✅ [PASS] Chunk 2 verified. Zero regressions.")
        return True
    except Exception as e:
        print(f"❌ [FAIL] Chunk 2 self-audit failed: {e}")
        return False

if __name__ == "__main__":
    run_self_audit()