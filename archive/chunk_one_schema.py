import sqlite3
import os

DB_PATH = os.path.join(os.getcwd(), "action_grid.db")

print("\n" + "="*60)
print(" 🏗️ CHUNK 1: DATABASE SCHEMA EXPANSION & NFL ANCHOR")
print("="*60)

def run_schema_upgrade():
    if not os.path.exists(DB_PATH):
        print("  [!] Error: action_grid.db not found.")
        return

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        
        # 1. UPGRADE PLAYER RANKINGS (Granular Stats for Mike)
        print("  [1/3] Expanding player_rankings for granular stats...")
        cur.execute("PRAGMA table_info(player_rankings)")
        existing_cols = [c[1] for c in cur.fetchall()]
        
        granular_cols = ['pass_yds', 'pass_tds', 'rush_yds', 'rush_tds', 'rec', 'rec_yds', 'rec_tds']
        for col in granular_cols:
            if col not in existing_cols:
                cur.execute(f"ALTER TABLE player_rankings ADD COLUMN {col} REAL DEFAULT 0.0")
                
        # 2. UPGRADE DFS ROSTERS (Cash vs GPP Toggle & DST)
        print("  [2/3] Upgrading DFS tables for Cash/GPP formats...")
        cur.execute("PRAGMA table_info(dfs_rosters)")
        dfs_cols = [c[1] for c in cur.fetchall()]
        
        if 'lineup_type' not in dfs_cols:
            cur.execute("ALTER TABLE dfs_rosters ADD COLUMN lineup_type TEXT DEFAULT 'GPP'")
        if 'dst' not in dfs_cols:
            cur.execute("ALTER TABLE dfs_rosters ADD COLUMN dst TEXT")
            
        # 3. INJECT ALL 32 NFL DEFENSES
        print("  [3/3] Injecting the full 32-team NFL Defense matrix...")
        dst_matrix = [
            ("49ers Defense", "DST", "SF"), ("Ravens Defense", "DST", "BAL"), ("Jets Defense", "DST", "NYJ"),
            ("Cowboys Defense", "DST", "DAL"), ("Browns Defense", "DST", "CLE"), ("Steelers Defense", "DST", "PIT"),
            ("Bills Defense", "DST", "BUF"), ("Dolphins Defense", "DST", "MIA"), ("Patriots Defense", "DST", "NE"),
            ("Broncos Defense", "DST", "DEN"), ("Chiefs Defense", "DST", "KC"), ("Raiders Defense", "DST", "LV"),
            ("Chargers Defense", "DST", "LAC"), ("Texans Defense", "DST", "HOU"), ("Colts Defense", "DST", "IND"),
            ("Jaguars Defense", "DST", "JAX"), ("Titans Defense", "DST", "TEN"), ("Bengals Defense", "DST", "CIN"),
            ("Bears Defense", "DST", "CHI"), ("Lions Defense", "DST", "DET"), ("Packers Defense", "DST", "GB"),
            ("Vikings Defense", "DST", "MIN"), ("Falcons Defense", "DST", "ATL"), ("Panthers Defense", "DST", "CAR"),
            ("Saints Defense", "DST", "NO"), ("Buccaneers Defense", "DST", "TB"), ("Cardinals Defense", "DST", "ARI"),
            ("Rams Defense", "DST", "LAR"), ("Seahawks Defense", "DST", "SEA"), ("Eagles Defense", "DST", "PHI"),
            ("Giants Defense", "DST", "NYG"), ("Commanders Defense", "DST", "WAS")
        ]
        
        for dst in dst_matrix:
            cur.execute("""
                INSERT OR IGNORE INTO player_rankings (player_name, pos, team) 
                VALUES (?, ?, ?)
            """, dst)
            
        # DIAGNOSTIC CHECK
        pr_cols = cur.execute("PRAGMA table_info(player_rankings)").fetchall()
        dst_count = cur.execute("SELECT COUNT(*) FROM player_rankings WHERE pos = 'DST'").fetchone()[0]
        
        print("\n  ✅ CHUNK 1 COMPLETE.")
        print(f"  -> Granular stat columns verified: {len(pr_cols)} total columns.")
        print(f"  -> Active NFL Defenses in pool: {dst_count}/32")

if __name__ == "__main__":
    run_schema_upgrade()
print("="*60 + "\n")