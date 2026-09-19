import sqlite3
from datetime import datetime

DB_FILE = "action_grid.db"

# Simulated Weather API Feed
LIVE_WEATHER_FEED = [
    {"game": "DAL vs NYG", "wind_mph": 22, "condition": "High Winds", "action": "Fade Passing"},
    {"game": "SF vs LAR", "wind_mph": 4, "condition": "Clear Dome", "action": "None"},
    {"game": "KC vs LAC", "wind_mph": 8, "condition": "Light Rain", "action": "None"},
    {"game": "DEN vs LV", "wind_mph": 14, "condition": "Heavy Snow", "action": "Boost Rushing"}
]

def deploy_meteorologist():
    print("=" * 65)
    print("🌪️ [UPGRADE CHUNK 8] Deploying 'The Meteorologist' Weather Feed...")
    print("=" * 65)
    
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS stadium_weather (
                game_matchup TEXT PRIMARY KEY,
                wind_mph INTEGER,
                condition TEXT,
                agent_action TEXT,
                updated_at TEXT
            )
        """)
        
        cur.execute("DELETE FROM stadium_weather")
        now_ts = datetime.now().strftime("%Y-%m-%d %I:%M %p ET")
        
        for w in LIVE_WEATHER_FEED:
            cur.execute("INSERT INTO stadium_weather VALUES (?, ?, ?, ?, ?)",
                        (w["game"], w["wind_mph"], w["condition"], w["action"], now_ts))
            
            alert = f"⚠️ ALERT: {w['action']}" if w["action"] != "None" else "✅ Clear"
            print(f"   • [WEATHER] {w['game']}: {w['wind_mph']}mph | {w['condition']} -> {alert}")
            
        conn.commit()

def run_self_test():
    print("\n🧪 [SELF-CHECK GATE] Auditing Weather Database...")
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        rows = cur.execute("SELECT * FROM stadium_weather WHERE wind_mph >= 18").fetchall()
        assert len(rows) > 0, "Integrity Failure: High wind alerts failed to log."
    print("✅ METEOROLOGIST ONLINE: Weather conditions mapped and active.\n")

if __name__ == "__main__":
    deploy_meteorologist()
    run_self_test()
