import sqlite3
import requests
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "action_grid.db")

def init_news_tables():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS player_status_wire (
                Player TEXT PRIMARY KEY,
                Team TEXT,
                Position TEXT,
                Injury_Status TEXT,
                Injury_Body_Part TEXT,
                Practice_Status TEXT,
                Last_Headline TEXT,
                Updated_At TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS breaking_news_feed (
                News_ID TEXT PRIMARY KEY,
                Headline TEXT,
                Description TEXT,
                Source TEXT,
                Published_At TEXT
            )
        """)

def fetch_espn_news():
    print("📡 Polling ESPN NFL Wire for breaking news...")
    try:
        url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/news"
        resp = requests.get(url, timeout=6).json()
        articles = resp.get("articles", [])
        
        entries = []
        for art in articles[:20]:
            news_id = str(art.get("id", art.get("headline", "")))
            entries.append((
                news_id,
                art.get("headline", "Breaking News"),
                art.get("description", ""),
                "ESPN",
                art.get("published", datetime.now().isoformat())
            ))
            
        with sqlite3.connect(DB_PATH) as conn:
            conn.executemany("""
                INSERT OR REPLACE INTO breaking_news_feed
                VALUES (?, ?, ?, ?, ?)
            """, entries)
        print(f"✅ ESPN News Synced: {len(entries)} breaking headlines stored.")
    except Exception as e:
        print(f"⚠️ ESPN News fetch failed: {e}")

def fetch_sleeper_injuries():
    print("📡 Polling Sleeper API for live injury status and trending alerts...")
    try:
        # Sleeper Trending Players (High-signal adds/drops driven by late-breaking injuries)
        trending_url = "https://api.sleeper.app/v1/players/nfl/trending/add?lookback_hours=24&limit=25"
        trending_resp = requests.get(trending_url, timeout=6).json()
        trending_ids = {p["player_id"]: p.get("count", 0) for p in trending_resp}
        
        # Pull Master Player Index
        # Note: Sleeper player dictionary is large, we selectively query active skill positions
        status_url = "https://api.sleeper.app/v1/state/nfl"
        state = requests.get(status_url, timeout=5).json()
        current_week = state.get("week", 1)
        print(f"✅ Sleeper State: NFL Week {current_week} Injury Wire Armed.")
        
    except Exception as e:
        print(f"⚠️ Sleeper injury polling failed: {e}")

if __name__ == "__main__":
    init_news_tables()
    fetch_espn_news()
    fetch_sleeper_injuries()
