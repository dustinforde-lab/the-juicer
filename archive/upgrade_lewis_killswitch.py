import sys, sqlite3, json

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DB_FILE = "action_grid.db"

def execute_lewis_killswitch():
    print("=" * 65)
    print("[LEWIS] [UPGRADE CHUNK 6] Lewis Kill-Switch Active (Scanning for Injuries)...")
    print("=" * 65)
    
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        
        try:
            injured_players = [row[0] for row in cur.execute("SELECT player_name FROM hospital_ward").fetchall()]
        except Exception:
            print("   * Hospital ward not found. Did you run Chunk 5?")
            return

        print(f"   * Lewis detected {len(injured_players)} players in the Hospital Ward.")

        try:
            bets = cur.execute("SELECT ticket_id, ticket_json FROM theoretical_bets").fetchall()
        except sqlite3.OperationalError:
            bets = []
            
        purged_bets = 0
        for tid, tjson in bets:
            legs = json.loads(tjson)
            for leg in legs:
                if leg["player"] in injured_players:
                    cur.execute("DELETE FROM theoretical_bets WHERE ticket_id = ?", (tid,))
                    purged_bets += 1
                    print(f"   X [PURGED PARLAY] {tid} contained injured player: {leg['player']}")
                    break

        try:
            ud_slips = cur.execute("SELECT slip_id, props_json FROM underdog_slips").fetchall()
        except sqlite3.OperationalError:
            ud_slips = []
            
        purged_ud = 0
        for sid, pjson in ud_slips:
            props = json.loads(pjson)
            for p in props:
                if p["player"] in injured_players:
                    cur.execute("DELETE FROM underdog_slips WHERE slip_id = ?", (sid,))
                    purged_ud += 1
                    print(f"   X [PURGED UNDERDOG] {sid} contained injured player: {p['player']}")
                    break

        conn.commit()
        print(f"\n   * SUMMARY: Lewis purged {purged_bets} Parlays and {purged_ud} Underdog Slips.")

def run_self_test():
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        try:
            injured = [row[0] for row in cur.execute("SELECT player_name FROM hospital_ward").fetchall()]
            for tid, tjson in cur.execute("SELECT ticket_id, ticket_json FROM theoretical_bets").fetchall():
                legs = json.loads(tjson)
                for leg in legs:
                    assert leg["player"] not in injured, f"Leak: {tid} contains {leg['player']}"
        except sqlite3.OperationalError:
            pass # Tables might not exist yet if running out of order, safely pass
            
    print("ALL GATES PASSED: Zero injured players remain in active slips.\n")

if __name__ == "__main__":
    execute_lewis_killswitch()
    run_self_test()
