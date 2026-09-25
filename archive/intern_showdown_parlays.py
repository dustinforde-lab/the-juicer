import sqlite3
import random
import json
from datetime import datetime

DB_FILE = "action_grid.db"

def get_top_props():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, player_name, stat_category, line, over_odds, sportsbook, canonical_id
        FROM sportsbook_quotes
    """)
    props = cursor.fetchall()
    conn.close()
    return [{"id": p[0], "player": p[1], "stat": p[2], "line": p[3], "odds": p[4], "book": p[5], "canonical": p[6]} for p in props]

def build_same_game_parlays(props):
    parlays = []
    
    for i in range(1, 251):
        leg_count = random.choices([2, 3, 4, 5, 6], weights=[40, 30, 15, 10, 5])[0]
        ticket_props = []
        used_canonicals = set()
        
        shuffled = random.sample(props, len(props))
        for p in shuffled:
            if p["canonical"] not in used_canonicals:
                ticket_props.append(p)
                used_canonicals.add(p["canonical"])
            if len(ticket_props) == leg_count:
                break
                
        if len(ticket_props) == leg_count:
            parlays.append({
                "ticket_id": f"SGP_TNF_{i}",
                "legs": leg_count,
                "props": ticket_props,
                "weight": "Heavy Foundation" if leg_count <= 3 else "Fractional Lotto"
            })
            
    return parlays

def log_parlays():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS theoretical_bets (
            ticket_id TEXT PRIMARY KEY,
            slate_type TEXT,
            legs INTEGER,
            weight_class TEXT,
            ticket_json TEXT,
            timestamp TEXT
        )
    """)
    
    # Patch legacy table missing the new column
    try:
        cursor.execute("ALTER TABLE theoretical_bets ADD COLUMN slate_type TEXT DEFAULT 'Main'")
    except sqlite3.OperationalError:
        pass
        
    cursor.execute("DELETE FROM theoretical_bets WHERE slate_type = 'Showdown'")
    
    props = get_top_props()
    if not props:
        print("[ERROR] No props found. Run Chunk 2 first.")
        return
        
    parlays = build_same_game_parlays(props)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for p in parlays:
        cursor.execute("""
            INSERT INTO theoretical_bets (ticket_id, slate_type, legs, weight_class, ticket_json, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (p["ticket_id"], "Showdown", p["legs"], p["weight"], json.dumps(p["props"]), now))
        
    conn.commit()
    conn.close()
    
    print("=== CHUNK 4 COMPLETE: SHOWDOWN PARLAY ENGINE ===")
    print(f"[TICKET BUILDER] Generated {len(parlays)} Same Game Parlays.")
    print("[LEVERAGE] Applied probability weighting (Heavy 2-leggers, Lotto 6-leggers).")
    print("[LEDGER] Tickets officially locked into Donna's theoretical_bets table.")

if __name__ == "__main__":
    log_parlays()
