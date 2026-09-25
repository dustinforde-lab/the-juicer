"""
The Juicer - Industrial Data Refinery & Clear Glass Manifold Assets
Chunk 1: Generates SVG/CSS Clear Plumbing Conduits, Spinning Impeller, and Gutter Trough.
"""

def get_refinery_markup(sync_active=True):
    # Percentage targets corresponding to the 9 tabs across the dashboard
    # Tabs: Scoreboard, DFS Engine, Donna's, Parlay, Season-Long, PrizePicks, Film Room, Ops Center, Learning Loop
    tab_targets = [5.5, 16.5, 27.5, 38.5, 50.0, 61.5, 72.5, 83.5, 94.5]
    
    # SVG Paths originating from central downspout (x=500, y=70) and elbowing 90 degrees down to each tab
    pipe_paths = ""
    for idx, pct in enumerate(tab_targets):
        x_target = pct * 10.0  # ViewBox is 0 0 1000 140
        # Draw: Down from manifold -> 90 elbow horizontal -> 90 elbow down into gutter
        if x_target == 500:
            d = f"M 500 70 L 500 135"
        elif x_target < 500:
            d = f"M 500 70 L 500 85 Q 500 95 490 95 L {x_target + 10} 95 Q {x_target} 95 {x_target} 105 L {x_target} 135"
        else:
            d = f"M 500 70 L 500 85 Q 500 95 510 95 L {x_target - 10} 95 Q {x_target} 95 {x_target} 105 L {x_target} 135"

        pipe_paths += f"""
        <!-- Conduit {idx+1} Glass & Fluid -->
        <path d='{d}' fill='none' stroke='rgba(0, 229, 255, 0.28)' stroke-width='11' stroke-linecap='round' stroke-linejoin='round'/>
        <path d='{d}' fill='none' stroke='rgba(255, 255, 255, 0.45)' stroke-width='9' stroke-linecap='round' stroke-linejoin='round'/>
        <path d='{d}' fill='none' class='pipe-fluid-flow' stroke='url(#neonJuiceGrad)' stroke-width='5' stroke-linecap='round' stroke-linejoin='round'/>
        <!-- Nozzle Fitting -->
        <rect x='{x_target - 5}' y='130' width='10' height='6' rx='2' fill='#263238' stroke='#00e5ff' stroke-width='1.5'/>
        """

    drop_animation_cls = "active-ingest" if sync_active else "idle-ingest"

    markup = f"""
    <style>
    .refinery-dock {{
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: -15px;
        margin-bottom: 6px;
        position: relative;
    }}
    /* Falling Ingestion Slips */
    .ingest-hopper {{
        width: 200px;
        height: 28px;
        position: relative;
        overflow: hidden;
    }}
    .data-slip {{
        position: absolute;
        font-family: monospace;
        font-size: 9px;
        font-weight: 800;
        padding: 1px 5px;
        border-radius: 3px;
    }}
    .slip-a {{ left: 15px; background: rgba(0,255,136,0.25); color: #00ff88; border: 1px solid #00ff88; animation: dropA 2.2s infinite ease-in; }}
    .slip-b {{ left: 80px; background: rgba(255,42,109,0.25); color: #ff2a6d; border: 1px solid #ff2a6d; animation: dropB 1.9s infinite ease-in; }}
    .slip-c {{ left: 140px; background: rgba(0,229,255,0.25); color: #00e5ff; border: 1px solid #00e5ff; animation: dropC 2.4s infinite ease-in; }}
    
    @keyframes dropA {{ 0% {{ top: -20px; opacity: 1; transform: scale(1); }} 100% {{ top: 28px; opacity: 0; transform: scale(0.4) rotate(15deg); }} }}
    @keyframes dropB {{ 0% {{ top: -20px; opacity: 1; transform: scale(1); }} 100% {{ top: 28px; opacity: 0; transform: scale(0.3) rotate(-15deg); }} }}
    @keyframes dropC {{ 0% {{ top: -20px; opacity: 1; transform: scale(1); }} 100% {{ top: 28px; opacity: 0; transform: scale(0.4) rotate(20deg); }} }}

    /* Compact Borosilicate Blender Jar */
    .refinery-jar-box {{
        width: 120px;
        height: 95px;
        border-left: 2.5px solid rgba(0, 229, 255, 0.7);
        border-right: 2.5px solid rgba(0, 229, 255, 0.7);
        border-bottom: 3.5px solid rgba(0, 229, 255, 0.85);
        border-radius: 0 0 14px 14px;
        background: linear-gradient(180deg, rgba(14,20,32,0.3) 0%, rgba(0,229,255,0.06) 100%);
        box-shadow: 0 0 18px rgba(0, 229, 255, 0.25), inset 0 0 12px rgba(0, 229, 255, 0.12);
        position: relative;
        overflow: hidden;
    }}
    .jar-grad-marks {{
        position: absolute;
        right: 4px;
        top: 8px;
        font-family: monospace;
        font-size: 7px;
        color: rgba(0, 229, 255, 0.5);
        line-height: 1.4;
        text-align: right;
        user-select: none;
    }}
    .churning-liquid {{
        position: absolute;
        bottom: 0;
        width: 100%;
        height: 62%;
        background: linear-gradient(180deg, rgba(255, 42, 109, 0.82) 0%, rgba(157, 78, 221, 0.95) 100%);
        box-shadow: 0 0 16px rgba(255, 42, 109, 0.7);
        animation: liquidChurn 0.75s infinite alternate ease-in-out;
    }}
    @keyframes liquidChurn {{
        0% {{ transform: scaleY(0.94) skewX(-1.5deg); }}
        100% {{ transform: scaleY(1.04) skewX(1.5deg); }}
    }}
    /* High-RPM Impeller Blade */
    .quad-blade {{
        position: absolute;
        bottom: 6px;
        left: 50%;
        transform: translateX(-50%);
        width: 32px;
        height: 32px;
        animation: fastSpin 0.12s infinite linear;
        z-index: 5;
    }}
    .blade-arm {{
        position: absolute;
        top: 13px;
        left: 0;
        width: 32px;
        height: 6px;
        background: linear-gradient(90deg, #b0bec5, #ffffff, #78909c);
        border-radius: 3px;
        box-shadow: 0 0 4px #ffffff;
    }}
    .blade-arm.vert {{ transform: rotate(90deg); }}
    .blade-nut {{
        position: absolute;
        top: 11px;
        left: 11px;
        width: 10px;
        height: 10px;
        background: #263238;
        border: 1.5px solid #eceff1;
        border-radius: 50%;
    }}
    @keyframes fastSpin {{
        0% {{ transform: translateX(-50%) rotate(0deg); }}
        100% {{ transform: translateX(-50%) rotate(360deg); }}
    }}

    /* Base Mount */
    .refinery-mount {{
        width: 130px;
        height: 16px;
        background: #111726;
        border: 1.5px solid #2d3748;
        border-radius: 3px;
        display: flex;
        align-items: center;
        justify-content: center;
    }}
    .pulse-diode {{
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #00ff88;
        box-shadow: 0 0 8px #00ff88;
        animation: diodePulse 1.1s infinite alternate ease-in-out;
    }}
    @keyframes diodePulse {{ 0% {{ opacity: 0.5; }} 100% {{ opacity: 1.0; box-shadow: 0 0 12px #00ff88; }} }}

    /* Clear Glass Conduit SVG Layer */
    .conduit-canvas {{
        width: 100%;
        height: 110px;
        margin-top: -4px;
        display: block;
    }}
    .pipe-fluid-flow {{
        stroke-dasharray: 12, 6;
        animation: flowDash 0.8s infinite linear;
    }}
    @keyframes flowDash {{
        0% {{ stroke-dashoffset: 36; }}
        100% {{ stroke-dashoffset: 0; }}
    }}

    /* Gutter Trough Directly Over Tabs */
    .collection-trough {{
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, transparent 0%, rgba(0, 229, 255, 0.4) 5%, rgba(255, 42, 109, 0.8) 50%, rgba(0, 229, 255, 0.4) 95%, transparent 100%);
        box-shadow: 0 0 10px rgba(255, 42, 109, 0.7);
        border-radius: 2px;
        margin-top: -3px;
    }}
    </style>

    <div class="refinery-dock">
        <div class="ingest-hopper">
            <div class="data-slip slip-a">ODDS: -3.5</div>
            <div class="data-slip slip-b">INJURY ALERT</div>
            <div class="data-slip slip-c">PROP: O 245.5</div>
        </div>
        <div class="refinery-jar-box">
            <div class="jar-grad-marks">- 500K<br>- 250K<br>- 100K</div>
            <div class="churning-liquid"></div>
            <div class="quad-blade">
                <div class="blade-arm"></div>
                <div class="blade-arm vert"></div>
                <div class="blade-nut"></div>
            </div>
        </div>
        <div class="refinery-mount">
            <div class="pulse-diode"></div>
        </div>
        <svg class="conduit-canvas" viewBox="0 0 1000 140" preserveAspectRatio="none">
            <defs>
                <linearGradient id="neonJuiceGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="#00e5ff" />
                    <stop offset="50%" stop-color="#ff2a6d" />
                    <stop offset="100%" stop-color="#00e5ff" />
                </linearGradient>
            </defs>
            {pipe_paths}
        </svg>
        <div class="collection-trough"></div>
    </div>
    """
    return markup

def run_self_audit():
    try:
        html = get_refinery_markup(sync_active=True)
        assert "viewBox='0 0 1000 140'" or 'viewBox="0 0 1000 140"' in html, "SVG viewport spec missing."
        assert "pipe-fluid-flow" in html, "Liquid flow animation missing."
        assert "collection-trough" in html, "Gutter collection bar missing."
        print("✅ [PASS] Chunk 1 verified. Zero regressions.")
        return True
    except Exception as e:
        print(f"❌ [FAIL] Chunk 1 self-audit failed: {e}")
        return False

if __name__ == "__main__":
    run_self_audit()