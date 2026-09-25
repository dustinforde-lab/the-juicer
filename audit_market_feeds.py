"""
The Juicer - TOML-Aware Odds API & Sportsbook Line Auditor
Reads API keys from .streamlit/secrets.toml, inspects active bookmakers,
and checks scoreboard_live line repository columns dynamically.
"""
import os
import sys
import requests
import sqlite3
from collections import Counter
from datetime import datetime

# 1. Load keys from Streamlit secrets.toml or root secrets.toml
odds_key = None
toml_paths = [
    os.path.join(os.path.dirname(__file__), ".streamlit", "secrets.toml"),
    os.path.join(os.path.dirname(__file__), "secrets.toml"),
    os.path.expanduser("~/.streamlit/secrets.toml")
]

for tp in toml_paths:
    if os.path.exists(tp):
        print(f"📄 Found TOML secrets at: {tp}")
        try:
            # Simple line parse to avoid extra library dependencies
            with open(tp, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("#") or not line:
                        continue
                    if any(term in line.upper() for term in ["ODDS", "API_KEY"]):
                        if "=" in line:
                            parts = line.split("=", 1)
                            key_name = parts[0].strip()
                            raw_val = parts[1].strip().strip('"').strip("'")
                            if raw_val:
                                odds_key = raw_val
                                print(f"   -> Resolved key variable: '{key_name}'")
                                break
            if odds_key:
                break
        except Exception as err:
            print(f"   Note: Failed to parse {tp}: {err}")

# Fallback to os.environ or config
if not odds_key:
    odds_key = os.environ.get("ODDS_API_KEY") or os.environ.get("THE_ODDS_API_KEY")

print("\n" + "="*68)
print("  🎯 THE ODDS API: LIVE SPORTSBOOK & MARKET LINE DEPTH")
print("="*68)

if not odds_key:
    print("❌ [FAIL] Could not locate an Odds API key in any secrets.toml file or env.")
else:
    masked_key = odds_key[:4] + "..." + odds_key[-4:] if len(odds_key) > 8 else "***"
    print(f"🔑 Authenticated Key: {masked_key}")
    
    url = f"https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds/?apiKey={odds_key}&regions=us&markets=spreads,totals&oddsFormat=american"
    
    try:
        res = requests.get(url, timeout=12)
        print(f"📡 API HTTP Status: {res.status_code}")
        
        if res.status_code == 200:
            games = res.json()
            remaining = res.headers.get("x-requests-remaining", "Unknown")
            used = res.headers.get("x-requests-used", "Unknown")
            
            print(f"📊 Account Quota: {remaining} requests remaining ({used} used this billing cycle)")
            print(f"🏈 NFL Events Evaluated: {len(games)} games\n")
            
            book_counter = Counter()
            total_spreads = 0
            total_totals = 0
            
            for g in games:
                for b in g.get("bookmakers", []):
                    b_title = b.get("title", b.get("key"))
                    book_counter[b_title] += 1
                    for m in b.get("markets", []):
                        if m.get("key") == "spreads":
                            total_spreads += len(m.get("outcomes", []))
                        elif m.get("key") == "totals":
                            total_totals += len(m.get("outcomes", []))
                            
            print(f"🏢 Active Sportsbooks Feeding Mike's Consensus ({len(book_counter)} Total Books):")
            print("-" * 68)
            for book, count in book_counter.most_common():
                print(f"   • {book:<28} -> Pricing {count} games")
                
            print("-" * 68)
            print(f"📈 Total Pricing Data Points Ingested:")
            print(f"   • Spread Line Outcomes:  {total_spreads}")
            print(f"   • Over/Under Outcomes:   {total_totals}")
            print(f"   • Grand Market Total:    {total_spreads + total_totals} live pricing points")
            
            print("\n📋 Matchup Breakdown (Books Pricing Each Game):")
            for g in games[:6]:
                matchup_str = f"{g.get('away_team')} @ {g.get('home_team')}"
                books_on_game = len(g.get("bookmakers", []))
                print(f"   • {matchup_str:<38} | {books_on_game} sportsbooks active")
                
        elif res.status_code == 401:
            print("❌ [401 Unauthorized] The Odds API rejected this key.")
        elif res.status_code == 429:
            print("⚠️ [429 Rate Limit] Monthly API quota reached.")
        else:
            print(f"⚠️ API returned code {res.status_code}: {res.text}")
    except Exception as err:
        print(f"❌ Connection error reaching The Odds API: {err}")

print("\n" + "="*68)
print("  🏈 MYFANTASYLEAGUE (MFL) SCHEDULE FEED")
print("="*68)
mfl_year = datetime.now().year
mfl_url = f"https://api.myfantasyleague.com/{mfl_year}/export?TYPE=nflSchedule&W=3&JSON=1"
try:
    mfl_res = requests.get(mfl_url, headers={"User-Agent": "TheJuicerSyndicate/1.0"}, timeout=10)
    if mfl_res.status_code == 200:
        matchups = mfl_res.json().get("nflSchedule", {}).get("matchup", [])
        print(f"✅ MFL API Active: {len(matchups)} Week 3 matchups verified.")
    else:
        print(f"⚠️ MFL responded with HTTP {mfl_res.status_code}")
except Exception as err:
    print(f"❌ MFL Error: {err}")

print("\n" + "="*68)
print("  🗄️ LOCAL DATABASE (scoreboard_live) DYNAMIC REPOSITORY CHECK")
print("="*68)
db_file = "action_grid.db"
if os.path.exists(db_file):
    with sqlite3.connect(db_file) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("PRAGMA table_info(scoreboard_live)")
        cols = [r["name"] for r in cur.fetchall()]
        print(f"✅ Live Table Columns: {', '.join(cols)}")
        
        # Pull first 3 rows dynamically
        sample_rows = cur.execute("SELECT * FROM scoreboard_live LIMIT 3").fetchall()
        print(f"✅ Sample Records ({len(sample_rows)} rows):")
        for r in sample_rows:
            r_dict = dict(r)
            # Find game identifiers
            name = r_dict.get("short_name") or f"{r_dict.get('away_team','AWY')} @ {r_dict.get('home_team','HME')}"
            status = r_dict.get("status_state") or r_dict.get("status_detail", "Scheduled")
            print(f"   • {name:<22} | Status: {status:<10} | Updated: {r_dict.get('updated_at', 'N/A')}")
else:
    print(f"⚠️ {db_file} not found.")

print("\n" + "="*68 + "\n")