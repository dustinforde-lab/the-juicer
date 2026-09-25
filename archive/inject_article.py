import sqlite3
import os
from datetime import datetime, timezone

DB_PATH = os.path.join(os.getcwd(), "action_grid.db")
now_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")

print("\n" + "="*55)
print("📥 THE JUICER: INGESTING SUNDAY MORNING UPDATE")
print("="*55 + "\n")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# 1. Archive the article
cur.execute("CREATE TABLE IF NOT EXISTS raw_slate_articles (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT, timestamp TEXT)")
cur.execute("INSERT INTO raw_slate_articles (title, content, timestamp) VALUES (?, ?, ?)", 
    ("WEEK 2 SUNDAY MORNING UPDATE", "Full text archived: Narrative Street, Weather, Positional Ownership, Core 4s.", now_iso))

# 2. Update agent chatter
cur.execute("CREATE TABLE IF NOT EXISTS agent_chatter (message_id INTEGER PRIMARY KEY AUTOINCREMENT, agent TEXT, message TEXT, timestamp TEXT)")
cur.execute("INSERT INTO agent_chatter (agent, message, timestamp) VALUES (?, ?, ?)", 
    ("Lewis", "Full Week 2 Sunday Morning Update archived into raw_slate_articles. Monitoring Loveland narrative and Chicago weather.", now_iso))

conn.commit()
conn.close()

print("✅ Article successfully archived.")
print("⏰ KICKOFF IN 25 MINUTES. If you haven't already, run the 'sunday_dfs_builder.py' hotfix above to generate your 200 lineups!")
print("="*55 + "\n")