import sqlite3
import pandas as pd
import os
import random
import pulp

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "action_grid.db")

def init_and_seed_slate():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS dfs_projections (
                Player TEXT PRIMARY KEY, Pos TEXT, Team TEXT, Opp TEXT, Salary REAL,
                PassYds REAL DEFAULT 0, PassTD REAL DEFAULT 0,
                RushYds REAL DEFAULT 0, RushTD REAL DEFAULT 0,
                Rec REAL DEFAULT 0, RecYds REAL DEFAULT 0, RecTD REAL DEFAULT 0,
                Sacks REAL DEFAULT 0, Turnovers REAL DEFAULT 0, DefTD REAL DEFAULT 0, PtsAllowed REAL DEFAULT 20,
                FGM REAL DEFAULT 0, FG50 REAL DEFAULT 0, XPM REAL DEFAULT 0
            )
        """)
        
        # Check if user has ingested DKSalaries.csv or if table has data
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM dfs_projections")
        count = cur.fetchone()[0]
        
        if count == 0:
            print("⚡ Seeding tonight's Falcons @ Packers Showdown Pool...")
            # Live Week 3 Thursday Night Football Slate (ATL @ GB)
            players = [
                # Player, Pos, Team, Opp, Salary, PassYds, PassTD, RushYds, RushTD, Rec, RecYds, RecTD, Sacks, TO, DefTD, PA, FGM, FG50, XPM
                ("Bijan Robinson", "RB", "ATL", "GB", 11000, 0, 0, 78, 0.7, 5.2, 42, 0.3, 0,0,0,0, 0,0,0),
                ("Jordan Love", "QB", "GB", "ATL", 10400, 245, 1.9, 12, 0.1, 0, 0, 0, 0,0,0,0, 0,0,0),
                ("Josh Jacobs", "RB", "GB", "ATL", 10000, 0, 0, 84, 0.8, 2.5, 18, 0.1, 0,0,0,0, 0,0,0),
                ("Michael Penix Jr.", "QB", "ATL", "GB", 9400, 235, 1.6, 8, 0.1, 0, 0, 0, 0,0,0,0, 0,0,0),
                ("Drake London", "WR", "ATL", "GB", 9000, 0, 0, 0, 0, 6.4, 76, 0.6, 0,0,0,0, 0,0,0),
                ("Jayden Reed", "WR", "GB", "ATL", 8600, 0, 0, 14, 0.2, 5.1, 68, 0.5, 0,0,0,0, 0,0,0),
                ("Christian Watson", "WR", "GB", "ATL", 7400, 0, 0, 0, 0, 3.8, 54, 0.4, 0,0,0,0, 0,0,0),
                ("Romeo Doubs", "WR", "GB", "ATL", 6800, 0, 0, 0, 0, 4.2, 48, 0.3, 0,0,0,0, 0,0,0),
                ("Kyle Pitts", "TE", "ATL", "GB", 6600, 0, 0, 0, 0, 4.1, 46, 0.4, 0,0,0,0, 0,0,0),
                ("Darnell Mooney", "WR", "ATL", "GB", 6200, 0, 0, 0, 0, 3.9, 45, 0.3, 0,0,0,0, 0,0,0),
                ("Tucker Kraft", "TE", "GB", "ATL", 5200, 0, 0, 0, 0, 3.2, 34, 0.3, 0,0,0,0, 0,0,0),
                ("Brayden Narveson", "K", "GB", "ATL", 4800, 0,0,0,0,0,0,0, 0,0,0,0, 2.2, 0.5, 2.5),
                ("Tyler Allgeier", "RB", "ATL", "GB", 4600, 0, 0, 34, 0.2, 1.1, 8, 0.0, 0,0,0,0, 0,0,0),
                ("Younghoe Koo", "K", "ATL", "GB", 4400, 0,0,0,0,0,0,0, 0,0,0,0, 2.0, 0.4, 2.0),
                ("Dontayvion Wicks", "WR", "GB", "ATL", 4200, 0, 0, 0, 0, 2.8, 32, 0.2, 0,0,0,0, 0,0,0),
                ("Packers DST", "DST", "GB", "ATL", 4000, 0,0,0,0,0,0,0, 3.2, 1.4, 0.15, 20, 0,0,0),
                ("Falcons DST", "DST", "ATL", "GB", 3600, 0,0,0,0,0,0,0, 2.8, 1.1, 0.10, 24, 0,0,0),
                ("Ray-Ray McCloud", "WR", "ATL", "GB", 3400, 0, 0, 4, 0, 2.5, 26, 0.1, 0,0,0,0, 0,0,0)
            ]
            conn.executemany("""
                INSERT OR REPLACE INTO dfs_projections 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, players)
            conn.commit()

def calc_mike_base_ppr(row):
    pos = row.get("Pos", "")
    if pos == "K":
        return round(row.get("FGM", 2.0) * 3.0 + row.get("FG50", 0.4) * 2.0 + row.get("XPM", 2.5) * 1.0, 2)
    if pos == "DST":
        return round(row.get("Sacks", 3.0) * 1.0 + row.get("Turnovers", 1.2) * 2.0 + row.get("DefTD", 0.1) * 6.0 + max(0, 10.0 - (row.get("PtsAllowed", 21) * 0.3)), 2)
    pts = (row.get("PassYds", 0) / 25.0) + (row.get("RushYds", 0) / 10.0) + (row.get("RecYds", 0) / 10.0) + (row.get("Rec", 0) * 1.0)
    pts += (row.get("PassTD", 0) * 4.0) + (row.get("RushTD", 0) * 6.0) + (row.get("RecTD", 0) * 6.0)
    return round(pts, 2)

def build_showdown_pool(df):
    df["Projection"] = df.apply(calc_mike_base_ppr, axis=1)
    
    cpt_df = df.copy()
    cpt_df["Roster_Pos"] = "CPT"
    cpt_df["Salary"] = cpt_df["Salary"] * 1.5
    cpt_df["Projection"] = cpt_df["Projection"] * 1.5
    
    flex_df = df.copy()
    flex_df["Roster_Pos"] = "FLEX"
    
    return pd.concat([cpt_df, flex_df]).reset_index(drop=True)

def solve_lineup(df):
    prob = pulp.LpProblem("Showdown", pulp.LpMaximize)
    players = df.index.tolist()
    
    # GPP 15% Variance to find optimal unique pivots
    randomized = {i: df.loc[i, "Projection"] * random.uniform(0.85, 1.15) for i in players}
    player_vars = pulp.LpVariable.dicts("P", players, cat="Binary")
    
    prob += pulp.lpSum([randomized[i] * player_vars[i] for i in players])
    prob += pulp.lpSum([player_vars[i] for i in players]) == 6
    prob += pulp.lpSum([player_vars[i] for i in players if df.loc[i, "Roster_Pos"] == "CPT"]) == 1
    
    # Mike Uniqueness Constraint: Cap at $49,600 (prevents mass split pots)
    prob += pulp.lpSum([df.loc[i, "Salary"] * player_vars[i] for i in players]) <= 49600
    
    # No duplicate player across CPT and FLEX
    for name in df["Player"].unique():
        cpt = df[(df["Player"] == name) & (df["Roster_Pos"] == "CPT")].index
        flx = df[(df["Player"] == name) & (df["Roster_Pos"] == "FLEX")].index
        if len(cpt) > 0 and len(flx) > 0:
            prob += pulp.lpSum([player_vars[i] for i in cpt] + [player_vars[i] for i in flx]) <= 1
            
    # Mike Game Theory Rules: Cap Kickers and Defenses
    prob += pulp.lpSum([player_vars[i] for i in players if df.loc[i, "Pos"] == "K"]) <= 1
    prob += pulp.lpSum([player_vars[i] for i in players if df.loc[i, "Pos"] == "DST"]) <= 1
    
    # Correlation: If QB is CPT, must have >=1 Pass Catcher in FLEX
    for t in df["Team"].unique():
        qb_cpt = df[(df["Team"] == t) & (df["Pos"] == "QB") & (df["Roster_Pos"] == "CPT")].index
        pc_flx = df[(df["Team"] == t) & (df["Pos"].isin(["WR", "TE"])) & (df["Roster_Pos"] == "FLEX")].index
        if len(qb_cpt) > 0 and len(pc_flx) > 0:
            prob += pulp.lpSum([player_vars[i] for i in pc_flx]) >= player_vars[qb_cpt[0]]

    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    if pulp.LpStatus[prob.status] == "Optimal":
        return df.loc[[i for i in players if player_vars[i].varValue == 1]]
    return None

if __name__ == "__main__":
    init_and_seed_slate()
    with sqlite3.connect(DB_PATH) as conn:
        raw_df = pd.read_sql("SELECT * FROM dfs_projections", conn)
        
    pool = build_showdown_pool(raw_df)
    print("🚀 Running 150-Max Showdown GPP Engine with Mike Evaluator...")
    
    lineups, hashes, attempts = [], set(), 0
    while len(lineups) < 150 and attempts < 1000:
        attempts += 1
        lu = solve_lineup(pool)
        if lu is not None:
            cpt = lu[lu["Roster_Pos"] == "CPT"]["Player"].iloc[0]
            flex = sorted(lu[lu["Roster_Pos"] == "FLEX"]["Player"].tolist())
            lu_hash = cpt + " | " + " - ".join(flex)
            if lu_hash not in hashes:
                hashes.add(lu_hash)
                lineups.append({
                    "CPT": cpt,
                    "FLEX_1": flex[0], "FLEX_2": flex[1], "FLEX_3": flex[2], "FLEX_4": flex[3], "FLEX_5": flex[4],
                    "Total_Salary": lu["Salary"].sum(),
                    "Mike_PPR_Score": round(lu["Projection"].sum(), 2)
                })
                
    out_df = pd.DataFrame(lineups)
    out_df.to_csv("Juicer_Showdown_GPP_150.csv", index=False)
    print(f"🔥 SUCCESS: 150 Lineups Generated! Exported to Juicer_Showdown_GPP_150.csv")
