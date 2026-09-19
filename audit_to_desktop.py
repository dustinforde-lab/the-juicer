import sqlite3
import os
import subprocess
import json
from datetime import datetime

DB_FILE = "action_grid.db"

# Robust Desktop path resolution (handles OneDrive redirection)
user_home = os.path.expanduser("~")
desktop_candidates = [
    os.path.join(user_home, "Desktop"),
    os.path.join(user_home, "OneDrive", "Desktop"),
    os.path.join(user_home, "OneDrive - Personal", "Desktop")
]

desktop_path = None
for candidate in desktop_candidates:
    if os.path.exists(candidate):
        desktop_path = candidate
        break

if not desktop_path:
    # Fallback to standard user home if desktop isn't found
    desktop_path = user_home

os.makedirs(desktop_path, exist_ok=True)
output_file = os.path.join(desktop_path, "Chuck's Mad Audit.txt")

def log(msg, file_handle):
    file_handle.write(msg + "\n")
    print(msg)

def run_file_audit():
    with open(output_file, "w", encoding="utf-8") as f:
        log("=" * 70, f)
        log(f"🕵️ CHUCK'S MAD AUDIT - RUNTIME: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", f)
        log("=" * 70, f)
        
        if not os.path.exists(DB_FILE):
            log(f"❌ Database {DB_FILE} not found.", f)
            return

        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()

        # 1. Inspect All Tables
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cur.fetchall()]
        log(f"\n📦 TOTAL TABLES IN DATABASE: {len(tables)}", f)
        for t in tables:
            cur.execute(f"SELECT COUNT(*) FROM [{t}]")
            count = cur.fetchone()[0]
            log(f"   • {t}: {count} total rows", f)
        log("-" * 70, f)

        # 2. Audit Stored Betting Lines / Market Odds (theoretical_bets)
        log("\n🎰 AUDIT: Stored Betting Lines & Odds (theoretical_bets)", f)
        if "theoretical_bets" in tables:
            cur.execute("SELECT ticket_id, weight_class, odds, source, created_at, ticket_json FROM theoretical_bets")
            slips = cur.fetchall()
            if slips:
                for ticket_id, weight, odds, source, created_at, t_json in slips:
                    log(f"   [{source}] {ticket_id} | {weight} | Odds: {odds} | Locked: {created_at}", f)
                    try:
                        legs = json.loads(t_json)
                        for leg in legs:
                            log(f"       ↳ {leg.get('player', 'Unknown')} ({leg.get('team', '')}): {leg.get('stat', '')}", f)
                    except:
                        log(f"       ↳ Raw: {t_json}", f)
            else:
                log("   ⚠️ No betting slips currently exist in theoretical_bets.", f)
        else:
            log("   ❌ theoretical_bets table does not exist.", f)
        log("-" * 70, f)

        # 3. Audit Agent Chatter
        log("\n🗣️ AUDIT: Syndicate Agent Activity (agent_chatter)", f)
        if "agent_chatter" in tables:
            cur.execute("SELECT sender, action, target, directive, timestamp FROM agent_chatter ORDER BY message_id DESC LIMIT 30")
            logs = cur.fetchall()
            if logs:
                for sender, action, target, directive, ts in logs:
                    log(f"   [{ts}] [{sender}] ({action}) -> Target: {target}", f)
                    log(f"       Directive: {directive}", f)
            else:
                log("   ⚠️ No chatter records found.", f)
        else:
            log("   ❌ agent_chatter table does not exist.", f)
        log("-" * 70, f)

        # 4. Audit DFS Ownership Matrix
        log("\n👑 AUDIT: Donna's Ownership Projections & Vibe Ratings", f)
        if "ownership_projections" in tables:
            cur.execute("SELECT player_name, team, projected_ownership, vibe_rating, updated_at FROM ownership_projections ORDER BY updated_at DESC")
            proj = cur.fetchall()
            if proj:
                for name, team, own, vibe, ts in proj:
                    log(f"   • {name} ({team}) | Proj Own: {own:<6} | Rating: {vibe:<18} | Updated: {ts}", f)
            else:
                log("   ⚠️ No projections found.", f)
        else:
            log("   ❌ ownership_projections table does not exist.", f)
        log("-" * 70, f)

        # 5. Audit Other Hidden/Legacy Tables
        other_tables = [t for t in tables if t not in ["theoretical_bets", "agent_chatter", "ownership_projections", "raw_slate_articles", "sqlite_sequence"]]
        if other_tables:
            log(f"\n🔍 AUDIT: Other Active/Legacy Tables ({', '.join(other_tables)})", f)
            for ot in other_tables:
                log(f"\n   --- Table: {ot} ---", f)
                cur.execute(f"PRAGMA table_info([{ot}])")
                cols = [col[1] for col in cur.fetchall()]
                log(f"   Columns: {cols}", f)
                cur.execute(f"SELECT * FROM [{ot}] LIMIT 10")
                sample = cur.fetchall()
                for row in sample:
                    log(f"   {row}", f)
        else:
            log("\n🔍 AUDIT: No other supplementary data tables found in database.", f)
        log("-" * 70, f)

        conn.close()

        # 6. Audit Running Processes
        log("\n🖥️ AUDIT: Active Python Processes Running on Host Machine", f)
        try:
            output = subprocess.check_output('tasklist /FI "IMAGENAME eq python.exe" /FO TABLE', shell=True).decode()
            log(output.strip(), f)
        except Exception as e:
            log(f"   ❌ Could not query process list: {e}", f)
        
        log("=" * 70, f)
        log(f"✅ REPORT SUCCESSFULLY WRITTEN TO: {output_file}", f)
        log("=" * 70, f)

if __name__ == "__main__":
    run_file_audit()
