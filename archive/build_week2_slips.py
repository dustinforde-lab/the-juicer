import sqlite3
import os
import json
from datetime import datetime

DB_FILE = "action_grid.db"

def build_week2_slips():
    print("=" * 65)
    print("🎯 [THE RECIPE BOOK] Generating Week 2 Correlated Slips...")
    print("=" * 65)
    
    if not os.path.exists(DB_FILE):
        print(f"❌ Error: {DB_FILE} not found.")
        return

    try:
        with sqlite3.connect(DB_FILE) as conn:
            cur = conn.cursor()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Slip 1: Chicago Volume Stack
            legs_chi = [
                {"player": "Caleb Williams", "team": "CHI", "stat": "Pass Yds > 245.5"},
                {"player": "Luther Burden", "team": "CHI", "stat": "Rec Yds > 62.5"},
                {"player": "Rome Odunze", "team": "CHI", "stat": "Receptions > 4.5"}
            ]
            cur.execute(
                """INSERT OR REPLACE INTO theoretical_bets 
                (ticket_id, weight_class, odds, border_color, ticket_json, source, created_at, confidence_score) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                ("DK-STACK-CHI-02", "3-LEG CORRELATION", "+420", "#00ff88", json.dumps(legs_chi), "DraftKings", timestamp, 88)
            )

            # Slip 2: The Leverage Punt
            legs_lev = [
                {"player": "De'Von Achane", "team": "MIA", "stat": "Rush Yds > 75.5"},
                {"player": "Luke Farrell", "team": "SF", "stat": "Receptions > 2.5"}
            ]
            cur.execute(
                """INSERT OR REPLACE INTO theoretical_bets 
                (ticket_id, weight_class, odds, border_color, ticket_json, source, created_at, confidence_score) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                ("FD-LEV-01", "2-LEG LEVERAGE", "+280", "#107aca", json.dumps(legs_lev), "FanDuel", timestamp, 92)
            )

            # Slip 3: Dallas Bounce Back
            legs_dal = [
                {"player": "Dak Prescott", "team": "DAL", "stat": "Pass Yds > 275.5"},
                {"player": "CeeDee Lamb", "team": "DAL", "stat": "Rec Yds > 85.5"},
                {"player": "Javonte Williams", "team": "DAL", "stat": "Rush Yds > 60.5"}
            ]
            cur.execute(
                """INSERT OR REPLACE INTO theoretical_bets 
                (ticket_id, weight_class, odds, border_color, ticket_json, source, created_at, confidence_score) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                ("MGM-CORE-03", "3-LEG CORRELATION", "+390", "#fdb927", json.dumps(legs_dal), "BetMGM", timestamp, 85)
            )

            conn.commit()
            print("   ✅ The Recipe Book successfully assembled 3 high-value Week 2 tickets.")
            
    except Exception as e:
        print(f"   ❌ Execution Failed: {e}")

    print("=" * 65)

if __name__ == "__main__":
    build_week2_slips()
