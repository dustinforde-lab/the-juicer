import sqlite3, json

print("="*60)
print("📋 CHUCK'S INVENTORY AUDIT: TRUE SCHEMA SCAN")
print("="*60 + "\n")

conn = sqlite3.connect("action_grid.db")
cur = conn.cursor()

def scan_table(table_name, emoji):
    try:
        print(f"{emoji} Scanning Table: {table_name}")
        cur.execute(f"PRAGMA table_info({table_name})")
        cols = [c[1] for c in cur.fetchall()]
        print(f"   Columns: {cols}")
        
        cur.execute(f"SELECT count(*) FROM {table_name}")
        cnt = cur.fetchone()[0]
        print(f"   Row Count: {cnt} active records")
        
        if cnt > 0:
            cur.execute(f"SELECT * FROM {table_name} LIMIT 1")
            row = cur.fetchone()
            for idx, val in enumerate(row):
                if isinstance(val, str) and (val.startswith("[") or val.startswith("{")):
                    try:
                        data = json.loads(val)
                        print(f"   JSON Found in column: '{cols[idx]}'")
                        if isinstance(data, list) and len(data) > 0:
                            print(f"   Array Size: {len(data)} items")
                            print(f"   Data Keys: {list(data[0].keys())}")
                        elif isinstance(data, dict):
                            print(f"   Data Keys: {list(data.keys())}")
                    except Exception:
                        pass
        print("-" * 40)
    except Exception as e:
        print(f"   ❌ Error scanning {table_name}: {e}")

# Scan the real tables we saw in your database
scan_table("dfs_classic_lineups", "🏈")
scan_table("theoretical_bets", "💸")

conn.close()
print("\n🎯 INVENTORY COMPLETE. DROP THESE KEYS IN THE CHAT.")