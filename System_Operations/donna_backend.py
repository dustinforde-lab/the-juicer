import asyncio
import websockets
import json
import random
import os
import feedparser
from datetime import datetime

print("=====================================================")
print(" MIKE DONNA CLOUD ENGINE: INITIALIZING...            ")
print("=====================================================")
print("[SYSTEM] 10x Daily Simulation Protocol: ARMED")

def scrape_sharp_news():
    headlines = [
        "Breece Hall practice reps monitored; trend tracker adjusts floor.",
        "Sharp money flooding Seahawks spread across Pinnacle and Circa.",
        "Atmospheric alert: Sustained winds approaching 18mph in open-air venue.",
        "Amon-Ra St. Brown target-share projection locked at 35% ceiling.",
        "Derrick Henry rushing line steamed upward by institutional action."
    ]
    return random.choice(headlines)

def calculate_live_edge():
    players = ["Kenneth Walker", "Breece Hall", "Amon-Ra St. Brown", "Justin Herbert"]
    player = random.choice(players)
    
    dk_line = round(random.uniform(50.5, 90.5), 1)
    fd_line = round(dk_line + random.uniform(-3.5, 3.5), 1)
    pp_line = round(dk_line + random.uniform(-2.5, 2.5), 1)
    
    max_line = max(dk_line, fd_line, pp_line)
    min_line = min(dk_line, fd_line, pp_line)
    
    edge_alert = (max_line - min_line) > 3.0
        
    return {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "player": player,
        "draftkings": dk_line,
        "fanduel": fd_line,
        "prizepicks": pp_line,
        "arbitrage_detected": edge_alert,
        "delta": round(max_line - min_line, 1)
    }

async def donna_feed(websocket):
    print(f"[WEBSOCKET] Client connected")
    try:
        while True:
            odds_data = calculate_live_edge()
            news_data = scrape_sharp_news() if random.random() > 0.8 else None
            
            payload = {
                "type": "market_update",
                "data": odds_data,
            }
            if news_data:
                payload["news_alert"] = news_data
            
            await websocket.send(json.dumps(payload))
            await asyncio.sleep(2)
    except websockets.exceptions.ConnectionClosed:
        print("[WEBSOCKET] Client disconnected.")

async def main():
    port = int(os.environ.get("PORT", 8765))
    host = "0.0.0.0"
    async with websockets.serve(donna_feed, host, port):
        print(f"\n[SUCCESS] Mike Donna Engine broadcasting live on ws://{host}:{port}")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
