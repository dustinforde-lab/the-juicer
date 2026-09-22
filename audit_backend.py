import sqlite3
import pandas as pd

def run_backend_audit():
    print("\n🔍 INITIATING BACKEND DATABASE AUDIT...\n" + "="*40)
    try:
        with sqlite3.connect("action_grid.db") as conn:
            # 1. Check if the tables exist and have data
            tables = ["slips", "agent_chatter"] 
            # (Add "dfs_rosters" and "parlays" if those are strictly separate tables in your schema)
            
            for t in tables:
                try:
                    count = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                    if count == 0:
                        print(f"⚠️ [{t.upper()} TABLE]: 0 rows. (Table exists, but is completely empty)")
                    else:
                        print(f"✅ [{t.upper()} TABLE]: {count} rows found.")
                except sqlite3.OperationalError:
                    print(f"❌ [{t.upper()} TABLE]: Table does not exist in the database!")
            
            # 2. Check the most recent Agent Chatter for silent errors
            print("\n🚨 LATEST BACKEND LOGS (Last 5 entries):")
            try:
                logs = pd.read_sql("SELECT timestamp, agent, message FROM agent_chatter ORDER BY message_id DESC LIMIT 5", conn)
                if logs.empty:
                    print("   No logs found. The backend scheduler might not be running at all.")
                else:
                    for _, row in logs.iterrows():
                        print(f"   [{row['timestamp']}] {row['agent']}: {row['message']}")
            except Exception as e:
                print(f"   Could not read chatter table: {e}")
                
    except Exception as e:
        print(f"Database connection failed: {e}")
    print("\n" + "="*40)

run_backend_audit()