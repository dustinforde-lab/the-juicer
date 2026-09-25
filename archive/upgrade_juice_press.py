import sqlite3
from datetime import datetime

DB_FILE = "action_grid.db"

# Simulated Sharp API Feed (Comparing Pinnacle Sharp Odds vs DraftKings Soft Odds)
SHARP_MARKET_FEED = [
    {"player": "Javonte Williams", "stat": "Rush Yds > 62.5", "sharp_odds": -145, "soft_odds": -110, "edge": "+12.5%"},
    {"player": "Deebo Samuel", "stat": "Anytime TD", "sharp_odds": -130, "soft_odds": +115, "edge": "+9.2%"},
    {"player": "Courtland Sutton", "stat": "Rec Yds > 54.5", "sharp_odds": -120, "soft_odds": -105, "edge": "+4.1%"}
]

def deploy_juice_press():
    print("=" * 65)
    print("📈 [UPGRADE CHUNK 9] Deploying 'The Juice Press' Sharp Feed...")
    print("=" * 65)
    
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sharp_market_lines (
                player_name TEXT PRIMARY KEY,
                stat_target TEXT,
                sharp_odds INTEGER,
                soft_odds INTEGER,
                ev_edge TEXT,
                updated_at TEXT
            )
        """)
        
        cur.execute("DELETE FROM sharp_market_lines")
        now_ts = datetime.now().strftime("%Y-%m-%d %I:%M %p ET")
        
        for edge in SHARP_MARKET_FEED:
            cur.execute("INSERT INTO sharp_market_lines VALUES (?, ?, ?, ?, ?, ?)",
                        (edge["player"], edge["stat"], edge["sharp_odds"], edge["soft_odds"], edge["edge"], now_ts))
            
            print(f"   • [+EV FOUND] {edge['player']} ({edge['stat']}) | Sharp: {edge['sharp_odds']} vs Soft: {edge['soft_odds']} -> Edge: {edge['edge']}")
            
        conn.commit()

def run_self_test():
    print("\n🧪 [SELF-CHECK GATE] Auditing Sharp Market Database...")
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        rows = cur.execute("SELECT * FROM sharp_market_lines").fetchall()
        assert len(rows) == len(SHARP_MARKET_FEED), "Integrity Failure: Sharp lines failed to save."
    print("✅ JUICE PRESS ONLINE: Positive EV market edges locked and loaded.\n")

if __name__ == "__main__":
    deploy_juice_press()
    run_self_test()
