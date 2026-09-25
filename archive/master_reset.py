import sqlite3
import json
import datetime

print("🔄 [MASTER RESET] Rebuilding production database baseline...")
db_path = "action_grid.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Cleanly drop and recreate theoretical_bets with exact UI-compatible schema
cursor.execute("DROP TABLE IF EXISTS theoretical_bets;")
cursor.execute("""
    CREATE TABLE theoretical_bets (
        ticket_id TEXT PRIMARY KEY,
        weight_class TEXT,
        odds TEXT,
        border_color TEXT,
        ticket_json TEXT,
        created_at TEXT,
        confidence_score INTEGER
    )
""")

# 2. Populate fresh slips across the 3 distinct tiers
now = str(datetime.datetime.now())

for i in range(1, 11):
    # Cash Builder Tier
    cursor.execute("INSERT OR REPLACE INTO theoretical_bets VALUES (?, ?, ?, ?, ?, ?, ?)", 
                   (f"SLIP-CB-{i:02d}", "Cash Builder", f"+{100 + i*5}", "#00ff88", 
                    json.dumps([{"player": f"Starter Prop {i}", "team": "NFL", "stat": "Over Line Hit"}]), now, 88))
    
    # Syndicate Core Tier
    cursor.execute("INSERT OR REPLACE INTO theoretical_bets VALUES (?, ?, ?, ?, ?, ?, ?)", 
                   (f"SLIP-SC-{i:02d}", "Syndicate Core", f"+{400 + i*25}", "#00e5ff", 
                    json.dumps([{"player": f"Core Alpha {i}", "team": "NFL", "stat": "Leg 1"}, {"player": f"Core Beta {i}", "team": "NFL", "stat": "Leg 2"}]), now, 82))
    
    # Moonshot Whale Tier
    cursor.execute("INSERT OR REPLACE INTO theoretical_bets VALUES (?, ?, ?, ?, ?, ?, ?)", 
                   (f"SLIP-MW-{i:02d}", "Moonshot Whale", f"+{1200 + i*100}", "#ff00ff", 
                    json.dumps([{"player": f"Whale Bomb {i}", "team": "NFL", "stat": "Deep Stat 1"}, {"player": f"Whale Target {i}", "team": "NFL", "stat": "Deep Stat 2"}]), now, 74))

conn.commit()
conn.close()
print("✨ MASTER RESET COMPLETE: Clean baseline established with 3 active tiers ready for the web UI!")
