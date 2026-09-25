import sqlite3
import os

DB_PATH = os.path.join(os.getcwd(), "action_grid.db")

def run_projection_engine():
    print("\n" + "="*55)
    print("🧠 THE JUICER: VEGAS BLENDING & RANGE PROJECTIONS")
    print("="*55)
    
    conn = sqlite3.connect(DB_PATH)
    
    # Positional variance mapping for Floor (10th percentile) and Ceiling (90th percentile)
    volatility = {
        "QB": 0.20,
        "RB": 0.25,
        "WR": 0.35,  # Higher variance for WRs (boom/bust)
        "TE": 0.40,
        "FLEX": 0.30,
        "DST": 0.50
    }
    
    # DFS Scoring approximations for Vegas lines
    scoring_weights = {
        "PASS_YDS": 0.04,
        "PASS_TD": 4.0,
        "RUSH_YDS": 0.10,
        "REC_YDS": 0.10,
        "REC": 1.0
    }
    
    cur = conn.execute("SELECT id, player_name, pos, team, projected_fp, consensus_line, stat_category, matchup_multiplier FROM player_rankings")
    players = cur.fetchall()
    
    updates = []
    for row in players:
        p_id, name, pos, team, baseline_fp, line, stat_cat, matchup = row
        matchup = matchup if matchup else 1.0
        
        # 1. Vegas-Implied Blending
        if line and stat_cat in scoring_weights:
            vegas_implied_pts = line * scoring_weights[stat_cat]
            # Blend Vegas primary prop with the rest of the player's baseline expectation
            blended_median = (vegas_implied_pts * 0.6) + (baseline_fp * 0.4)
        else:
            blended_median = baseline_fp
            
        # 2. Matchup Adjustment
        final_median = blended_median * matchup
        
        # 3. Calculate Floor and Ceiling
        var = volatility.get(pos, 0.30)
        floor_fp = final_median * (1 - var)
        ceiling_fp = final_median * (1 + var)
        
        updates.append((
            round(final_median, 2), # Overwrite projected_fp with new blended median
            round(floor_fp, 2),
            round(final_median, 2),
            round(ceiling_fp, 2),
            p_id
        ))
        
    conn.executemany("UPDATE player_rankings SET projected_fp=?, floor_fp=?, median_fp=?, ceiling_fp=? WHERE id=?", updates)
    conn.commit()
    conn.close()
    
    print(f"✅ Evaluated and generated Floor/Median/Ceiling ranges for {len(players)} players.")
    print("="*55 + "\n")

if __name__ == "__main__":
    run_projection_engine()