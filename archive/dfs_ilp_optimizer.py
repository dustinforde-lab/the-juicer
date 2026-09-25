import sqlite3
import os
import pulp
from recommendation_engine import RecommendationEngine

DB_PATH = os.path.join(os.getcwd(), "action_grid.db")

def run_ilp_optimizer():
    conn = sqlite3.connect(DB_PATH)
    engine = RecommendationEngine(conn)
    
    # 1. Fetch data
    cur = conn.execute("SELECT player_name, pos, team, projected_fp FROM player_rankings")
    players = []
    for row in cur:
        # Mock salary for demo purposes based on projected FP
        sal = int(row[3] * 300) 
        players.append({"name": row[0], "pos": row[1], "team": row[2], "fp": row[3], "salary": sal})
        
    if not players:
        return
        
    print("\n" + "="*55)
    print("🧮 THE JUICER: PuLP INTEGER LINEAR OPTIMIZER")
    print("="*55)

    prob = pulp.LpProblem("DFS_Optimization", pulp.LpMaximize)
    
    # Variables
    player_vars = {p["name"]: pulp.LpVariable(f"var_{i}", cat="Binary") for i, p in enumerate(players)}
    
    # Objective
    prob += pulp.lpSum([p["fp"] * player_vars[p["name"]] for p in players])
    
    # Constraints
    prob += pulp.lpSum([player_vars[p["name"]] for p in players]) == 9 # Exactly 9 players
    prob += pulp.lpSum([p["salary"] * player_vars[p["name"]] for p in players]) <= 50000 # Salary Cap
    
    # Position limits
    prob += pulp.lpSum([player_vars[p["name"]] for p in players if p["pos"] == "QB"]) == 1
    prob += pulp.lpSum([player_vars[p["name"]] for p in players if p["pos"] == "RB"]) >= 2
    prob += pulp.lpSum([player_vars[p["name"]] for p in players if p["pos"] == "RB"]) <= 3
    prob += pulp.lpSum([player_vars[p["name"]] for p in players if p["pos"] == "WR"]) >= 3
    prob += pulp.lpSum([player_vars[p["name"]] for p in players if p["pos"] == "WR"]) <= 4
    prob += pulp.lpSum([player_vars[p["name"]] for p in players if p["pos"] == "TE"]) >= 1
    prob += pulp.lpSum([player_vars[p["name"]] for p in players if p["pos"] == "TE"]) <= 2
    prob += pulp.lpSum([player_vars[p["name"]] for p in players if p["pos"] == "DST"]) == 1
    
    # Solve
    pulp.PULP_CBC_CMD(msg=0).solve(prob)
    
    roster = []
    total_pts = 0
    for p in players:
        if player_vars[p["name"]].varValue == 1.0:
            roster.append({"pos": p["pos"], "name": p["name"]})
            total_pts += p["fp"]
            
    if roster:
        lineup_id = engine.record_dfs_lineup("GPP_MULTI", total_pts, roster)
        print(f"✅ Generated Optimal ILP Lineup (ID: {lineup_id} | Proj: {total_pts:.2f} FP)")
        
    conn.close()
    print("="*55 + "\n")

if __name__ == "__main__":
    run_ilp_optimizer()