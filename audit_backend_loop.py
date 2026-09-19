import sqlite3
import os
import json
from datetime import datetime

DB_FILE = "action_grid.db"

# Robust Desktop path resolution (handling OneDrive redirection)
user_home = os.path.expanduser("~")
desktop_candidates = [
    os.path.join(user_home, "Desktop"),
    os.path.join(user_home, "OneDrive", "Desktop"),
    os.path.join(user_home, "OneDrive - Personal", "Desktop")
]

desktop_path = next((c for c in desktop_candidates if os.path.exists(c)), user_home)
os.makedirs(desktop_path, exist_ok=True)
output_file = os.path.join(desktop_path, "testing backend loop.txt")

def log(msg, f):
    f.write(msg + "\n")
    print(msg)

def run_loop_audit():
    with open(output_file, "w", encoding="utf-8") as f:
        log("=" * 70, f)
        log(f"🔄 CONTINUOUS LOOP & PORT ROUTING AUDIT - RUNTIME: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", f)
        log("=" * 70, f)
        
        if not os.path.exists(DB_FILE):
            log(f"❌ Database {DB_FILE} not found.", f)
            return

        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()

        # 1. Telemetry Pulse Check (Intern Network & Daemon)
        log("\n📡 1. SYSTEM TELEMETRY & NODE PULSE (Intern Network & Daemon):", f)
        try:
            cur.execute("SELECT node, last_heartbeat, status, records, agent_report FROM system_telemetry")
            for node, hb, status, recs, report in cur.fetchall():
                log(f"   • Node: {node}", f)
                log(f"     Status: {status} | Records: {recs} | Last Pulse: {hb}", f)
                log(f"     Report: {report}", f)
        except Exception as e:
            log(f"   ⚠️ Telemetry check error: {e}", f)
        log("-" * 70, f)

        # 2. Lewis's Port Routing & Agent Chatter Cross-Talk
        log("\n🗣️ 2. AGENT CROSS-TALK & LEWIS PORT ROUTING LOGS:", f)
        try:
            cur.execute("SELECT sender, action, target, directive, timestamp FROM agent_chatter ORDER BY message_id DESC LIMIT 10")
            chatter = cur.fetchall()
            if chatter:
                for sender, action, target, directive, ts in chatter:
                    log(f"   [{ts}] [{sender}] ({action}) -> Port/Target: {target}", f)
                    log(f"       Directive: {directive}", f)
            else:
                log("   ⚠️ No agent chatter found.", f)
        except Exception as e:
            log(f"   ⚠️ Chatter check error: {e}", f)
        log("-" * 70, f)

        # 3. Fused Slips & Betting Engine Output
        log("\n🎰 3. FUSED SLIPS & MASS REGENERATION OUTPUT (theoretical_bets):", f)
        try:
            cur.execute("SELECT ticket_id, weight_class, odds, source, ticket_json FROM theoretical_bets LIMIT 5")
            slips = cur.fetchall()
            if slips:
                for tid, weight, odds, source, t_json in slips:
                    log(f"   [{source}] {tid} | {weight} | Odds: {odds}", f)
                    try:
                        legs = json.loads(t_json)
                        for leg in legs:
                            log(f"       ↳ {leg.get('player')} ({leg.get('team')}): {leg.get('stat')} ", f)
                    except:
                        log(f"       ↳ Raw: {t_json}", f)
            else:
                log("   ⚠️ No theoretical bets found.", f)
        except Exception as e:
            log(f"   ⚠️ Bets check error: {e}", f)
        log("-" * 70, f)

        # 4. Database Table Overview
        log("\n📦 4. DATABASE TABLE HEALTH SUMMARY:", f)
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cur.fetchall()]
        log(f"   Total Active Tables: {len(tables)}", f)
        for t in ['system_telemetry', 'agent_chatter', 'theoretical_bets', 'hospital_ward', 'stadium_weather', 'raw_slate_articles']:
            if t in tables:
                cur.execute(f"SELECT COUNT(*) FROM [{t}]")
                cnt = cur.fetchone()[0]
                log(f"   • Table '{t}': {cnt} records synced.", f)
        
        conn.close()
        log("=" * 70, f)
        log(f"✅ AUDIT COMPLETE. FILE GENERATED AT: {output_file}", f)
        log("=" * 70, f)

if __name__ == "__main__":
    run_loop_audit()
