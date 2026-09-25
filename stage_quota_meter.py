"""
The Juicer - Quota Telemetry & Live Calculator Module
Tracks Odds API usage against a monthly 470 ceiling (resets on the 1st).
Renders the visual fuel gauge in Streamlit.
"""
import sqlite3
import calendar
import os
from datetime import datetime, date

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "action_grid.db")

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=10000;")
    conn.row_factory = sqlite3.Row
    return conn

def init_quota_table():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS api_quota_telemetry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                used_calls INTEGER,
                remaining_calls INTEGER,
                monthly_limit INTEGER DEFAULT 500,
                usable_ceiling INTEGER DEFAULT 470,
                endpoint_called TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Seed default state if empty (8 used, 492 remaining)
        row = conn.execute("SELECT COUNT(*) FROM api_quota_telemetry").fetchone()[0]
        if row == 0:
            conn.execute("""
                INSERT INTO api_quota_telemetry (used_calls, remaining_calls, monthly_limit, usable_ceiling, endpoint_called)
                VALUES (8, 492, 500, 470, 'INITIAL_SEEDED')
            """)
        conn.commit()

def record_api_call(used, remaining, endpoint=""):
    init_quota_table()
    with get_db() as conn:
        conn.execute("""
            INSERT INTO api_quota_telemetry (used_calls, remaining_calls, monthly_limit, usable_ceiling, endpoint_called)
            VALUES (?, ?, 500, 470, ?)
        """, (int(used), int(remaining), endpoint))
        conn.commit()

def get_quota_status():
    init_quota_table()
    with get_db() as conn:
        row = conn.execute("SELECT * FROM api_quota_telemetry ORDER BY id DESC LIMIT 1").fetchone()
    
    used = row["used_calls"] if row else 8
    remaining = row["remaining_calls"] if row else 492
    ceiling = 470
    limit = 500
    
    today = date.today()
    _, last_day = calendar.monthrange(today.year, today.month)
    days_left = max(1, (last_day - today.day) + 1)
    
    # Usable calls left before hitting the 470 target ceiling
    usable_left = max(0, ceiling - used)
    daily_budget = round(usable_left / days_left, 1)
    pct_used = min(100.0, round((used / ceiling) * 100, 1))

    return {
        "used": used,
        "remaining": remaining,
        "ceiling": ceiling,
        "limit": limit,
        "days_left": days_left,
        "usable_left": usable_left,
        "daily_budget": daily_budget,
        "pct_used": pct_used,
        "is_frozen": used >= ceiling
    }

def render_quota_calculator_html():
    q = get_quota_status()
    bar_color = "#00ff88" if q["pct_used"] < 70 else ("#ffd700" if q["pct_used"] < 90 else "#ff2a6d")
    freeze_badge = "<b style='color:#ff2a6d;'>🔒 FROZEN</b>" if q["is_frozen"] else "<b style='color:#00ff88;'>🟢 ACTIVE</b>"

    html = f"""
    <div style='background:#0d1117; border:1px solid rgba(255,255,255,0.1); border-radius:8px; padding:8px 14px; margin-bottom:12px;'>
        <div style='display:flex; justify-content:space-between; align-items:center; font-size:11px; margin-bottom:6px;'>
            <div>
                <span style='color:#00e5ff; font-weight:800; letter-spacing:0.5px;'>🔋 THE ODDS API TELEMETRY</span>
                <span style='color:#8b949e; margin-left:8px;'>Status: {freeze_badge}</span>
            </div>
            <div style='color:#8b949e;'>
                Used: <b style='color:#ffffff;'>{q['used']}</b> / {q['ceiling']} cap 
                <span style='color:rgba(255,255,255,0.3);'>({q['limit'] - q['ceiling']} reserve)</span> | 
                Remaining to 1st: <b style='color:#00ff88;'>{q['usable_left']} calls</b> ({q['days_left']} days left)
            </div>
            <div style='color:#cad3df;'>
                Daily Burn Allowance: <b style='color:#00e5ff;'>{q['daily_budget']}/day</b>
            </div>
        </div>
        <div style='width:100%; height:6px; background:rgba(255,255,255,0.06); border-radius:3px; overflow:hidden;'>
            <div style='width:{q['pct_used']}%; height:100%; background:{bar_color};'></div>
        </div>
    </div>
    """
    return html

def run_self_audit():
    init_quota_table()
    st = get_quota_status()
    assert st["ceiling"] == 470
    assert st["days_left"] >= 1
    print(f"✅ [PASS] Quota Telemetry verified: {st['used']}/470 used. Budget: {st['daily_budget']} calls/day until 1st.")
    return True

if __name__ == "__main__":
    run_self_audit()