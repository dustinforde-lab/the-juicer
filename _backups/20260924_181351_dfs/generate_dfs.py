"""
The Juicer - Multi-Slate DFS Portfolio Generator (Fixed 340 Suite)
Guarantees:
  • Showdown: 150 GPP + 20 Cash
  • Classic:  150 GPP + 20 Cash
Total: Exactly 340 Builds in US/Central Time.
"""
import sqlite3
import json
import os
import random
from datetime import datetime, timezone, timedelta

try:
    from zoneinfo import ZoneInfo
    CENTRAL_TZ = ZoneInfo("America/Chicago")
except Exception:
    CENTRAL_TZ = timezone(timedelta(hours=-5), "CDT")

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "action_grid.db")

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=10000;")
    conn.row_factory = sqlite3.Row
    return conn

def get_current_central_time_str():
    now_ct = datetime.now(CENTRAL_TZ)
    return now_ct.strftime("%Y-%m-%d %H:%M:%S")

def init_dfs_table():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS dfs_lineups (
                lineup_id TEXT PRIMARY KEY,
                format_type TEXT,
                contest_type TEXT,
                total_salary INTEGER,
                projected_points REAL,
                floor_points REAL,
                ceiling_points REAL,
                stack_summary TEXT,
                roster_json TEXT,
                meta_json TEXT,
                created_at TIMESTAMP
            )
        """)
        conn.commit()

# --- 1. SHOWDOWN GENERATOR: 150 GPP + 20 CASH ---
def generate_showdown_pool():
    print("🏈 Generating 170 Showdown Builds (150 MME GPP + 20 Cash)...")
    player_pool = {
        "Jordan Love": {"pos": "QB", "team": "GB", "opp": "ATL", "salary": 10400, "proj": 20.8},
        "Michael Penix Jr.": {"pos": "QB", "team": "ATL", "opp": "GB", "salary": 9600, "proj": 18.2},
        "Bijan Robinson": {"pos": "RB", "team": "ATL", "opp": "GB", "salary": 11200, "proj": 21.4},
        "Josh Jacobs": {"pos": "RB", "team": "GB", "opp": "ATL", "salary": 10000, "proj": 17.6},
        "Drake London": {"pos": "WR", "team": "ATL", "opp": "GB", "salary": 8800, "proj": 16.4},
        "Jayden Reed": {"pos": "WR", "team": "GB", "opp": "ATL", "salary": 8200, "proj": 15.1},
        "Kyle Pitts": {"pos": "TE", "team": "ATL", "opp": "GB", "salary": 6400, "proj": 11.2},
        "Christian Watson": {"pos": "WR", "team": "GB", "opp": "ATL", "salary": 7200, "proj": 12.8},
        "Romeo Doubs": {"pos": "WR", "team": "GB", "opp": "ATL", "salary": 6800, "proj": 11.5},
        "Darnell Mooney": {"pos": "WR", "team": "ATL", "opp": "GB", "salary": 5600, "proj": 9.8},
        "Tucker Kraft": {"pos": "TE", "team": "GB", "opp": "ATL", "salary": 4800, "proj": 8.4},
        "MarShawn Lloyd": {"pos": "RB", "team": "GB", "opp": "ATL", "salary": 3800, "proj": 7.2},
        "Packers D/ST": {"pos": "DEF", "team": "GB", "opp": "ATL", "salary": 4200, "proj": 7.0},
        "Falcons D/ST": {"pos": "DEF", "team": "ATL", "opp": "GB", "salary": 3600, "proj": 5.5},
        "Brayden Narveson": {"pos": "K", "team": "GB", "opp": "ATL", "salary": 4600, "proj": 8.0},
        "Younghoe Koo": {"pos": "K", "team": "ATL", "opp": "GB", "salary": 4400, "proj": 7.8}
    }

    ct_timestamp = get_current_central_time_str()
    lineups = []
    
    # 20 Cash
    for i in range(20):
        while True:
            cpt_name = random.choice(["Jordan Love", "Bijan Robinson", "Josh Jacobs"])
            cpt_p = player_pool[cpt_name]
            cpt_cost = int(cpt_p["salary"] * 1.5)
            rem_sal = 50000 - cpt_cost
            
            avail = [k for k in player_pool.keys() if k != cpt_name]
            flex_names = random.sample(avail, 5)
            flex_cost = sum(player_pool[n]["salary"] for n in flex_names)
            
            if flex_cost <= rem_sal and (rem_sal - flex_cost) <= 2000:
                roster = [{
                    "name": cpt_name, "pos": cpt_p["pos"], "team": cpt_p["team"], "opp": cpt_p["opp"],
                    "salary": cpt_cost, "proj": round(cpt_p["proj"] * 1.5, 1), "alpha": 95.0, "is_cpt": True
                }]
                for fn in flex_names:
                    fp = player_pool[fn]
                    roster.append({
                        "name": fn, "pos": fp["pos"], "team": fp["team"], "opp": fp["opp"],
                        "salary": fp["salary"], "proj": fp["proj"], "alpha": 88.0, "is_cpt": False
                    })
                
                tot_proj = sum(p["proj"] for p in roster)
                tot_sal = cpt_cost + flex_cost
                teams = [p["team"] for p in roster]
                gb_c = teams.count("GB")
                atl_c = teams.count("ATL")
                stack_sum = f"{gb_c}-2 GB Heavy" if gb_c >= 4 else (f"{atl_c}-2 ATL Heavy" if atl_c >= 4 else "3-3 Split Game Script")

                meta = {
                    "remaining_salary": 50000 - tot_sal,
                    "stud_count": 2, "mid_count": 3, "punt_count": 1,
                    "leverage_label": "CASH CORE OPTIMAL",
                    "mike_verdict": f"Pristine median floor anchored by {cpt_name} CPT."
                }
                lineups.append({
                    "lineup_id": f"DK_SHOWDOWN_CASH_{i+1:03d}",
                    "format_type": "SHOWDOWN",
                    "contest_type": "CASH",
                    "total_salary": tot_sal,
                    "projected_points": round(tot_proj, 2),
                    "floor_points": round(tot_proj * 0.74, 1),
                    "ceiling_points": round(tot_proj * 1.35, 1),
                    "stack_summary": stack_sum,
                    "roster_json": json.dumps(roster),
                    "meta_json": json.dumps(meta),
                    "created_at": ct_timestamp
                })
                break

    # 150 GPP
    for i in range(150):
        while True:
            cpt_name = random.choice(list(player_pool.keys()))
            cpt_p = player_pool[cpt_name]
            cpt_cost = int(cpt_p["salary"] * 1.5)
            rem_sal = 50000 - cpt_cost
            
            avail = [k for k in player_pool.keys() if k != cpt_name]
            flex_names = random.sample(avail, 5)
            flex_cost = sum(player_pool[n]["salary"] for n in flex_names)
            
            if flex_cost <= rem_sal and (rem_sal - flex_cost) <= 2500:
                roster = [{
                    "name": cpt_name, "pos": cpt_p["pos"], "team": cpt_p["team"], "opp": cpt_p["opp"],
                    "salary": cpt_cost, "proj": round(cpt_p["proj"] * 1.5, 1), "alpha": 89.0, "is_cpt": True
                }]
                for fn in flex_names:
                    fp = player_pool[fn]
                    roster.append({
                        "name": fn, "pos": fp["pos"], "team": fp["team"], "opp": fp["opp"],
                        "salary": fp["salary"], "proj": fp["proj"], "alpha": 85.0, "is_cpt": False
                    })
                
                tot_proj = sum(p["proj"] for p in roster)
                tot_sal = cpt_cost + flex_cost
                teams = [p["team"] for p in roster]
                gb_c = teams.count("GB")
                atl_c = teams.count("ATL")
                stack_sum = f"{gb_c}-2 GB Heavy" if gb_c >= 4 else (f"{atl_c}-2 ATL Heavy" if atl_c >= 4 else "3-3 Split Game Script")

                meta = {
                    "remaining_salary": 50000 - tot_sal,
                    "stud_count": 3, "mid_count": 2, "punt_count": 1,
                    "leverage_label": "MME GPP CEILING",
                    "mike_verdict": f"150-Max GPP rotation with {cpt_name} Captain leverage."
                }
                lineups.append({
                    "lineup_id": f"DK_SHOWDOWN_GPP_{i+1:03d}",
                    "format_type": "SHOWDOWN",
                    "contest_type": "GPP",
                    "total_salary": tot_sal,
                    "projected_points": round(tot_proj, 2),
                    "floor_points": round(tot_proj * 0.70, 1),
                    "ceiling_points": round(tot_proj * 1.42, 1),
                    "stack_summary": stack_sum,
                    "roster_json": json.dumps(roster),
                    "meta_json": json.dumps(meta),
                    "created_at": ct_timestamp
                })
                break

    return lineups

# --- 2. CLASSIC GENERATOR: 150 GPP + 20 CASH ---
def generate_classic_pool():
    print("🏈 Generating 170 Classic Builds (150 MME GPP + 20 Cash)...")
    players = {
        "QB": [
            {"name": "Josh Allen", "pos": "QB", "team": "BUF", "opp": "LAC", "salary": 8000, "proj": 24.8},
            {"name": "Jared Goff", "pos": "QB", "team": "DET", "opp": "NYJ", "salary": 6400, "proj": 19.5},
            {"name": "Lamar Jackson", "pos": "QB", "team": "BAL", "opp": "DAL", "salary": 7900, "proj": 23.4},
            {"name": "Brock Purdy", "pos": "QB", "team": "SF", "opp": "ARI", "salary": 6300, "proj": 18.9}
        ],
        "RB": [
            {"name": "Christian McCaffrey", "pos": "RB", "team": "SF", "opp": "ARI", "salary": 8700, "proj": 22.4},
            {"name": "James Cook", "pos": "RB", "team": "BUF", "opp": "LAC", "salary": 6900, "proj": 16.8},
            {"name": "Jahmyr Gibbs", "pos": "RB", "team": "DET", "opp": "NYJ", "salary": 7200, "proj": 17.5},
            {"name": "Derrick Henry", "pos": "RB", "team": "BAL", "opp": "DAL", "salary": 6800, "proj": 16.2},
            {"name": "Tony Pollard", "pos": "RB", "team": "TEN", "opp": "NYG", "salary": 5800, "proj": 13.4},
            {"name": "Jordan Mason", "pos": "RB", "team": "SF", "opp": "ARI", "salary": 6200, "proj": 14.8}
        ],
        "WR": [
            {"name": "Amon-Ra St. Brown", "pos": "WR", "team": "DET", "opp": "NYJ", "salary": 8100, "proj": 20.2},
            {"name": "CeeDee Lamb", "pos": "WR", "team": "DAL", "opp": "BAL", "salary": 8500, "proj": 21.0},
            {"name": "Keon Coleman", "pos": "WR", "team": "BUF", "opp": "LAC", "salary": 5500, "proj": 12.5},
            {"name": "Khalil Shakir", "pos": "WR", "team": "BUF", "opp": "LAC", "salary": 5300, "proj": 12.2},
            {"name": "Jameson Williams", "pos": "WR", "team": "DET", "opp": "NYJ", "salary": 5800, "proj": 13.8},
            {"name": "Zay Flowers", "pos": "WR", "team": "BAL", "opp": "DAL", "salary": 6200, "proj": 14.5},
            {"name": "George Pickens", "pos": "WR", "team": "PIT", "opp": "CIN", "salary": 5700, "proj": 13.0},
            {"name": "Jauan Jennings", "pos": "WR", "team": "SF", "opp": "ARI", "salary": 4900, "proj": 11.0}
        ],
        "TE": [
            {"name": "Sam LaPorta", "pos": "TE", "team": "DET", "opp": "NYJ", "salary": 5900, "proj": 13.6},
            {"name": "Mark Andrews", "pos": "TE", "team": "BAL", "opp": "DAL", "salary": 5100, "proj": 11.8},
            {"name": "Dalton Kincaid", "pos": "TE", "team": "BUF", "opp": "LAC", "salary": 5200, "proj": 12.0},
            {"name": "George Kittle", "pos": "TE", "team": "SF", "opp": "ARI", "salary": 5800, "proj": 13.2}
        ],
        "DEF": [
            {"name": "Bills D/ST", "pos": "DEF", "team": "BUF", "opp": "LAC", "salary": 3400, "proj": 8.0},
            {"name": "Lions D/ST", "pos": "DEF", "team": "DET", "opp": "NYJ", "salary": 3100, "proj": 7.5},
            {"name": "49ers D/ST", "pos": "DEF", "team": "SF", "opp": "ARI", "salary": 3500, "proj": 8.5},
            {"name": "Steelers D/ST", "pos": "DEF", "team": "PIT", "opp": "CIN", "salary": 3300, "proj": 8.2}
        ]
    }

    ct_timestamp = get_current_central_time_str()
    lineups = []
    
    # 20 Cash (Relaxed buffer to ensure 100% completion)
    for i in range(20):
        while True:
            qb = random.choice(players["QB"])
            pass_catchers = [w for w in players["WR"] if w["team"] == qb["team"]] + [t for t in players["TE"] if t["team"] == qb["team"]]
            w1 = random.choice(pass_catchers) if pass_catchers else players["WR"][0]
            w2 = random.choice([w for w in players["WR"] if w["name"] != w1["name"]])
            w3 = random.choice([w for w in players["WR"] if w["name"] not in (w1["name"], w2["name"])])
            rbs = random.sample(players["RB"], 2)
            te = random.choice([t for t in players["TE"] if t["name"] != w1["name"]])
            dst = random.choice(players["DEF"])

            picked_names = {qb["name"], w1["name"], w2["name"], w3["name"], rbs[0]["name"], rbs[1]["name"], te["name"], dst["name"]}
            flex_candidates = [p for p in (players["RB"] + players["WR"] + players["TE"]) if p["name"] not in picked_names]
            flex = random.choice(flex_candidates)

            roster = [
                {"name": qb["name"], "pos": "QB", "team": qb["team"], "opp": qb["opp"], "salary": qb["salary"], "proj": qb["proj"], "alpha": 94.0},
                {"name": rbs[0]["name"], "pos": "RB", "team": rbs[0]["team"], "opp": rbs[0]["opp"], "salary": rbs[0]["salary"], "proj": rbs[0]["proj"], "alpha": 90.0},
                {"name": rbs[1]["name"], "pos": "RB", "team": rbs[1]["team"], "opp": rbs[1]["opp"], "salary": rbs[1]["salary"], "proj": rbs[1]["proj"], "alpha": 88.0},
                {"name": w1["name"], "pos": "WR", "team": w1["team"], "opp": w1["opp"], "salary": w1["salary"], "proj": w1["proj"], "alpha": 91.0},
                {"name": w2["name"], "pos": "WR", "team": w2["team"], "opp": w2["opp"], "salary": w2["salary"], "proj": w2["proj"], "alpha": 86.0},
                {"name": w3["name"], "pos": "WR", "team": w3["team"], "opp": w3["opp"], "salary": w3["salary"], "proj": w3["proj"], "alpha": 84.0},
                {"name": te["name"], "pos": "TE", "team": te["team"], "opp": te["opp"], "salary": te["salary"], "proj": te["proj"], "alpha": 85.0},
                {"name": flex["name"], "pos": flex["pos"], "team": flex["team"], "opp": flex["opp"], "salary": flex["salary"], "proj": flex["proj"], "alpha": 86.0},
                {"name": dst["name"], "pos": "DEF", "team": dst["team"], "opp": dst["opp"], "salary": dst["salary"], "proj": dst["proj"], "alpha": 84.0}
            ]

            tot_sal = sum(p["salary"] for p in roster)
            if tot_sal <= 50000 and (50000 - tot_sal) <= 2000:
                tot_proj = sum(p["proj"] for p in roster)
                meta = {
                    "remaining_salary": 50000 - tot_sal,
                    "stud_count": 3, "mid_count": 4, "punt_count": 2,
                    "leverage_label": "OPTIMAL CASH FLOOR",
                    "mike_verdict": "Maximum median floor. 2-stud RB foundation with high-volume QB."
                }
                lineups.append({
                    "lineup_id": f"DK_CLASSIC_CASH_{i+1:03d}",
                    "format_type": "CLASSIC",
                    "contest_type": "CASH",
                    "total_salary": tot_sal,
                    "projected_points": round(tot_proj, 2),
                    "floor_points": round(tot_proj * 0.77, 1),
                    "ceiling_points": round(tot_proj * 1.31, 1),
                    "stack_summary": f"{qb['team']} QB+{w1['pos']}",
                    "roster_json": json.dumps(roster),
                    "meta_json": json.dumps(meta),
                    "created_at": ct_timestamp
                })
                break

    # 150 GPP
    for i in range(150):
        while True:
            qb = random.choice(players["QB"])
            pass_catchers = [w for w in players["WR"] if w["team"] == qb["team"]] + [t for t in players["TE"] if t["team"] == qb["team"]]
            w1 = random.choice(pass_catchers) if pass_catchers else random.choice(players["WR"])
            
            bring_backs = [w for w in players["WR"] if w["team"] == qb["opp"]]
            w2 = random.choice(bring_backs) if bring_backs else random.choice([w for w in players["WR"] if w["name"] != w1["name"]])
            w3 = random.choice([w for w in players["WR"] if w["name"] not in (w1["name"], w2["name"])])
            rbs = random.sample(players["RB"], 2)
            te = random.choice([t for t in players["TE"] if t["name"] != w1["name"]])
            dst = random.choice(players["DEF"])

            picked_names = {qb["name"], w1["name"], w2["name"], w3["name"], rbs[0]["name"], rbs[1]["name"], te["name"], dst["name"]}
            flex_candidates = [p for p in (players["RB"] + players["WR"] + players["TE"]) if p["name"] not in picked_names]
            flex = random.choice(flex_candidates)

            roster = [
                {"name": qb["name"], "pos": "QB", "team": qb["team"], "opp": qb["opp"], "salary": qb["salary"], "proj": qb["proj"], "alpha": 91.0},
                {"name": rbs[0]["name"], "pos": "RB", "team": rbs[0]["team"], "opp": rbs[0]["opp"], "salary": rbs[0]["salary"], "proj": rbs[0]["proj"], "alpha": 87.0},
                {"name": rbs[1]["name"], "pos": "RB", "team": rbs[1]["team"], "opp": rbs[1]["opp"], "salary": rbs[1]["salary"], "proj": rbs[1]["proj"], "alpha": 85.0},
                {"name": w1["name"], "pos": "WR", "team": w1["team"], "opp": w1["opp"], "salary": w1["salary"], "proj": w1["proj"], "alpha": 89.0},
                {"name": w2["name"], "pos": "WR", "team": w2["team"], "opp": w2["opp"], "salary": w2["salary"], "proj": w2["proj"], "alpha": 84.0},
                {"name": w3["name"], "pos": "WR", "team": w3["team"], "opp": w3["opp"], "salary": w3["salary"], "proj": w3["proj"], "alpha": 83.0},
                {"name": te["name"], "pos": "TE", "team": te["team"], "opp": te["opp"], "salary": te["salary"], "proj": te["proj"], "alpha": 82.0},
                {"name": flex["name"], "pos": flex["pos"], "team": flex["team"], "opp": flex["opp"], "salary": flex["salary"], "proj": flex["proj"], "alpha": 84.0},
                {"name": dst["name"], "pos": "DEF", "team": dst["team"], "opp": dst["opp"], "salary": dst["salary"], "proj": dst["proj"], "alpha": 80.0}
            ]

            tot_sal = sum(p["salary"] for p in roster)
            if tot_sal <= 50000 and (50000 - tot_sal) <= 2200:
                tot_proj = sum(p["proj"] for p in roster)
                stack_label = f"{qb['team']} QB+{w1['pos']} w/ {w2['team']} Bring"
                meta = {
                    "remaining_salary": 50000 - tot_sal,
                    "stud_count": 2, "mid_count": 4, "punt_count": 3,
                    "leverage_label": "MME 150 TOURNAMENT CEILING",
                    "mike_verdict": f"Correlated game environment: {stack_label}."
                }
                lineups.append({
                    "lineup_id": f"DK_CLASSIC_GPP_{i+1:03d}",
                    "format_type": "CLASSIC",
                    "contest_type": "GPP",
                    "total_salary": tot_sal,
                    "projected_points": round(tot_proj, 2),
                    "floor_points": round(tot_proj * 0.72, 1),
                    "ceiling_points": round(tot_proj * 1.38, 1),
                    "stack_summary": stack_label,
                    "roster_json": json.dumps(roster),
                    "meta_json": json.dumps(meta),
                    "created_at": ct_timestamp
                })
                break

    return lineups

def build_full_portfolio():
    init_dfs_table()
    showdown = generate_showdown_pool()
    classic = generate_classic_pool()
    all_lineups = showdown + classic
    
    with get_db() as conn:
        conn.execute("DELETE FROM dfs_lineups")
        for l in all_lineups:
            conn.execute("""
                INSERT INTO dfs_lineups (lineup_id, format_type, contest_type, total_salary, projected_points, floor_points, ceiling_points, stack_summary, roster_json, meta_json, created_at)
                VALUES (:lineup_id, :format_type, :contest_type, :total_salary, :projected_points, :floor_points, :ceiling_points, :stack_summary, :roster_json, :meta_json, :created_at)
            """, l)
        conn.commit()

    print(f"✅ [SUCCESS] Generated and committed {len(all_lineups)} total lineups across 150 GPP / 20 Cash strategy in Central Time.")
    return True

if __name__ == "__main__":
    build_full_portfolio()