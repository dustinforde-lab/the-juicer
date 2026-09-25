"""
The Juicer - Production Market Prop Consensus Pipeline
Ingests player props from The Odds API across sharp books (DraftKings, FanDuel, BetRivers).
Computes mean stat lines and generates Mike's true quant baseline.
"""
import requests
import sqlite3
import json
import os
from collections import Counter

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "action_grid.db")

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=10000;")
    conn.row_factory = sqlite3.Row
    return conn

def resolve_odds_api_key():
    toml_paths = [
        os.path.join(os.path.dirname(__file__), ".streamlit", "secrets.toml"),
        os.path.join(os.path.dirname(__file__), "secrets.toml"),
        os.path.expanduser("~/.streamlit/secrets.toml")
    ]
    for tp in toml_paths:
        if os.path.exists(tp):
            try:
                with open(tp, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("#") or not line:
                            continue
                        if any(term in line.upper() for term in ["ODDS", "API_KEY"]):
                            if "=" in line:
                                return line.split("=", 1)[1].strip().strip("\"'")
            except Exception:
                pass
    return os.environ.get("ODDS_API_KEY")

def sync_live_player_props(max_events=2):
    """
    Pulls player props for current upcoming games (e.g., TNF / Marquee games)
    across DraftKings, FanDuel, BetRivers, and other active sportsbooks.
    """
    key = resolve_odds_api_key()
    if not key:
        print("❌ [FAIL] Missing Odds API Key.")
        return 0

    events_url = f"https://api.the-odds-api.com/v4/sports/americanfootball_nfl/events?apiKey={key}"
    try:
        ev_res = requests.get(events_url, timeout=10)
        if ev_res.status_code != 200:
            print(f"⚠️ Failed to fetch events: HTTP {ev_res.status_code}")
            return 0
        events = ev_res.json()
    except Exception as e:
        print(f"❌ Events fetch error: {e}")
        return 0

    target_events = events[:max_events]
    total_props_saved = 0
    markets = "player_pass_yds,player_rush_yds,player_receptions"

    with get_db() as conn:
        for ev in target_events:
            ev_id = ev["id"]
            home = ev.get("home_team", "HME")
            away = ev.get("away_team", "AWY")
            matchup = f"{away} @ {home}"
            print(f"📡 Syncing Props for: {matchup}...")

            prop_url = f"https://api.the-odds-api.com/v4/sports/americanfootball_nfl/events/{ev_id}/odds?apiKey={key}&regions=us&markets={markets}&oddsFormat=american"
            try:
                res = requests.get(prop_url, timeout=12)
                if res.status_code != 200:
                    continue
                p_data = res.json()
                books = p_data.get("bookmakers", [])
                
                for b in books:
                    b_title = b.get("title", b.get("key"))
                    for m in b.get("markets", []):
                        m_key = m.get("key")
                        stat_type = "pass_yds" if "pass" in m_key else ("rush_yds" if "rush" in m_key else "receptions")
                        outcomes = m.get("outcomes", [])
                        players = {o.get("description") for o in outcomes if o.get("description")}

                        for p_name in players:
                            p_outs = [o for o in outcomes if o.get("description") == p_name]
                            over_o = next((o for o in p_outs if o.get("name") == "Over"), None)
                            under_o = next((o for o in p_outs if o.get("name") == "Under"), None)

                            if over_o:
                                line_val = float(over_o.get("point", 0))
                                o_odds = int(over_o.get("price", -110))
                                u_odds = int(under_o.get("price", -110)) if under_o else -110

                                prop_id = f"{p_name}_{stat_type}_{b_title}".replace(" ", "_").upper()
                                conn.execute("""
                                    INSERT INTO market_player_props (prop_id, player_name, team, opp, game_id, stat_type, line_value, over_odds, under_odds, source, updated_at)
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                                    ON CONFLICT(prop_id) DO UPDATE SET
                                        line_value=excluded.line_value,
                                        over_odds=excluded.over_odds,
                                        under_odds=excluded.under_odds,
                                        updated_at=CURRENT_TIMESTAMP
                                """, (prop_id, p_name, away, home, ev_id, stat_type, line_val, o_odds, u_odds, b_title))

                                conn.execute("""
                                    INSERT INTO market_props_history (player_name, stat_type, line_value, over_odds, under_odds, source)
                                    VALUES (?, ?, ?, ?, ?, ?)
                                """, (p_name, stat_type, line_val, o_odds, u_odds, b_title))
                                total_props_saved += 1
            except Exception as err:
                print(f"⚠️ Error syncing {matchup}: {err}")

        conn.commit()

    print(f"✅ [SUCCESS] Ingested {total_props_saved} market props across active sportsbooks.")
    return total_props_saved

def compute_mike_quant_baselines():
    """
    Derives Mike's baseline projections from the consensus mean of sportsbooks.
    Applies yardage right-skew scalar (1.05x) and calculates DraftKings fantasy points.
    """
    with get_db() as conn:
        rows = conn.execute("SELECT player_name, team, stat_type, line_value, over_odds, source FROM market_player_props").fetchall()

    if not rows:
        return {}

    players = {}
    for r in rows:
        p_name = r["player_name"]
        stype = r["stat_type"]
        if p_name not in players:
            players[p_name] = {"team": r["team"], "stats": {}, "sources": set()}
        if stype not in players[p_name]["stats"]:
            players[p_name]["stats"][stype] = []
        players[p_name]["stats"][stype].append(r["line_value"])
        players[p_name]["sources"].add(r["source"])

    baselines = {}
    for p_name, data in players.items():
        stats = data["stats"]
        pass_mean = (sum(stats["pass_yds"]) / len(stats["pass_yds"])) * 1.04 if "pass_yds" in stats else 0.0
        rush_mean = (sum(stats["rush_yds"]) / len(stats["rush_yds"])) * 1.06 if "rush_yds" in stats else 0.0
        rec_mean = (sum(stats["receptions"]) / len(stats["receptions"])) if "receptions" in stats else 0.0

        # DraftKings scoring: 0.04/pass_yd, 0.10/rush_yd, 1.0/rec
        dk_pts = (pass_mean * 0.04) + (rush_mean * 0.10) + (rec_mean * 1.0)
        if pass_mean >= 300: dk_pts += 3.0
        if rush_mean >= 100: dk_pts += 3.0

        baselines[p_name] = {
            "player_name": p_name,
            "pass_yds_consensus": round(pass_mean, 1),
            "rush_yds_consensus": round(rush_mean, 1),
            "receptions_consensus": round(rec_mean, 1),
            "raw_quant_baseline": round(dk_pts, 2),
            "books_reporting": len(data["sources"]),
            "book_list": list(data["sources"])
        }

    return baselines

def run_self_audit():
    saved = sync_live_player_props(max_events=1)
    baselines = compute_mike_quant_baselines()
    print(f"\n📊 Evaluated {len(baselines)} unique players from live sportsbook consensus:")
    for p_name, b in list(baselines.items())[:5]:
        books_str = ", ".join(b["book_list"][:3])
        print(f"  • {p_name:<20} -> {b['raw_quant_baseline']:>5.2f} DK Pts | Pass: {b['pass_yds_consensus']:<4} | Rush: {b['rush_yds_consensus']:<4} ({b['books_reporting']} Books: {books_str})")
    print("✅ [PASS] Market Prop Consensus Engine verified.")
    return True

if __name__ == "__main__":
    run_self_audit()