import sqlite3, json, random
from datetime import datetime

DB_FILE = "action_grid.db"
SOURCES = ["DraftKings", "FanDuel", "BetMGM", "Caesars"]

SUNDAY_CORRELATIONS = [
    {"game": "DAL vs NYG", "qb": ("Dak Prescott", "DAL", "Pass Yds > 262.5"), "wr": ("CeeDee Lamb", "DAL", "Rec Yds > 84.5"), "opp": ("Malik Nabers", "NYG", "Rec Yds > 68.5")},
    {"game": "SF vs LAR", "qb": ("Brock Purdy", "SF", "Pass TDs > 1.5"), "wr": ("Deebo Samuel", "SF", "Anytime TD"), "opp": ("Kyren Williams", "LAR", "Rush Yds > 72.5")},
    {"game": "KC vs LAC", "qb": ("Patrick Mahomes", "KC", "Pass Yds > 255.5"), "wr": ("Travis Kelce", "KC", "Rec Yds > 58.5"), "opp": ("Ladd McConkey", "LAC", "Rec Yds > 52.5")},
    {"game": "DEN vs LV", "qb": ("Bo Nix", "DEN", "Pass Yds > 215.5"), "wr": ("Courtland Sutton", "DEN", "Rec Yds > 54.5"), "rush": ("Javonte Williams", "DEN", "Rush Yds > 62.5"), "opp": ("Brock Bowers", "LV", "Rec Yds > 56.5")}
]

def execute_telemetry_driven_build():
    print("=" * 65)
    print("🧠 [UPGRADE CHUNK 11] Mike Integrating Recipe Book & Telemetry...")
    print("=" * 65)
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        
        chatter = cur.execute("SELECT sender, directive, target, action FROM agent_chatter").fetchall()
        hard_purges = [c[2] for c in chatter if c[3] == "HARD PURGE"]
        force_includes = [c[2] for c in chatter if c[3] == "FORCE INCLUDE"]
        faded_games = [c[2] for c in chatter if "Fade Passing" in c[3]]

        print(f"   • Telemetry Read: {len(hard_purges)} Purged Players, {len(force_includes)} Forced Sharps, {len(faded_games)} Faded Games")

        valid_trees = []
        for c in SUNDAY_CORRELATIONS:
            if c["qb"][0] in hard_purges or c["wr"][0] in hard_purges or c["opp"][0] in hard_purges:
                print(f"   🚫 Bypassing {c['game']} (Contains injured/purged player)")
                continue
            if c["game"] in faded_games:
                print(f"   🌪️ Bypassing {c['game']} (Weather: passing faded)")
                continue
            valid_trees.append(c)

        now_ts = datetime.now().strftime("%Y-%m-%d %I:%M %p ET")
        cur.execute("DELETE FROM theoretical_bets")

        for i in range(1, 201):
            tier = "Cash Builder" if i <= 80 else ("Syndicate Core" if i <= 160 else "Moonshot Whale")
            color = {"Cash Builder": "#00ff88", "Syndicate Core": "#00e5ff", "Moonshot Whale": "#ff2a6d"}[tier]
            source = random.choice(SOURCES)
            c = random.choice(valid_trees)
            legs = []

            if tier in ["Syndicate Core", "Moonshot Whale"] and force_includes and (i % 2 == 0):
                forced_p = random.choice(force_includes)
                sharp_row = cur.execute("SELECT stat_target FROM sharp_market_lines WHERE player_name = ?", (forced_p,)).fetchone()
                stat = sharp_row[0] if sharp_row else "Anytime TD"
                legs.append({"player": forced_p, "team": "SF" if "Deebo" in forced_p else "DEN", "stat": stat})

            if len(legs) == 0:
                legs.append({"player": c["qb"][0], "team": c["qb"][1], "stat": c["qb"][2]})
            legs.append({"player": c["wr"][0], "team": c["wr"][1], "stat": c["wr"][2]})
            if tier != "Cash Builder":
                legs.append({"player": c["opp"][0], "team": c["opp"][1], "stat": c["opp"][2]})
            if tier == "Moonshot Whale" and len(legs) < 4:
                rush_stat = c.get("rush", ("Brock Bowers", "LV", "Rec Yds > 56.5"))
                legs.append({"player": rush_stat[0], "team": rush_stat[1], "stat": rush_stat[2]})

            odds = f"+{random.randint(210, 320)}" if tier == "Cash Builder" else (f"+{random.randint(520, 890)}" if tier == "Syndicate Core" else f"+{random.randint(1200, 2400)}")
            tid = f"SLIP-{i:03d} ({tier.upper()})"
            cur.execute("INSERT INTO theoretical_bets VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (tid, tier, odds, color, json.dumps(legs), source, now_ts))
        conn.commit()

def run_self_test():
    print("\n🧪 [SELF-CHECK GATE] Auditing Telemetry-Driven Inventory...")
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        rows = cur.execute("SELECT ticket_id, ticket_json FROM theoretical_bets").fetchall()
        assert len(rows) == 200, f"Integrity Failure: Expected 200 slips, got {len(rows)}"

        chatter = cur.execute("SELECT target, action FROM agent_chatter").fetchall()
        purges = [c[0] for c in chatter if c[1] == "HARD PURGE"]
        forces = [c[0] for c in chatter if c[1] == "FORCE INCLUDE"]

        found_forced = False
        for tid, tjson in rows:
            legs = json.loads(tjson)
            for leg in legs:
                assert leg["player"] not in purges, f"Quarantine Breach: {leg['player']} in {tid}"
                if leg["player"] in forces: found_forced = True
        assert found_forced, "Telemetry Failure: Forced sharp plays missing from inventory."
    print("✅ ALL GATES PASSED: 200 Slips, Zero Injured Players, Sharp Lines Successfully Injected.\n")

if __name__ == "__main__":
    execute_telemetry_driven_build()
    run_self_test()
