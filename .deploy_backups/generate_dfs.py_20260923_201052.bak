import json
import os
import random
import sqlite3
from datetime import datetime, timezone

DB_PATH = os.path.join(os.getcwd(), "action_grid.db")


def weighted_sample(pool, count, score_key, top_fraction=1.0):
    candidates = sorted(pool, key=score_key, reverse=True)
    candidates = candidates[:max(count, int(len(candidates) * top_fraction))]
    selected = []
    while candidates and len(selected) < count:
        weights = [max(0.1, score_key(player)) for player in candidates]
        player = random.choices(candidates, weights=weights, k=1)[0]
        selected.append(player)
        candidates.remove(player)
    return selected


def build_leg(player, tier):
    baseline = max(1.0, player["baseline"])
    line = round(baseline * {"A": 0.92, "B": 1.0, "C": 1.12}[tier], 1)
    return {
        "player_name": player["name"],
        "position": player["pos"],
        "stat_category": "PPR",
        "line": line,
        "direction": "OVER" if tier != "C" else "UNDER",
        "predicted_value": round(baseline, 1),
    }


def generate_lineups_and_slips():
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS dfs_rosters (
                roster_id INTEGER PRIMARY KEY AUTOINCREMENT,
                qb TEXT, rb1 TEXT, rb2 TEXT, wr1 TEXT, wr2 TEXT, wr3 TEXT,
                te TEXT, flex TEXT, projected_score REAL, dst TEXT,
                lineup_type TEXT DEFAULT 'GPP'
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS slips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                leg_count INTEGER NOT NULL,
                legs_json TEXT NOT NULL,
                implied_probability REAL,
                confidence_tier TEXT,
                status TEXT NOT NULL DEFAULT 'PENDING',
                legs_hit INTEGER,
                created_at TEXT NOT NULL,
                graded_at TEXT
            )
        """)
        rows = conn.execute("""
            SELECT player_name, pos, team,
                   COALESCE(ppr_baseline, projected_fp, 0),
                   COALESCE(sim_floor, 0), COALESCE(sim_ceiling, 0),
                   COALESCE(gpp_pathway, 0)
            FROM player_rankings
            WHERE ppr_baseline > 0 OR projected_fp > 0
        """).fetchall()
        players = [{
            "name": row[0], "pos": row[1], "team": row[2],
            "baseline": float(row[3] or 0), "floor": float(row[4] or row[3] or 0),
            "ceiling": float(row[5] or row[3] or 0), "pathway": float(row[6] or 0)
        } for row in rows]
        qbs = [p for p in players if p["pos"] == "QB"]
        rbs = [p for p in players if p["pos"] == "RB"]
        wrs = [p for p in players if p["pos"] == "WR"]
        tes = [p for p in players if p["pos"] == "TE"]
        dsts = [p for p in players if p["pos"] in ("DST", "DEF")]
        if not (qbs and len(rbs) >= 2 and len(wrs) >= 3 and tes):
            raise RuntimeError("Insufficient evaluated players for a nine-slot DFS roster")
        if not dsts:
            dsts = [{"name": "Defense", "pos": "DEF", "team": "NFL", "baseline": 6.0, "floor": 4.0, "ceiling": 10.0, "pathway": 0.0}]

        conn.execute("DELETE FROM dfs_rosters")
        lineups = []
        for index in range(200):
            lineup_type = "CASH" if index < 100 else "GPP"
            score_key = (lambda p: p["floor"]) if lineup_type == "CASH" else (lambda p: p["ceiling"] + p["pathway"] / 10)
            qb = weighted_sample(qbs, 1, score_key, 0.45)[0]
            rb = weighted_sample(rbs, 2, score_key, 0.55)
            wr = weighted_sample(wrs, 3, score_key, 0.55)
            te = weighted_sample(tes, 1, score_key, 0.6)[0]
            used = {qb["name"], *(p["name"] for p in rb + wr), te["name"]}
            flex_pool = [p for p in rbs + wrs + tes if p["name"] not in used]
            flex = weighted_sample(flex_pool or rbs, 1, score_key, 0.75)[0]
            dst = weighted_sample(dsts, 1, score_key, 1.0)[0]
            projection = round(sum(p["baseline"] for p in [qb, *rb, *wr, te, flex, dst]), 1)
            lineups.append((qb["name"], rb[0]["name"], rb[1]["name"], wr[0]["name"], wr[1]["name"], wr[2]["name"], te["name"], flex["name"], projection, dst["name"], lineup_type))
        conn.executemany("""
            INSERT INTO dfs_rosters (qb, rb1, rb2, wr1, wr2, wr3, te, flex, projected_score, dst, lineup_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, lineups)

        conn.execute("DELETE FROM slips")
        slip_specs = [("SPORTSBOOK_PARLAY", 250, (2, 4)), ("PRIZEPICKS", 75, (2, 3)), ("UNDERDOG", 75, (2, 3))]
        offensive = [p for p in players if p["pos"] in ("QB", "RB", "WR", "TE")]
        slips = []
        for platform, count, leg_range in slip_specs:
            for index in range(count):
                tier = "A" if index < int(count * 0.5) else "B" if index < int(count * 0.8) else "C"
                score_key = (lambda p: p["floor"]) if tier == "A" else (lambda p: p["baseline"]) if tier == "B" else (lambda p: p["ceiling"] + p["pathway"] / 10)
                leg_count = random.randint(*leg_range)
                chosen = weighted_sample(offensive, min(leg_count, len(offensive)), score_key, 0.5 if tier == "A" else 0.85)
                legs = [build_leg(player, tier) for player in chosen]
                probability = {"A": 0.68, "B": 0.54, "C": 0.36}[tier]
                slips.append((platform, len(legs), json.dumps(legs), probability, tier, "PENDING", now))
        conn.executemany("""
            INSERT INTO slips (platform, leg_count, legs_json, implied_probability, confidence_tier, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, slips)
        conn.commit()
    print(f"Generated {len(lineups)} DFS lineups and {len(slips)} weighted slips.")


if __name__ == "__main__":
    generate_lineups_and_slips()
