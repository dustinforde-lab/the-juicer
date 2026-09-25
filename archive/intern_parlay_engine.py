import sqlite3, json
from datetime import datetime

DB_FILE = "action_grid.db"

TICKETS = [
    {
        "ticket_id": "TKT-01",
        "title": "Floor Builder Double",
        "slate_type": "Showdown",
        "legs": 2,
        "weight_class": "Cash Builder",
        "border_color": "#00ff88",
        "odds": "+135",
        "implied_prob": "42.5%",
        "correlation_note": "Script: Floor Anchors // High snap share bellcows in neutral script",
        "props": [
            {"icon": "🎯", "player": "Josh Allen", "stat": "200+ Passing Yards"},
            {"icon": "⚡", "player": "Jahmyr Gibbs", "stat": "50+ Rushing Yards"}
        ]
    },
    {
        "ticket_id": "TKT-02",
        "title": "Bills Aerial Funnel Triple",
        "slate_type": "Showdown",
        "legs": 3,
        "weight_class": "Syndicate Core",
        "border_color": "#00e5ff",
        "odds": "+385",
        "implied_prob": "20.6%",
        "correlation_note": "Script: Shootout // Allen target funnel + ARSB man-coverage volume",
        "props": [
            {"icon": "🎯", "player": "Josh Allen", "stat": "OVER 1.5 Passing TDs"},
            {"icon": "👐", "player": "DJ Moore", "stat": "OVER 58.5 Receiving Yards"},
            {"icon": "👐", "player": "Amon-Ra St. Brown", "stat": "OVER 6.5 Receptions"}
        ]
    },
    {
        "ticket_id": "TKT-03",
        "title": "Detroit Ground Control",
        "slate_type": "Showdown",
        "legs": 3,
        "weight_class": "Syndicate Core",
        "border_color": "#00e5ff",
        "odds": "+420",
        "implied_prob": "19.2%",
        "correlation_note": "Script: Lions Control // Low aDOT underneath pace + Gibbs touches",
        "props": [
            {"icon": "⚡", "player": "Jahmyr Gibbs", "stat": "OVER 74.5 Rush + Rec Yards"},
            {"icon": "🎯", "player": "Jared Goff", "stat": "UNDER 254.5 Passing Yards"},
            {"icon": "👐", "player": "Sam LaPorta", "stat": "OVER 4.5 Receptions"}
        ]
    },
    {
        "ticket_id": "TKT-04",
        "title": "Red Zone Ceiling Lotto",
        "slate_type": "Showdown",
        "legs": 4,
        "weight_class": "Moonshot Whale",
        "border_color": "#ff2a6d",
        "odds": "+850",
        "implied_prob": "10.5%",
        "correlation_note": "Script: High-Octane GPP // High red-zone conversion + air yards regression",
        "props": [
            {"icon": "🏈", "player": "Jahmyr Gibbs", "stat": "Anytime Touchdown"},
            {"icon": "🏈", "player": "Dalton Kincaid", "stat": "Anytime Touchdown"},
            {"icon": "⚡", "player": "James Cook", "stat": "OVER 48.5 Rushing Yards"},
            {"icon": "🚀", "player": "Jameson Williams", "stat": "40+ Receiving Yards"}
        ]
    }
]

def build_parlay_engine():
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS theoretical_bets")
        cur.execute("""
            CREATE TABLE theoretical_bets (
                ticket_id TEXT PRIMARY KEY,
                title TEXT,
                slate_type TEXT,
                legs INTEGER,
                weight_class TEXT,
                border_color TEXT,
                odds TEXT,
                implied_prob TEXT,
                correlation_note TEXT,
                ticket_json TEXT,
                timestamp TEXT
            )
        """)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for t in TICKETS:
            cur.execute("""
                INSERT INTO theoretical_bets VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                t["ticket_id"], t["title"], t["slate_type"], t["legs"],
                t["weight_class"], t["border_color"], t["odds"], t["implied_prob"],
                t["correlation_note"], json.dumps(t["props"]), now
            ))
        conn.commit()
    print(f"=== PARLAY ENGINE INITIALIZED: {len(TICKETS)} SHOWDOWN TICKETS SEEDED ===")

if __name__ == "__main__":
    build_parlay_engine()
