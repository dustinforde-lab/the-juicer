import sqlite3
from datetime import datetime

DB_FILE = "action_grid.db"

def deploy_telemetry_hub():
    print("=" * 65)
    print("📡 [UPGRADE CHUNK 10] Deploying Agent Telemetry (The Slack Channel)...")
    print("=" * 65)
    
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS agent_chatter (
                message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT,
                directive TEXT,
                target TEXT,
                action TEXT,
                timestamp TEXT
            )
        """)
        
        cur.execute("DELETE FROM agent_chatter")
        now_ts = datetime.now().strftime("%Y-%m-%d %I:%M %p ET")
        msg_count = 0
        
        # 1. Pull Medic Directives
        try:
            for player, status in cur.execute("SELECT player_name, status FROM hospital_ward").fetchall():
                cur.execute("INSERT INTO agent_chatter (sender, directive, target, action, timestamp) VALUES (?, ?, ?, ?, ?)",
                            ("The Medic", f"{status} Alert", player, "HARD PURGE", now_ts))
                print(f"   💬 [Medic] -> Lewis: 'Purge {player} ({status})'")
                msg_count += 1
        except Exception: pass

        # 2. Pull Weather Directives
        try:
            for game, cond, act in cur.execute("SELECT game_matchup, condition, agent_action FROM stadium_weather WHERE agent_action != 'None'").fetchall():
                cur.execute("INSERT INTO agent_chatter (sender, directive, target, action, timestamp) VALUES (?, ?, ?, ?, ?)",
                            ("Meteorologist", f"{cond} Warning", game, act, now_ts))
                print(f"   💬 [Meteorologist] -> Mike: '{act} in {game} ({cond})'")
                msg_count += 1
        except Exception: pass

        # 3. Pull Sharp Market Directives
        try:
            for player, edge in cur.execute("SELECT player_name, ev_edge FROM sharp_market_lines").fetchall():
                cur.execute("INSERT INTO agent_chatter (sender, directive, target, action, timestamp) VALUES (?, ?, ?, ?, ?)",
                            ("Juice Press", f"+EV Found ({edge})", player, "FORCE INCLUDE", now_ts))
                print(f"   💬 [Juice Press] -> Mike: 'Force include {player} (Edge: {edge})'")
                msg_count += 1
        except Exception: pass

        conn.commit()
        print(f"\n   📡 Hub Online: {msg_count} active directives broadcasted to the War Room.")

def run_self_test():
    print("\n🧪 [SELF-CHECK GATE] Auditing Telemetry Routing...")
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        rows = cur.execute("SELECT * FROM agent_chatter").fetchall()
        assert len(rows) > 0, "Integrity Failure: Telemetry hub is silent."
        
        senders = [r[1] for r in rows]
        assert "The Medic" in senders, "Routing Failure: Medic offline."
        assert "Meteorologist" in senders, "Routing Failure: Meteorologist offline."
        assert "Juice Press" in senders, "Routing Failure: Juice Press offline."
        
    print("✅ TELEMETRY ONLINE: All interns are successfully communicating in the hub.\n")

if __name__ == "__main__":
    deploy_telemetry_hub()
    run_self_test()
