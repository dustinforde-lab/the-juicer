import sqlite3
import os
import pulp
from recommendation_engine import RecommendationEngine

DB_PATH = os.path.join(os.getcwd(), "action_grid.db")

def run_multi_ilp(num_lineups=200, max_exposure=0.35):
    conn = sqlite3.connect(DB_PATH)
    engine = RecommendationEngine(conn)
    
    # Flush legacy lineups so we start fresh
    conn.execute("DELETE FROM dfs_classic_lineups")
    conn.commit()
    
    cur = conn.execute("SELECT player_name, pos, team, projected_fp FROM player_rankings")
    players = []
    for row in cur:
        # Mock salary for demo purposes based on projected FP
        sal = int(row[3] * 300) 
        players.append({"name": row[0], "pos": row[1], "team": row[2], "fp": row[3], "salary": sal})
        
    if not players: return
        
    print("\n" + "="*55)
    print(f"🧮 THE JUICER: MULTI-ILP OPTIMIZER ({num_lineups} Lineups)")
    print("="*55)

    prob = pulp.LpProblem("DFS_Optimization", pulp.LpMaximize)
    player_vars = {p["name"]: pulp.LpVariable(f"var_{i}", cat="Binary") for i, p in enumerate(players)}
    
    # Objective
    prob += pulp.lpSum([p["fp"] * player_vars[p["name"]] for p in players])
    
    # Base DFS Constraints
    prob += pulp.lpSum([player_vars[p["name"]] for p in players]) == 9
    prob += pulp.lpSum([p["salary"] * player_vars[p["name"]] for p in players]) <= 50000
    prob += pulp.lpSum([player_vars[p["name"]] for p in players if p["pos"] == "QB"]) == 1
    prob += pulp.lpSum([player_vars[p["name"]] for p in players if p["pos"] == "RB"]) >= 2
    prob += pulp.lpSum([player_vars[p["name"]] for p in players if p["pos"] == "RB"]) <= 3
    prob += pulp.lpSum([player_vars[p["name"]] for p in players if p["pos"] == "WR"]) >= 3
    prob += pulp.lpSum([player_vars[p["name"]] for p in players if p["pos"] == "WR"]) <= 4
    prob += pulp.lpSum([player_vars[p["name"]] for p in players if p["pos"] == "TE"]) >= 1
    prob += pulp.lpSum([player_vars[p["name"]] for p in players if p["pos"] == "TE"]) <= 2
    prob += pulp.lpSum([player_vars[p["name"]] for p in players if p["pos"] == "DST"]) == 1
    
    exposure_limit = int(num_lineups * max_exposure)
    player_counts = {p["name"]: 0 for p in players}
    
    generated = 0
    print("⚙️ Solving for unique lineups...")
    
    for i in range(num_lineups):
        pulp.PULP_CBC_CMD(msg=0).solve(prob)
        
        if pulp.LpStatus[prob.status] != 'Optimal':
            print(f"⚠️ Exhausted optimal combinations after {generated} lineups.")
            break
            
        roster = []
        total_pts = 0
        for p in players:
            if player_vars[p["name"]].varValue == 1.0:
                roster.append(p)
                total_pts += p["fp"]
                player_counts[p["name"]] += 1
                
        if not roster: break
            
        formatted_roster = [{"pos": p["pos"], "name": p["name"]} for p in roster]
        lineup_type = "CASH_DK" if generated < 50 else "GPP_MULTI"
        engine.record_dfs_lineup(lineup_type, total_pts, formatted_roster)
        generated += 1
        
        # 1. Uniqueness Constraint
        prob += pulp.lpSum([player_vars[p["name"]] for p in roster]) <= 8
        
        # 2. Dynamic Exposure Constraint
        for p in roster:
            if player_counts[p["name"]] >= exposure_limit:
                prob += player_vars[p["name"]] == 0
                
    conn.close()
    print(f"✅ Successfully exported {generated} optimal, unique lineups to DB.")
    print("="*55 + "\n")

if __name__ == "__main__":
    run_multi_ilp()