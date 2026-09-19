import sqlite3
import os
from datetime import datetime

DB_FILE = "action_grid.db"

def run_injury_ingestion():
    print("=" * 65)
    print("🚑 [INTELLIGENCE DROP] Ingesting Week 2 Injury Report...")
    print("=" * 65)
    
    if not os.path.exists(DB_FILE):
        print(f"❌ Error: {DB_FILE} not found.")
        return

    try:
        with sqlite3.connect(DB_FILE) as conn:
            cur = conn.cursor()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 1. LEWIS - RISK & PURGE ALERTS
            # 2. MIKE - CONFIDENCE BOOSTS
            
            chatter = [
                ("LEWIS", "INJURY PURGE: Kyler Murray (Concussion) OUT. Purging Murray props. Carson Wentz officially starting.", "Kyler Murray", "PURGE", timestamp),
                ("MIKE", "CONFIDENCE UPGRADE: Wentz threw 3 TDs in Week 1. Heavy target funnel to Justin Jefferson anticipated. Confidence boosted to 94.", "Justin Jefferson", "ADJUST", timestamp),
                
                ("LEWIS", "INJURY PURGE: Zay Flowers (Hamstring) DOUBTFUL. Flagging for removal.", "Zay Flowers", "PURGE", timestamp),
                ("MIKE", "CONFIDENCE UPGRADE: Mark Andrews (6 targets in Wk 1) and Rashod Bateman seeing target spikes with Flowers sidelined.", "Mark Andrews", "ADJUST", timestamp),
                
                ("LEWIS", "INJURY PURGE: Nico Collins (Hamstring) OUT. Stripping Collins from theoretical parlays.", "Nico Collins", "PURGE", timestamp),
                ("MIKE", "CONFIDENCE UPGRADE: Kayshon Boutte and Dalton Schultz target volume increased in high-pass script vs CIN.", "HOU Receivers", "ADJUST", timestamp),

                ("LEWIS", "INJURY PURGE: Brock Bowers (Knee) DOUBTFUL. Purging Bowers from all models.", "Brock Bowers", "PURGE", timestamp),
                ("MIKE", "CONFIDENCE UPGRADE: Michael Mayer led LV in Week 1 targets. Status locked as TE1 vs LAC.", "Michael Mayer", "ADJUST", timestamp),

                ("LEWIS", "INJURY PURGE: Kaelon Black (Groin) QUESTIONABLE. If out, Christian McCaffrey touch volume skyrockets.", "Christian McCaffrey", "ADJUST", timestamp),
                ("MIKE", "CONFIDENCE UPGRADE: TreVeyon Henderson is fully ACTIVE for New England. Adjusting NE backfield splits.", "TreVeyon Henderson", "ADJUST", timestamp),

                ("LEWIS", "INJURY DOWNGRADE: ATL offense heavily compromised. Tua Tagovailoa DOUBTFUL, Penix OUT. Cooper Rush starting.", "ATL Offense", "ADJUST", timestamp),
                ("MIKE", "CONFIDENCE UPGRADE: Chig Okonkwo OUT. John Bates stepping up (3 targets from Daniels in Wk 1).", "John Bates", "ADJUST", timestamp)
            ]
            
            cur.executemany(
                "INSERT INTO agent_chatter (sender, directive, target, action, timestamp) VALUES (?, ?, ?, ?, ?)",
                chatter
            )
            print("   ✅ Lewis and Mike processed the casualty list and updated the Film Room.")
            
            conn.commit()
            
    except Exception as e:
        print(f"   ❌ Execution Failed: {e}")

    print("=" * 65)
    print("🟢 INJURY INGESTION COMPLETE: The Juicer has adapted to the Week 2 injury landscape.")
    print("=" * 65)

if __name__ == "__main__":
    run_injury_ingestion()
