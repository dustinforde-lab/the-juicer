import sqlite3
import os
from datetime import datetime

DB_FILE = "action_grid.db"

def run_week2_ingestion():
    print("=" * 65)
    print("🧠 [INTELLIGENCE DROP] Ingesting Week 2 DFS & Weather Data...")
    print("=" * 65)
    
    if not os.path.exists(DB_FILE):
        print(f"❌ Error: {DB_FILE} not found.")
        return

    try:
        with sqlite3.connect(DB_FILE) as conn:
            cur = conn.cursor()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 1. THE PURGE: Clear out the sandbox data
            cur.execute("DELETE FROM theoretical_bets")
            cur.execute("DELETE FROM ownership_projections")
            # Keep agent_chatter but we will flood it with new Week 2 data
            print("   ✅ Sandbox data (Bo Nix/Sutton) purged.")

            # 2. DONNA'S DFS ENGINE: Inject Week 2 Ownership & Vibe Ratings
            week2_dfs = [
                ("Bijan Robinson", "ATL", "45.0%", "FADE (CHALK)", timestamp),
                ("Derrick Henry", "BAL", "33.0%", "FADE (CHALK)", timestamp),
                ("De'Von Achane", "MIA", "12.0%", "SMASH (LEVERAGE)", timestamp),
                ("Caleb Williams", "CHI", "7.0%", "SMASH (CORE 4)", timestamp),
                ("Dak Prescott", "DAL", "24.0%", "FADE (CHALK)", timestamp),
                ("Justin Jefferson", "MIN", "18.0%", "SMASH", timestamp),
                ("Luther Burden", "CHI", "24.0%", "SMASH (CASH)", timestamp),
                ("Luke Farrell", "SF", "3.0%", "SMASH (PUNT TE)", timestamp),
                ("Kyle Pitts", "ATL", "9.0%", "SMASH (CONTRARIAN)", timestamp),
                ("Mark Andrews", "BAL", "39.0%", "FADE (CHALK)", timestamp)
            ]
            
            cur.executemany(
                "INSERT INTO ownership_projections (player_name, team, projected_ownership, vibe_rating, updated_at) VALUES (?, ?, ?, ?, ?)",
                week2_dfs
            )
            print("   ✅ Donna's Leverage Matrix updated with Week 2 Projections.")

            # 3. FILM ROOM TELEMETRY: Broadcast Week 2 Insights to the dashboard
            chatter = [
                ("METEOROLOGIST", "WEATHER SHOCK: 40% chance of rain at Soldier Field (MIN @ CHI). Field will be soggy and slow. Adjusting game scripts.", "MIN/CHI Game", "ADJUST", timestamp),
                ("METEOROLOGIST", "WEATHER SHOCK: Rain showers likely in Tampa Bay (CLE @ TB). Potential for paused play. Downgrading passing attacks.", "CLE/TB Game", "ADJUST", timestamp),
                ("DONNA", "DFS VIBE CHECK: Bijan Robinson hitting massive 45% FD ownership. Pivoting to De'Von Achane (MIA) against weak SF run defense for leverage.", "De'Von Achane", "SMASH", timestamp),
                ("DONNA", "DFS VIBE CHECK: Luke Farrell ($2500 DK) identified as elite punt TE to open salary for premium RBs. Locked for Cash Core 4.", "Luke Farrell", "LOCK", timestamp),
                ("RECIPE BOOK", "CORRELATION BUILT: Caleb Williams + Luther Burden (CHI). Fading the weather concerns based on offensive playcalling volume.", "CHI Stack", "STACK_BUILT", timestamp)
            ]
            
            cur.executemany(
                "INSERT INTO agent_chatter (sender, directive, target, action, timestamp) VALUES (?, ?, ?, ?, ?)",
                chatter
            )
            print("   ✅ Syndicate Agents broadcasted Week 2 intelligence to the Film Room.")
            
            conn.commit()
            
    except Exception as e:
        print(f"   ❌ Execution Failed: {e}")

    print("=" * 65)
    print("🟢 INGESTION COMPLETE: The Juicer is locked onto Week 2.")
    print("=" * 65)

if __name__ == "__main__":
    run_week2_ingestion()
