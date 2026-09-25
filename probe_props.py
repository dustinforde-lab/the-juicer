import requests
import json
import os

print("--- [1/2] TESTING PRIZEPICKS (NFL LEAGUE ID 9) ---")
# PrizePicks uses league_id=9 for NFL
url = "https://api.prizepicks.com/projections?league_id=9&per_page=250&single_stat=true"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://app.prizepicks.com/"
}

try:
    res = requests.get(url, headers=headers, timeout=10)
    print(f"PrizePicks HTTP Status: {res.status_code}")
    if res.status_code == 200:
        data = res.json()
        props = data.get("data", [])
        included = {item["id"]: item["attributes"] for item in data.get("included", []) if item.get("type") == "new_player"}
        print(f"✅ PrizePicks NFL Lines Retrieved: {len(props)} props on board!")
        for p in props[:4]:
            attrs = p.get("attributes", {})
            rel_player = p.get("relationships", {}).get("new_player", {}).get("data", {})
            p_name = included.get(rel_player.get("id"), {}).get("name", "Player")
            print(f"   • {p_name}: {attrs.get('stat_type')} -> {attrs.get('line_score')}")
    else:
        print(f"⚠️ PrizePicks returned HTTP {res.status_code}: {res.text[:120]}")
except Exception as e:
    print(f"❌ PrizePicks probe error: {e}")

print("\n--- [2/2] TESTING THE ODDS API (PLAYER PROPS TARGETED) ---")
try:
    import stage_props_engine
    key = stage_props_engine.resolve_odds_api_key()
    if not key:
        print("❌ No Odds API key resolved.")
    else:
        # Step A: Get 1 live NFL event ID
        events_url = f"https://api.the-odds-api.com/v4/sports/americanfootball_nfl/events?apiKey={key}"
        ev_res = requests.get(events_url, timeout=10)
        print(f"Events Endpoint HTTP Status: {ev_res.status_code}")
        if ev_res.status_code == 200:
            events = ev_res.json()
            if events:
                target_ev = events[0]
                ev_id = target_ev["id"]
                matchup = f"{target_ev.get('away_team')} @ {target_ev.get('home_team')}"
                print(f"🎯 Target Event: {matchup} (ID: {ev_id})")
                
                # Step B: Query passing & rushing props for that single game
                prop_url = f"https://api.the-odds-api.com/v4/sports/americanfootball_nfl/events/{ev_id}/odds?apiKey={key}&regions=us&markets=player_pass_yds,player_rush_yds&oddsFormat=american"
                p_res = requests.get(prop_url, timeout=10)
                print(f"Player Props Endpoint HTTP Status: {p_res.status_code}")
                if p_res.status_code == 200:
                    p_data = p_res.json()
                    books = p_data.get("bookmakers", [])
                    print(f"✅ Retrieved props from {len(books)} sportsbooks for {matchup}!")
                    for b in books[:3]:
                        print(f"   • Book: {b.get('title')}")
                        for m in b.get("markets", []):
                            print(f"     - Market: {m.get('key')} ({len(m.get('outcomes', []))} outcomes)")
                else:
                    print(f"⚠️ Props returned {p_res.status_code}: {p_res.text[:120]}")
except Exception as e:
    print(f"❌ Odds API probe error: {e}")