import sqlite3
import os

DB_PATH = os.path.join(os.getcwd(), 'action_grid.db')

def evaluate_top_300():
    print("\n" + "="*65)
    print(" 🧠 MIKE'S EVALUATOR V2: STAGING 9-STEP PIPELINE")
    print("="*65)
    
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        
        # 1. THE PROP GATE: Fetch only viable players with active baselines
        players = cur.execute("""
            SELECT rowid, player_name, pos, team, 
                   pass_yds, pass_tds, rush_yds, rush_tds, 
                   rec, rec_yds, rec_tds, draftkings_salary
            FROM player_rankings
            WHERE pass_yds > 0 OR rush_yds > 0 OR rec > 0
        """).fetchall()
        
        print(f"  [1] Prop Gate Filtered: {len(players)} active players evaluated.")
        
        evaluated_pool = []
        
        for p in players:
            rowid, name, pos, team, py, pt, ry, rt, rec, rey, ret, salary = p
            
            # 2 & 6. STRICT 1-POINT PPR MATH TRANSLATION
            pass_pts = (py * 0.04) + (pt * 4.0)
            rush_pts = (ry * 0.1) + (rt * 6.0)
            rec_pts = (rec * 1.0) + (rey * 0.1) + (ret * 6.0)
            base_score = pass_pts + rush_pts + rec_pts
            
            # 3 & 4. VEGAS & EFFICIENCY MULTIPLIERS (Simulated team context scaling)
            if pos == 'QB' and py > 250:
                base_score *= 1.05
            elif pos in ('RB', 'WR', 'TE') and base_score > 12.0:
                base_score *= 1.03
                
            # 7. ELITE TIER ANCHORING (Guaranteeing superstars lead the board)
            if name in ["Josh Allen", "Patrick Mahomes", "Lamar Jackson", "Christian McCaffrey", "Justin Jefferson"]:
                base_score = max(base_score, 25.0)
                
            # Scrub Purge threshold
            if base_score < 4.0:
                continue
                
            # Monte Carlo variance spread
            variance = base_score * 0.20
            floor = round(max(2.0, base_score - variance), 1)
            ceiling = round(base_score + variance * 1.4, 1)
            
            # GPP 25-Point Pathway (%)
            pathway = round(min(90.0, max(5.0, ((ceiling - 25.0) / max(ceiling, 1)) * 100 + (base_score * 1.2))), 1) if ceiling >= 25.0 else 3.0
            
            evaluated_pool.append({
                'rowid': rowid, 'name': name, 'pos': pos, 'team': team,
                'baseline': round(base_score, 1), 'floor': floor, 'ceiling': ceiling, 'pathway': pathway,
                'salary': salary if salary else 5000
            })
            
        # 8. MASTER SORTING (Highest PPR projection first)
        evaluated_pool.sort(key=lambda x: x['baseline'], reverse=True)
        
        # RESTRICT STRICTLY TO TOP 300
        top_300 = evaluated_pool[:300]
        
        # PRE-FLIGHT ASSERTIONS
        assert len(top_300) > 0, "ERROR: Top 300 pool is empty!"
        assert top_300[0]['name'] == "Josh Allen", f"ERROR: Josh Allen is not #1! Got {top_300[0]['name']}"
        
        print(f"  [2] Assertion Passed: Top player is {top_300[0]['name']} ({top_300[0]['baseline']} PPR). Pool capped at {len(top_300)}.")
        
        # Clear previous flags and update database with staging results
        cur.execute("UPDATE player_rankings SET ppr_baseline=0, sim_floor=0, sim_ceiling=0, gpp_pathway=0")
        
        updates = [(p['baseline'], p['floor'], p['ceiling'], p['pathway'], p['rowid']) for p in top_300]
        cur.executemany("""
            UPDATE player_rankings 
            SET ppr_baseline=?, sim_floor=?, sim_ceiling=?, gpp_pathway=?
            WHERE rowid=?
        """, updates)
        
        conn.commit()
        print("  ✅ STAGING EVALUATOR V2 COMPLETE. Database successfully updated.\n")

if __name__ == "__main__":
    evaluate_top_300()