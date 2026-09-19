import sqlite3
import json
import os
from datetime import datetime

DB_FILE = "action_grid.db"
BRAIN_FILE = "brain.json"

def load_modifiers():
    defaults = {"QB_PASS": 1.0, "RB_RUSH_REC": 1.0, "WR_RECEPTIONS": 1.0, "TE_RECEPTIONS": 1.0}
    if os.path.exists(BRAIN_FILE):
        try:
            with open(BRAIN_FILE, "r") as f:
                data = json.load(f)
                weights = data.get("model_weights", {})
                for k, v in weights.items():
                    defaults[k] = v.get("modifier", 1.0)
        except Exception:
            pass
    return defaults

def generate_rankings():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS player_rankings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player TEXT,
            position TEXT,
            team TEXT,
            stat_category TEXT,
            consensus_line REAL,
            juice_score REAL,
            rank INTEGER,
            updated_at TEXT
        )
    ''')
    cursor.execute("DELETE FROM player_rankings")
    
    weights = load_modifiers()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''
        SELECT player, position, team, stat_category, AVG(line) as consensus_line
        FROM vegas_lines
        GROUP BY player, stat_category
    ''')
    raw_props = cursor.fetchall()
    
    scored_players = []
    for player, pos, team, stat, cons_line in raw_props:
        mod_key = "QB_PASS" if pos == "QB" else ("RB_RUSH_REC" if pos == "RB" else ("WR_RECEPTIONS" if pos == "WR" else "TE_RECEPTIONS"))
        modifier = weights.get(mod_key, 1.0)
        juice_score = round(cons_line * modifier * 0.35, 2)
        scored_players.append((player, pos, team, stat, round(cons_line, 1), juice_score))
    
    scored_players.sort(key=lambda x: x[5], reverse=True)
    
    ranked_records = []
    for idx, p in enumerate(scored_players, 1):
        ranked_records.append((p[0], p[1], p[2], p[3], p[4], p[5], idx, now))
        
    cursor.executemany('''
        INSERT INTO player_rankings (player, position, team, stat_category, consensus_line, juice_score, rank, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', ranked_records)
    
    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM player_rankings")
    total = cursor.fetchone()[0]
    conn.close()
    
    print("=== INTERN 2 (MIKE EVALUATOR): SUCCESS ===")
    print(f"[EVALUATION] Processed consensus lines & generated {total} baseline Juice Rankings.")
    print(f"[TOP JUICER] {ranked_records[0][0]} ({ranked_records[0][1]}) - Score: {ranked_records[0][5]}")

if __name__ == "__main__":
    generate_rankings()
