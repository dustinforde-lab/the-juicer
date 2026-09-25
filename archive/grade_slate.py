import sqlite3
import os
import json
import random
from datetime import datetime, timezone
from recommendation_engine import RecommendationEngine

DB_PATH = os.path.join(os.getcwd(), "action_grid.db")

def mock_actual_outcomes(conn):
    """Simulates actual game outcomes from a live stat provider to test the grading loop."""
    cur = conn.execute("SELECT player_name, COALESCE(projected_fp, ppr_baseline, 0) FROM player_rankings")
    outcomes = {}
    for name, proj in cur:
        # Simulate actual performance with variance
        outcomes[name] = round(max(0, proj + random.uniform(-10.0, 15.0)), 1)
    return outcomes

def run_automated_grading():
    print("\n" + "="*55)
    print("⚖️ THE JUICER: AUTOMATED SLATE GRADING")
    print("="*55)
    
    conn = sqlite3.connect(DB_PATH)
    engine = RecommendationEngine(conn)
    actuals = mock_actual_outcomes(conn)
    
    # 1. Grade canonical DFS lineups, with legacy fallback support.
    tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    if "dfs_rosters" in tables:
        conn.execute("ALTER TABLE dfs_rosters ADD COLUMN actual_score REAL") if "actual_score" not in {row[1] for row in conn.execute("PRAGMA table_info(dfs_rosters)")} else None
        conn.execute("ALTER TABLE dfs_rosters ADD COLUMN graded_at TEXT") if "graded_at" not in {row[1] for row in conn.execute("PRAGMA table_info(dfs_rosters)")} else None
        dfs_lineups = conn.execute("SELECT roster_id, qb, rb1, rb2, wr1, wr2, wr3, te, flex, dst, projected_score FROM dfs_rosters WHERE graded_at IS NULL").fetchall()
        dfs_legacy = False
    elif "dfs_classic_lineups" in tables:
        dfs_lineups = conn.execute("SELECT id, roster_json FROM dfs_classic_lineups WHERE graded_at IS NULL").fetchall()
        dfs_legacy = True
    else:
        dfs_lineups = []
        dfs_legacy = False
    
    dfs_hits = 0
    for lineup in dfs_lineups:
        try:
            if dfs_legacy:
                l_id, roster_json = lineup
                roster = json.loads(roster_json)
                actual_pts = sum(actuals.get(p.get("name", ""), 0) for p in roster)
                result = engine.grade_dfs_lineup(l_id, actual_pts)
            else:
                l_id, *players, projected_pts = lineup
                actual_pts = sum(actuals.get(player, 0) for player in players)
                hit_flag = int(actual_pts >= projected_pts)
                graded_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
                conn.execute("UPDATE dfs_rosters SET actual_score = ?, graded_at = ? WHERE roster_id = ?", (actual_pts, graded_at, l_id))
                conn.execute("INSERT INTO bet_grading (source, reference_id, predicted_value, actual_value, hit_flag, created_at, graded_at) VALUES ('DFS', ?, ?, ?, ?, ?, ?)", (l_id, projected_pts, actual_pts, hit_flag, graded_at, graded_at))
                result = type("Result", (), {"hit_flag": hit_flag})()
            if result.hit_flag == 1:
                dfs_hits += 1
        except Exception as e:
            continue
            
    print(f"✅ Graded {len(dfs_lineups)} DFS Lineups ({dfs_hits} exceeded projections).")

    # 2. Grade PrizePicks/Underdog Slips
    slips_cur = conn.execute("SELECT id, legs_json FROM slips WHERE status = 'PENDING'")
    slips = slips_cur.fetchall()
    
    slip_hits = 0
    for s_id, legs_json in slips:
        try:
            legs = json.loads(legs_json)
            leg_outcomes = [(leg["player_name"], actuals.get(leg["player_name"], 0)) for leg in legs]
            result = engine.grade_slip(s_id, leg_outcomes)
            if result.hit_flag == 1: slip_hits += 1
        except Exception as e:
            continue
            
    print(f"✅ Graded {len(slips)} Pick'em Slips ({slip_hits} fully cashed).")
    
    conn.close()
    
    # 3. Trigger Learning Loop Recalibration
    print("🧠 System writing delta errors to bet_grading matrix...")
    try:
        import learning_loop
        print(f"  ✓ {learning_loop.recalculate_weights()}")
    except Exception as exc:
        print(f"  ! Learning loop deferred: {exc}")
        
    print("="*55 + "\n")

if __name__ == "__main__":
    run_automated_grading()