import sqlite3
import json
from datetime import datetime

DB_FILE = "action_grid.db"

def setup_schema():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 1. Permanent Player Registry for Canonical Entity Resolution
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS master_players (
            canonical_id TEXT PRIMARY KEY,
            clean_name TEXT NOT NULL,
            team TEXT NOT NULL,
            position TEXT NOT NULL,
            aliases TEXT,
            updated_at TEXT
        )
    """)
    
    # 2. Multi-Sportsbook Odds & Quotes Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sportsbook_quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            canonical_id TEXT NOT NULL,
            player_name TEXT NOT NULL,
            sportsbook TEXT NOT NULL,
            stat_category TEXT NOT NULL,
            line REAL,
            over_odds INTEGER,
            under_odds INTEGER,
            week INTEGER DEFAULT 2,
            timestamp TEXT,
            FOREIGN KEY(canonical_id) REFERENCES master_players(canonical_id)
        )
    """)
    
    # 3. Winning Contest Benchmarks (for Donna's Post-Slate Learning)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contest_results (
            contest_id TEXT PRIMARY KEY,
            slate_type TEXT NOT NULL,
            week INTEGER NOT NULL,
            winning_score REAL,
            cash_line_score REAL,
            salary_remaining REAL,
            winning_lineup_json TEXT,
            top_captain_position TEXT,
            timestamp TEXT
        )
    """)
    
    # Seed core TNF players for entity resolution
    core_players = [
        ("josh_allen_buf_qb", "Josh Allen", "BUF", "QB", json.dumps(["Josh Allen", "J. Allen", "J.Allen"])),
        ("jared_goff_det_qb", "Jared Goff", "DET", "QB", json.dumps(["Jared Goff", "J. Goff", "J.Goff"])),
        ("jahmyr_gibbs_det_rb", "Jahmyr Gibbs", "DET", "RB", json.dumps(["Jahmyr Gibbs", "J. Gibbs"])),
        ("david_montgomery_det_rb", "David Montgomery", "DET", "RB", json.dumps(["David Montgomery", "D. Montgomery"])),
        ("james_cook_buf_rb", "James Cook", "BUF", "RB", json.dumps(["James Cook", "J. Cook"])),
        ("amon_ra_st_brown_det_wr", "Amon-Ra St. Brown", "DET", "WR", json.dumps(["Amon-Ra St. Brown", "A. St. Brown", "Amon-Ra St Brown"])),
        ("jameson_williams_det_wr", "Jameson Williams", "DET", "WR", json.dumps(["Jameson Williams", "J. Williams"])),
        ("khalil_shakir_buf_wr", "Khalil Shakir", "BUF", "WR", json.dumps(["Khalil Shakir", "K. Shakir"])),
        ("keon_coleman_buf_wr", "Keon Coleman", "BUF", "WR", json.dumps(["Keon Coleman", "K. Coleman"])),
        ("sam_laporta_det_te", "Sam LaPorta", "DET", "TE", json.dumps(["Sam LaPorta", "S. LaPorta"])),
        ("dalton_kincaid_buf_te", "Dalton Kincaid", "BUF", "TE", json.dumps(["Dalton Kincaid", "D. Kincaid"])),
        ("jake_bates_det_k", "Jake Bates", "DET", "K", json.dumps(["Jake Bates", "J. Bates"])),
        ("tyler_bass_buf_k", "Tyler Bass", "BUF", "K", json.dumps(["Tyler Bass", "T. Bass"])),
        ("det_dst", "Lions Defense", "DET", "DST", json.dumps(["Lions", "Detroit Lions", "DET DST"])),
        ("buf_dst", "Bills Defense", "BUF", "DST", json.dumps(["Bills", "Buffalo Bills", "BUF DST"]))
    ]
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for p in core_players:
        cursor.execute("""
            INSERT INTO master_players (canonical_id, clean_name, team, position, aliases, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(canonical_id) DO UPDATE SET
                clean_name = excluded.clean_name,
                team = excluded.team,
                position = excluded.position,
                aliases = excluded.aliases,
                updated_at = excluded.updated_at
        """, (p[0], p[1], p[2], p[3], p[4], now))
        
    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM master_players")
    total_players = cursor.fetchone()[0]
    conn.close()
    
    print("=== CHUNK 1 COMPLETE: MASTER SCHEMA INITIALIZED ===")
    print(f"[ENTITY REGISTRY] master_players seeded with {total_players} canonical profiles.")
    print("[ODDS STORE] sportsbook_quotes table configured for multi-book pricing.")
    print("[AUDIT BENCHMARK] contest_results table ready for DraftKings winning lineups.")

if __name__ == "__main__":
    setup_schema()
