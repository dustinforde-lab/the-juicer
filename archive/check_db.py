import sqlite3
import os

db_path = "action_grid.db"
print("\n" + "="*50)
print(" 🔍 DATABASE STATE REPORT")
print("="*50)

if not os.path.exists(db_path):
    print("Database not found at expected path!")
else:
    try:
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            
            # 1. Check Row Counts
            dfs_count = cur.execute("SELECT COUNT(*) FROM dfs_rosters").fetchone()[0]
            slips_count = cur.execute("SELECT COUNT(*) FROM slips").fetchone()[0]
            pr_count = cur.execute("SELECT COUNT(*) FROM player_rankings").fetchone()[0]
            dst_count = cur.execute("SELECT COUNT(*) FROM player_rankings WHERE pos = 'DST'").fetchone()[0]
            
            print(f"  dfs_rosters rows:       {dfs_count}")
            print(f"  slips rows:             {slips_count}")
            print(f"  player_rankings total:  {pr_count}")
            print(f"  DSTs in pool:           {dst_count}")
            
            # 2. Check Schema
            cur.execute("PRAGMA table_info(dfs_rosters)")
            cols = [c[1] for c in cur.fetchall()]
            print(f"\n  dfs_rosters columns:")
            print(f"  {cols}")
            
            # 3. Check for Positional completeness in player_rankings
            positions = cur.execute("SELECT pos, COUNT(*) FROM player_rankings GROUP BY pos").fetchall()
            print(f"\n  Positional Breakdown:")
            for pos, count in positions:
                print(f"  - {pos}: {count}")
                
    except Exception as e:
        print(f"  ⚠️ Error querying database: {e}")

print("="*50 + "\n")