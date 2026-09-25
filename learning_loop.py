# -*- coding: utf-8 -*-
import sqlite3
from datetime import datetime
import address_book

def fetch_actual_box_scores():
    """Simulates fetching real box scores via ESPN API to grade the week."""
    # In production, this pings the ESPN box score endpoint.
    return {
        "Josh Allen": 26.4, "Bijan Robinson": 19.8, "Jordan Love": 28.2, 
        "CeeDee Lamb": 14.5, "Breece Hall": 22.1, "Jayden Reed": 12.0
    }

def grade_weekly_picks():
    """Weekly auto-grade of projections vs actuals."""
    db_path = address_book.PATHS.get("DATABASE", "action_grid.db")
    try:
        actuals = fetch_actual_box_scores()
        
        with sqlite3.connect(db_path) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS pick_grades (id INTEGER PRIMARY KEY, player TEXT, projected REAL, actual REAL, delta REAL, hit INTEGER, graded_at TEXT)")
            
            # Fetch active projections from our system
            df = conn.execute("SELECT Player, Mike_PPR FROM dfs_projections LIMIT 10").fetchall()
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            for row in df:
                player, proj = row[0], row[1]
                if player in actuals:
                    actual_pts = actuals[player]
                    delta = round(actual_pts - proj, 1)
                    hit = 1 if abs(delta) <= 4.0 else 0 # Evaluator hit threshold
                    
                    conn.execute("""
                        INSERT INTO pick_grades (player, projected, actual, delta, hit, graded_at) 
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (player, proj, actual_pts, delta, hit, now_str))
            conn.commit()
        return True
    except Exception as e:
        print(f"Grader Error: {e}")
        return False
