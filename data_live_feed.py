import os
import sqlite3
import requests
from datetime import datetime

try:
    import tomllib
except ImportError:
    import toml as tomllib 

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "action_grid.db")
SECRETS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".streamlit", "secrets.toml")

def get_toml_key(key_name):
    if not os.path.exists(SECRETS_PATH): return None
    try:
        with open(SECRETS_PATH, "rb") as f: data = tomllib.load(f)
        return data.get(key_name)
    except Exception:
        with open(SECRETS_PATH, "r", encoding="utf-8") as f: data = tomllib.load(f)
        return data.get(key_name)

def update_quota_ledger(cost):
    """Circuit Breaker: Records usage and prevents polling if close to the 500 limit"""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO odds_api_quota (Endpoint, Calls_Made, Last_Call)
            VALUES ('nfl_odds', ?, ?)
            ON CONFLICT(Endpoint) DO UPDATE SET 
                Calls_Made = Calls_Made + ?,
                Last_Call = ?
        """, (cost, datetime.now().isoformat(), cost, datetime.now().isoformat()))
        
        cur = conn.cursor()
        cur.execute("SELECT Calls_Made FROM odds_api_quota WHERE Endpoint = 'nfl_odds'")
        return cur.fetchone()[0]

def run_market_ingestion():
    api_key = get_toml_key("ODDS_API_KEY")
    
    # 1. Circuit Breaker Check
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT Calls_Made FROM odds_api_quota WHERE Endpoint = 'nfl_odds'")
        row = cur.fetchone()
        if row and row[0] >= 480:
            print("🚨 QUOTA GUARD ACTIVE: Approaching monthly limit. API call blocked to protect your account.")
            return

    # 2. Fetch Free News & State Feeds (ESPN / Sleeper)
    print("📡 Polling ESPN for Live Scores & News...")
    try:
        espn = requests.get("https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard", timeout=5).json()
        print(f"✅ ESPN Data Synced: {len(espn.get('events', []))} games tracked.")
    except Exception as e:
        print(f"⚠️ ESPN Poll Failed: {e}")

    print("📡 Polling Sleeper for NFL State...")
    try:
        sleeper = requests.get("https://api.sleeper.app/v1/state/nfl", timeout=5).json()
        print(f"✅ Sleeper Data Synced: Active Week {sleeper.get('week', 'UNK')}.")
    except Exception as e:
        print(f"⚠️ Sleeper Poll Failed: {e}")

    # 3. Fetch Live Lines (The Odds API)
    print("📡 Fetching Live Vegas Lines from The Odds API...")
    url = f"https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds?apiKey={api_key}&regions=us&markets=h2h,spreads,totals&oddsFormat=american"
    
    try:
        resp = requests.get(url, timeout=10)
        
        # Read quota directly from server headers
        cost = int(resp.headers.get("x-requests-last", 0))
        remaining = resp.headers.get("x-requests-remaining", "Unknown")
        
        if resp.status_code != 200:
            print(f"🚨 API Error: {resp.status_code} - {resp.text}")
            return
            
        total_used = update_quota_ledger(cost)
        print(f"✅ Quota Updated: {cost} credits used this run. Total Local: {total_used}. API Server Remaining: {remaining}")
        
        # 4. Parse Markets and Upsert to Action Grid
        data = resp.json()
        games_to_insert = []
        
        for game in data:
            game_id = game["id"]
            home = game["home_team"]
            away = game["away_team"]
            spread = 0.0
            over_under = 0.0
            
            # Extract DraftKings/US bookie lines for spreads and totals
            for bookie in game.get("bookmakers", []):
                for market in bookie.get("markets", []):
                    if market["key"] == "spreads":
                        for outcome in market["outcomes"]:
                            if outcome["name"] == home: spread = outcome.get("point", 0.0)
                    if market["key"] == "totals":
                        over_under = market["outcomes"][0].get("point", 0.0)
                if spread != 0.0 and over_under != 0.0: break
                
            games_to_insert.append((
                game_id, home, away, spread, over_under, "Clear", datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            
        with sqlite3.connect(DB_PATH) as conn:
            conn.executemany("""
                INSERT INTO vegas_lines (Game_ID, Home, Away, Spread, Over_Under, Weather_Alert, Updated_At)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(Game_ID) DO UPDATE SET 
                    Spread=excluded.Spread, 
                    Over_Under=excluded.Over_Under, 
                    Updated_At=excluded.Updated_At
            """, games_to_insert)
            
        print(f"✅ SUCCESS: {len(games_to_insert)} NFL games safely merged into action_grid.db.")
        
    except Exception as e:
        print(f"🚨 Ingestion Error: {e}")

if __name__ == '__main__':
    print("\n=======================================================")
    print(" 🔄 THE JUICER: LIVE MARKET INGESTION SCHEDULER")
    print("=======================================================")
    run_market_ingestion()
    print("=======================================================\n")
