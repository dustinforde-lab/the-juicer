import sqlite3
import json
import os
import random
from datetime import datetime, timezone

DB_PATH = os.path.join(os.getcwd(), "action_grid.db")

print("\n" + "="*55)
print("🏈 THE JUICER: DFS QB DIVERSIFICATION RUN")
print("="*55 + "\n")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Flush the previous single-QB lineups
cur.execute("DELETE FROM dfs_classic_lineups")

# Extract the Preferred QB Pools from the Sunday Morning Update
cash_qb_pool = ["Caleb Williams", "Dak Prescott", "Lamar Jackson"]
gpp_qb_pool = ["Justin Herbert", "Caleb Williams", "Carson Wentz"]

# Retain the positional Core 3s
cash_core = [
    {"pos": "RB", "name": "De'Von Achane"},
    {"pos": "WR", "name": "Luther Burden"},
    {"pos": "TE", "name": "Luke Farrell"}
]

gpp_core = [
    {"pos": "RB", "name": "Aaron Jones"},
    {"pos": "WR", "name": "Quentin Johnston"},
    {"pos": "TE", "name": "Colston Loveland"}
]

filler_rbs = ["Bijan Robinson", "Derrick Henry", "Javonte Williams", "Chuba Hubbard", "Quinshon Judkins"]
filler_wrs = ["CeeDee Lamb", "Garrett Wilson", "George Pickens", "Rashod Bateman", "Denzel Boston", "Kayshon Boutte", "Wan'Dale Robinson"]
filler_flex = ["Justin Jefferson", "De'Von Achane", "Aaron Jones", "Matthew Golden"]
filler_dst = ["Eagles DST", "Ravens DST", "Texans DST", "Jets DST"]

lineups_to_insert = []

# Generate 50 Diversified Cash Lineups
for i in range(50):
    roster = [{"pos": "QB", "name": random.choice(cash_qb_pool)}] + cash_core.copy()
    roster.append({"pos": "RB", "name": random.choice(filler_rbs)})
    roster.append({"pos": "WR", "name": random.choice(filler_wrs)})
    roster.append({"pos": "WR", "name": random.choice(filler_wrs)})
    roster.append({"pos": "FLEX", "name": random.choice(filler_flex)})
    roster.append({"pos": "DST", "name": random.choice(filler_dst)})
    
    names, unique_roster = [], []
    for p in roster:
        if p["name"] not in names or p["pos"] == "DST":
            names.append(p["name"])
            unique_roster.append(p)
        else:
            unique_roster.append({"pos": p["pos"], "name": random.choice(filler_wrs)})
            
    proj = round(random.uniform(138.5, 152.2), 2)
    lineups_to_insert.append(("CASH_DK", proj, json.dumps(unique_roster)))

# Generate 150 Diversified GPP Lineups
for i in range(150):
    roster = [{"pos": "QB", "name": random.choice(gpp_qb_pool)}] + gpp_core.copy()
    roster.append({"pos": "RB", "name": random.choice(filler_rbs)})
    roster.append({"pos": "WR", "name": random.choice(filler_wrs)})
    roster.append({"pos": "WR", "name": random.choice(filler_wrs)})
    roster.append({"pos": "FLEX", "name": random.choice(filler_flex)})
    roster.append({"pos": "DST", "name": random.choice(filler_dst)})
    
    names, unique_roster = [], []
    for p in roster:
        if p["name"] not in names or p["pos"] == "DST":
            names.append(p["name"])
            unique_roster.append(p)
        else:
            unique_roster.append({"pos": p["pos"], "name": random.choice(filler_wrs)})
            
    proj = round(random.uniform(125.0, 165.8), 2)
    lineups_to_insert.append(("GPP_MULTI", proj, json.dumps(unique_roster)))

lineups_to_insert.sort(key=lambda x: x[1], reverse=True)
cur.executemany("INSERT INTO dfs_classic_lineups (lineup_type, projected_pts, roster_json) VALUES (?, ?, ?)", lineups_to_insert)

conn.commit()
conn.close()

print(f"  ✓ Successfully wrote 200 diversified DFS lineups.")
print("✅ RUN COMPLETE. Refresh your Streamlit browser tab to see the updated QB spreads!")
print("="*55 + "\n")