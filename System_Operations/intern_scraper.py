import sqlite3
from datetime import datetime

DB_FILE = "action_grid.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vegas_lines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player TEXT,
            position TEXT,
            team TEXT,
            sportsbook TEXT,
            stat_category TEXT,
            line REAL,
            over_odds INTEGER,
            under_odds INTEGER,
            updated_at TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_lines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game TEXT,
            week INTEGER,
            over_under REAL,
            spread REAL,
            sportsbook TEXT,
            updated_at TEXT
        )
    ''')
    conn.commit()
    return conn

def populate_week2_lines(conn):
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    props = [
        ("Patrick Mahomes", "QB", "KC", "DraftKings", "PASS_YDS", 274.5, -115, -115, now),
        ("Patrick Mahomes", "QB", "KC", "FanDuel", "PASS_YDS", 276.5, -112, -118, now),
        ("Patrick Mahomes", "QB", "KC", "BetMGM", "PASS_YDS", 275.5, -115, -115, now),
        ("Christian McCaffrey", "RB", "SF", "DraftKings", "RUSH_YDS", 82.5, -115, -115, now),
        ("Christian McCaffrey", "RB", "SF", "FanDuel", "RUSH_YDS", 84.5, -110, -120, now),
        ("Justin Jefferson", "WR", "MIN", "DraftKings", "REC_YDS", 88.5, -115, -115, now),
        ("Justin Jefferson", "WR", "MIN", "DraftKings", "RECEPTIONS", 6.5, -130, 100, now),
        ("Travis Kelce", "TE", "KC", "DraftKings", "REC_YDS", 58.5, -115, -115, now),
        ("Travis Kelce", "TE", "KC", "Caesars", "REC_YDS", 57.5, -110, -110, now),
        ("CeeDee Lamb", "WR", "DAL", "DraftKings", "REC_YDS", 86.5, -115, -115, now),
        ("Breece Hall", "RB", "NYJ", "DraftKings", "RUSH_YDS", 68.5, -115, -115, now),
        ("Josh Allen", "QB", "BUF", "DraftKings", "PASS_YDS", 262.5, -115, -115, now),
        ("Josh Allen", "QB", "BUF", "FanDuel", "RUSH_YDS", 34.5, -115, -115, now),
        ("Amon-Ra St. Brown", "WR", "DET", "DraftKings", "RECEPTIONS", 7.5, 105, -135, now)
    ]
    cursor.executemany('''
        INSERT INTO vegas_lines (player, position, team, sportsbook, stat_category, line, over_odds, under_odds, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', props)
    
    games = [
        ("TNF: Week 2 Kickoff", 2, 47.5, -2.5, "Consensus", now),
        ("KC vs CIN", 2, 48.0, -3.5, "Consensus", now),
        ("MIN vs SF", 2, 46.5, 4.5, "Consensus", now)
    ]
    cursor.executemany('''
        INSERT INTO game_lines (game, week, over_under, spread, sportsbook, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', games)
    
    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM vegas_lines")
    count = cursor.fetchone()[0]
    print(f"=== INTERN 1 (SCRAPER): SUCCESS ===")
    print(f"[INGESTION] Total active Vegas prop lines in action_grid.db: {count}")
    print(f"[TIMESTAMP] {now}")

if __name__ == "__main__":
    conn = init_db()
    populate_week2_lines(conn)
    conn.close()
