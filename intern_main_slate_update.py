import sqlite3
from datetime import datetime

DB_FILE = "action_grid.db"

WR_INTEL = [
    {"id": "ceedee_lamb_dal", "name": "CeeDee Lamb", "team": "DAL", "opp": "WAS", "salary": 7300, "proj": 21.5, "tag": "Zone Smasher"},
    {"id": "chris_olave_no", "name": "Chris Olave", "team": "NO", "opp": "BAL", "salary": 7200, "proj": 19.8, "tag": "High Vol (Monitor Medical)"},
    {"id": "zay_flowers_bal", "name": "Zay Flowers", "team": "BAL", "opp": "NO", "salary": 6700, "proj": 16.5, "tag": "Q - Hamstring (Check Fri)"},
    {"id": "mike_evans_sf", "name": "Mike Evans", "team": "SF", "opp": "MIA", "salary": 6600, "proj": 18.2, "tag": "Single-High Mismatch"},
    {"id": "parker_washington_jax", "name": "Parker Washington", "team": "JAX", "opp": "DEN", "salary": 5900, "proj": 15.0, "tag": "Man-Coverage Elusive"},
    {"id": "luther_burden_chi", "name": "Luther Burden", "team": "CHI", "opp": "MIN", "salary": 5700, "proj": 16.8, "tag": "Blitz Beater (WR1 Upside)"},
    {"id": "romeo_doubs_ne", "name": "Romeo Doubs", "team": "NE", "opp": "PIT", "salary": 5000, "proj": 14.2, "tag": "Elevated WR1 (AJB Out)"},
    {"id": "matthew_golden_gb", "name": "Matthew Golden", "team": "GB", "opp": "NYJ", "salary": 4700, "proj": 12.5, "tag": "Rookie Vol (82% Snap)"},
    {"id": "devaughn_vele_no", "name": "Devaughn Vele", "team": "NO", "opp": "BAL", "salary": 4200, "proj": 10.1, "tag": "Pace-Up Punt"},
    {"id": "caleb_douglas_mia", "name": "Caleb Douglas", "team": "MIA", "opp": "SF", "salary": 3700, "proj": 8.5, "tag": "Min-Price Deep Threat"},
    {"id": "jaylin_noel_hou", "name": "Jaylin Noel", "team": "HOU", "opp": "CIN", "salary": 3700, "proj": 11.0, "tag": "Slot Funnel (Nico Injured)"}
]

def execute():
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sunday_wr_intel (
                player_id TEXT PRIMARY KEY,
                name TEXT, team TEXT, opp TEXT,
                salary INTEGER, proj REAL, leverage_tag TEXT,
                updated_at TEXT
            )
        """)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for wr in WR_INTEL:
            cur.execute("""
                INSERT OR REPLACE INTO sunday_wr_intel 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (wr["id"], wr["name"], wr["team"], wr["opp"], wr["salary"], wr["proj"], wr["tag"], now))
        conn.commit()
    print("=== SUNDAY MAIN SLATE WR INTEL INGESTED ===")
    print("[INJURY FLAGS APPLIED] Z. Flowers (Hamstring), R. Doubs (AJ Brown OUT), J. Noel (Nico Collins Q).")
    print("[LEVERAGE TAGS APPLIED] Burden (Blitz), Evans (Single-High), Lamb (Zone).")

if __name__ == "__main__":
    execute()
