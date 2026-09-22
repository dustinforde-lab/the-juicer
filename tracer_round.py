import sqlite3
import json
import datetime

print("\n" + "="*55)
print("🧪 THE JUICER: INJECTING PLUMBING TRACER ROUND")
print("="*55)

try:
    conn = sqlite3.connect("action_grid.db")
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. Inject 1 Fake DFS Lineup (9 players)
    fake_dfs = (
        "TRACER_QB (TEST)", "TRACER_RB1 (TEST)", "TRACER_RB2 (TEST)",
        "TRACER_WR1 (TEST)", "TRACER_WR2 (TEST)", "TRACER_WR3 (TEST)",
        "TRACER_TE (TEST)", "TRACER_FLEX (TEST)", 999.99
    )
    
    conn.execute(
        "INSERT INTO dfs_rosters (qb, rb1, rb2, wr1, wr2, wr3, te, flex, projected_score) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
        fake_dfs
    )
    print("✅ Tracer DFS Roster Injected.")

    # 2. Inject 3 Fake Slips (PrizePicks, Underdog, Parlay)
    fake_legs = json.dumps([
        {"player_name": "TRACER_WR1 (TEST)", "stat_category": "receiving_yds", "line": 99.5, "direction": "OVER"},
        {"player_name": "TRACER_RB1 (TEST)", "stat_category": "rushing_yds", "line": 45.5, "direction": "UNDER"}
    ])

    fake_slips = [
        ("PRIZEPICKS", 2, fake_legs, 0.999, "A", "PENDING", now),
        ("UNDERDOG", 2, fake_legs, 0.999, "A", "PENDING", now),
        ("SPORTSBOOK_PARLAY", 2, fake_legs, 0.999, "A", "PENDING", now)
    ]

    conn.executemany(
        "INSERT INTO slips (platform, leg_count, legs_json, implied_probability, confidence_tier, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)", 
        fake_slips
    )
    print("✅ Tracer Slips Injected (PrizePicks, Underdog, Parlay).")

    conn.commit()
    conn.close()
    print("="*55 + "\n")

except Exception as e:
    print(f"❌ Tracer injection failed: {e}")