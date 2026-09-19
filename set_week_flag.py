import json
import sqlite3
from datetime import datetime

BRAIN_FILE = "brain.json"
DB_FILE = "action_grid.db"
CURRENT_WEEK = 2
SLATE_INFO = "Week 2 - Lions at Bills (TNF)"

# 1. Update JSON Brain
try:
    with open(BRAIN_FILE, "r") as f:
        brain = json.load(f)
except Exception:
    brain = {"model_weights": {}, "bet_ledger": []}

brain["system_context"] = {
    "current_week": CURRENT_WEEK,
    "active_slate": SLATE_INFO,
    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

with open(BRAIN_FILE, "w") as f:
    json.dump(brain, f, indent=4)

# 2. Update SQLite Ledger
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS system_config (
        key TEXT PRIMARY KEY,
        value TEXT,
        updated_at TEXT
    )
""")
cursor.execute("REPLACE INTO system_config (key, value, updated_at) VALUES (?, ?, ?)", 
               ("current_week", str(CURRENT_WEEK), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
cursor.execute("REPLACE INTO system_config (key, value, updated_at) VALUES (?, ?, ?)", 
               ("active_slate", SLATE_INFO, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
conn.commit()
conn.close()

print("=== SYSTEM CONTEXT UPDATED ===")
print(f"[FLAG LOCKED] Engine globally synced to: {SLATE_INFO}")
