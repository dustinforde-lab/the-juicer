import sqlite3
import os
import subprocess
import json

DB_FILE = "action_grid.db"

def run_full_backend_audit():
    print("=" * 70)
    print("🕵️ FULL BACKEND & SYSTEM REALITY AUDIT")
    print("=" * 70)
    
    if not os.path.exists(DB_FILE):
        print(f"❌ Database {DB_FILE} not found.")
        return

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    # 1. Inspect All Tables in action_grid.db
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cur.fetchall()]
    print(f"📦 Total Tables in Database: {len(tables)}")
    for t in tables:
        cur.execute(f"SELECT COUNT(*) FROM [{t}]")
        count = cur.fetchone()[0]
        print(f"   • {t}: {count} total rows")
    print("-" * 70)

    # 2. Audit Stored Vegas Lines / Market Odds (theoretical_bets)
    print("🎰 AUDIT: Stored Betting Lines & Odds (theoretical_bets)")
    if "theoretical_bets" in tables:
        cur.execute("SELECT ticket_id, weight_class, odds, source, created_at, ticket_json FROM theoretical_bets")
        slips = cur.fetchall()
        if slips:
            for ticket_id, weight, odds, source, created_at, t_json in slips:
                print(f"   [{source}] {ticket_id} | {weight} | Odds: {odds} | Locked: {created_at}")
                try:
                    legs = json.loads(t_json)
                    for leg in legs:
                        print(f"       ↳ {leg.get('player', 'Unknown')} ({leg.get('team', '')}): {leg.get('stat', '')}")
                except:
                    print(f"       ↳ Raw: {t_json}")
        else:
            print("   ⚠️ No betting slips currently exist in theoretical_bets.")
    else:
        print("   ❌ theoretical_bets table does not exist.")
    print("-" * 70)

    # 3. Audit Agent Chatter & Evaluation Logs (Mike, Lewis, Donna)
    print("🗣️ AUDIT: Syndicate Agent Activity (agent_chatter)")
    if "agent_chatter" in tables:
        cur.execute("SELECT sender, action, target, directive, timestamp FROM agent_chatter ORDER BY message_id DESC LIMIT 15")
        logs = cur.fetchall()
        if logs:
            for sender, action, target, directive, ts in logs:
                print(f"   [{ts}] [{sender}] ({action}) -> Target: {target}")
                print(f"       Directive: {directive}")
        else:
            print("   ⚠️ No chatter records found.")
    else:
        print("   ❌ agent_chatter table does not exist.")
    print("-" * 70)

    # 4. Audit DFS Ownership & Leverage Matrix (ownership_projections)
    print("👑 AUDIT: Donna's Ownership Projections & Vibe Ratings")
    if "ownership_projections" in tables:
        cur.execute("SELECT player_name, team, projected_ownership, vibe_rating, updated_at FROM ownership_projections ORDER BY updated_at DESC")
        proj = cur.fetchall()
        if proj:
            for name, team, own, vibe, ts in proj:
                print(f"   • {name} ({team}) | Proj Own: {own:<6} | Rating: {vibe:<18} | Updated: {ts}")
        else:
            print("   ⚠️ No projections found.")
    else:
        print("   ❌ ownership_projections table does not exist.")
    print("-" * 70)

    # 5. Audit Any Other Data Tables (Excluding raw_slate_articles)
    other_tables = [t for t in tables if t not in ["theoretical_bets", "agent_chatter", "ownership_projections", "raw_slate_articles", "sqlite_sequence"]]
    if other_tables:
        print(f"🔍 AUDIT: Other Active Tables ({', '.join(other_tables)})")
        for ot in other_tables:
            print(f"\n   --- Table: {ot} ---")
            cur.execute(f"PRAGMA table_info([{ot}])")
            cols = [col[1] for col in cur.fetchall()]
            print(f"   Columns: {cols}")
            cur.execute(f"SELECT * FROM [{ot}] LIMIT 5")
            sample = cur.fetchall()
            for row in sample:
                print(f"   {row}")
    else:
        print("🔍 AUDIT: No other supplementary data tables found in database.")
    print("-" * 70)

    conn.close()

    # 6. Audit System Running Processes (Looking for active scrapers/daemons)
    print("🖥️ AUDIT: Active Python Processes Running on Host Machine")
    try:
        output = subprocess.check_output('tasklist /FI "IMAGENAME eq python.exe" /FO TABLE', shell=True).decode()
        print(output.strip())
    except Exception as e:
        print(f"   ❌ Could not query process list: {e}")
    print("=" * 70)

if __name__ == "__main__":
    run_full_backend_audit()
