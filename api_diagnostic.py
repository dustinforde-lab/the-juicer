import os
import sqlite3
import requests
import pandas as pd

# Fallback for Python versions under 3.11
try:
    import tomllib
except ImportError:
    import toml as tomllib 

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "action_grid.db")
SECRETS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".streamlit", "secrets.toml")

def get_toml_key(key_name):
    if not os.path.exists(SECRETS_PATH):
        return None
    try:
        # tomllib requires the file to be opened in binary mode
        with open(SECRETS_PATH, "rb") as f:
            data = tomllib.load(f)
        return data.get(key_name)
    except TypeError:
        # Fallback if a legacy third-party toml library rejects the binary stream
        with open(SECRETS_PATH, "r", encoding="utf-8") as f:
            data = tomllib.load(f)
        return data.get(key_name)
    except Exception:
        return None

def run_backend_health_check():
    print("\n============================================================")
    print(" 🛡️  INITIATING BACKEND DIAGNOSTIC & QUOTA GUARD (TOML)")
    print("============================================================")
    
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS odds_api_quota (
                Endpoint TEXT PRIMARY KEY,
                Calls_Made INTEGER,
                Last_Call TEXT
            )
        """)
    print("✅ QUOTA GUARD: Tracking table established in action_grid.db")

    try:
        espn = requests.get("https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard", timeout=5).json()
        print(f"✅ ESPN API: Online ({len(espn.get('events', []))} games detected)")
    except Exception as e:
        print(f"🚨 ESPN API: FAILED ({e})")

    try:
        sleeper = requests.get("https://api.sleeper.app/v1/state/nfl", timeout=5).json()
        print(f"✅ Sleeper API: Online (NFL Week {sleeper.get('week', 'UNK')} state loaded)")
    except Exception as e:
        print(f"🚨 Sleeper API: FAILED ({e})")

    odds_key = get_toml_key("ODDS_API_KEY")
    if odds_key and odds_key != "paste_odds_key_here":
        print("✅ The Odds API: TOML key detected. Live line scheduler is armed.")
    else:
        print("⚠️ The Odds API: Key missing. Paste it into .streamlit/secrets.toml.")

    mfl_cookie = get_toml_key("MFL_COOKIE")
    if mfl_cookie and mfl_cookie != "paste_mfl_cookie_here":
        print("✅ MyFantasyLeague: TOML cookie detected. Roster synchronization active.")
    else:
        print("⚠️ MyFantasyLeague: Cookie missing. Paste it into .streamlit/secrets.toml.")

    try:
        from ui_dfs import apply_mike_evaluator
        test_df = pd.DataFrame([{"Player": "Evaluator Test", "Pos": "TE", "PassYds":0, "PassTD":0, "RushYds":0, "RushTD":0, "Rec": 6, "RecYds": 65, "Salary": 4000}])
        val = apply_mike_evaluator(test_df).iloc[0]["DFS Value"]
        print(f"✅ Evaluator Pipeline: Online & Talking (Test record scored {val}x value)")
    except Exception as e:
        print(f"🚨 Evaluator Pipeline: FAILED ({e})")
        
    print("============================================================\n")

if __name__ == "__main__":
    run_backend_health_check()
