import os
import requests

# Put your actual key directly here for a quick verification test
API_KEY = "YOUR_ACTUAL_API_KEY_HERE"

print(f"🔑 Testing Odds API Key: {API_KEY[:5]}...[REDACTED]")
url = f"https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds/?apiKey={API_KEY}&regions=us&markets=h2h,spreads"

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    print(f"✅ SUCCESS! Fetched {len(data)} active game lines from live feed.")
    for game in data[:3]:
        print(f"  - Match: {game.get('away_team')} @ {game.get('home_team')} ({game.get('commence_time')})")
else:
    print(f"❌ API Error [{response.status_code}]: {response.text}")