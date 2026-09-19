import sqlite3
import random
from datetime import datetime

DB_FILE = "action_grid.db"

def build_parlays(num_tickets=250):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS theoretical_bets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bet_type TEXT,
            details TEXT,
            stake REAL,
            result TEXT,
            timestamp TEXT
        )
    """)
    cursor.execute("DELETE FROM theoretical_bets WHERE bet_type LIKE 'PARLAY_%' AND result = 'PENDING'")
    
    cursor.execute("SELECT player, stat_category, consensus_line FROM player_rankings ORDER BY rank ASC LIMIT 40")
    top_props = cursor.fetchall()
    
    if not top_props:
        top_props = [("Jahmyr Gibbs", "RUSH_YDS", 55.5), ("Amon-Ra St. Brown", "RECEPTIONS", 7.5), ("Josh Allen", "PASS_YDS", 262.5), ("Jameson Williams", "RECEPTIONS", 4.5)]
        
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tickets = []
    
    for i in range(1, num_tickets + 1):
        if i <= 100:
            legs = random.choice([2, 3])
            stake = 100.0 if legs == 2 else 75.0
        elif i <= 200:
            legs = random.choice([4, 5])
            stake = 25.0 if legs == 4 else 15.0
        else:
            legs = random.randint(6, 10)
            stake = round(10.0 / (legs - 4), 2)
            
        ticket_props = random.sample(top_props, legs)
        details = " | ".join([f"{p[0]} O {p[2]} {p[1]}" for p in ticket_props])
        bet_type = f"PARLAY_{legs}LEG"
        
        tickets.append((bet_type, details, stake, "PENDING", now))
        
    cursor.executemany("""
        INSERT INTO theoretical_bets (bet_type, details, stake, result, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, tickets)
    
    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM theoretical_bets WHERE bet_type LIKE 'PARLAY_%'")
    total = cursor.fetchone()[0]
    conn.close()
    
    print("=== INTERN 4 (PARLAY BUILDER): SUCCESS ===")
    print(f"[LEDGER] Logged {total} weighted theoretical parlays for Donna to grade.")
    print(f"[SAMPLE TICKET] {tickets[0][0]} (${tickets[0][2]}): {tickets[0][1]}")

if __name__ == "__main__":
    build_parlays(250)
