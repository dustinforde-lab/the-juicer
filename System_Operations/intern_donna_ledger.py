import sqlite3
from datetime import datetime

DB_FILE = "action_grid.db"

def populate_donna_ledger():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM theoretical_bets WHERE bet_type IN ('JUICE_PROP', 'DFS_CONTEST') AND result = 'PENDING'")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tickets = []
    
    cursor.execute("SELECT player, stat_category, consensus_line, rank FROM player_rankings ORDER BY rank ASC LIMIT 25")
    top_props = cursor.fetchall()
    
    for prop in top_props:
        details = f"{prop[0]} OVER {prop[2]} {prop[1]} (Rank {prop[3]})"
        tickets.append(("JUICE_PROP", details, 50.0, "PENDING", now))
        
    cursor.execute("SELECT lineup_num, qb, rb1, rb2, wr1, wr2, wr3, te, flex, dst FROM dfs_lineups")
    dfs_lineups = cursor.fetchall()
    
    for lineup in dfs_lineups:
        details = f"DK Lineup #{lineup[0]}: {lineup[1]}, {lineup[2]}, {lineup[4]}, {lineup[7]}..."
        tickets.append(("DFS_CONTEST", details, 20.0, "PENDING", now))
        
    cursor.executemany('''
        INSERT INTO theoretical_bets (bet_type, details, stake, result, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', tickets)
    
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM theoretical_bets WHERE result = 'PENDING'")
    total_pending = cursor.fetchone()[0]
    conn.close()
    
    print("=== INTERN 5 (DONNA LEDGER): SUCCESS ===")
    print(f"[PORTFOLIO LOCKED] Added Top 25 Juice Props and 200 DFS Lineups to Donna's theoretical ledger.")
    print(f"[TOTAL TICKETS] Donna is now actively tracking {total_pending} pending tickets for Week 2 kickoff.")

if __name__ == "__main__":
    populate_donna_ledger()
