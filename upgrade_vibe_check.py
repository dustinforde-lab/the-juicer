import sqlite3
from datetime import datetime

DB_FILE = "action_grid.db"

# Simulated DFS Ownership & Chalk Feed
CHALK_FEED = [
    {"player": "Christian McCaffrey", "team": "SF", "ownership": "34.5%", "vibe": "MEGA CHALK"},
    {"player": "CeeDee Lamb", "team": "DAL", "ownership": "28.2%", "vibe": "HEAVY CHALK"},
    {"player": "Bo Nix", "team": "DEN", "ownership": "2.1%", "vibe": "CONTRARIAN"},
    {"player": "Malik Nabers", "team": "NYG", "ownership": "4.5%", "vibe": "LEVERAGE PLAY"}
]

def deploy_vibe_check():
    print("=" * 65)
    print("📉 [UPGRADE CHUNK 14] Deploying Donna's Vibe Check (Ownership Scrape)...")
    print("=" * 65)
    
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ownership_projections (
                player_name TEXT PRIMARY KEY, team TEXT,
                projected_ownership TEXT, vibe_rating TEXT, updated_at TEXT
            )
        """)
        
        cur.execute("DELETE FROM ownership_projections")
        now_ts = datetime.now().strftime("%Y-%m-%d %I:%M %p ET")
        
        for p in CHALK_FEED:
            cur.execute("INSERT INTO ownership_projections VALUES (?, ?, ?, ?, ?)",
                        (p["player"], p["team"], p["ownership"], p["vibe"], now_ts))
            
            # Donna broadcasts the ownership directly to the UI Ticker
            action = "AVOID IN GPP" if "CHALK" in p["vibe"] else "BOOST IN GPP"
            cur.execute("INSERT INTO agent_chatter (sender, directive, target, action, timestamp) VALUES (?, ?, ?, ?, ?)",
                        ("Donna", f"Ownership: {p['ownership']}", p["player"], action, now_ts))
            
            print(f"   • [VIBE CHECK] {p['player']} ({p['team']}) -> {p['ownership']} ({p['vibe']})")
            
        conn.commit()

def run_self_test():
    print("\n🧪 [SELF-CHECK GATE] Auditing Ownership Database & Telemetry Routing...")
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        rows = cur.execute("SELECT * FROM ownership_projections").fetchall()
        assert len(rows) == len(CHALK_FEED), "Integrity Failure: Ownership data failed to save."
        
        chatter = [r[0] for r in cur.execute("SELECT sender FROM agent_chatter").fetchall()]
        assert "Donna" in chatter, "Telemetry Failure: Donna's vibe checks didn't hit the hub."
        
    print("✅ VIBE CHECK ONLINE: Ownership projections locked and broadcasting to UI.\n")

if __name__ == "__main__":
    deploy_vibe_check()
    run_self_test()
