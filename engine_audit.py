import sqlite3

DB_PATH = r"C:\Users\chuck\the-juicer\action_grid.db"

def audit_table(cursor, table_name, display_name):
    try:
        cursor.execute(f"SELECT count(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        
        cursor.execute(f"PRAGMA table_info({table_name})")
        cols = [c[1] for c in cursor.fetchall()]
        
        time_info = ""
        for t_col in ['updated_at', 'created_at', 'timestamp', 'last_updated', 'line_locked']:
            if t_col in cols:
                cursor.execute(f"SELECT {t_col} FROM {table_name} ORDER BY {t_col} DESC LIMIT 1")
                res = cursor.fetchone()
                if res and res[0]: time_info = f" | Last Ping: {res[0]}"
                break
                
        print(f"[{count:>5} records] {display_name:<26}{time_info}")
    except:
        print(f"[  ---  records] {display_name:<26} | ❌ Offline or Missing")

print("\n" + "="*75)
print("🏈 THE JUICER: PIPELINE HEALTH & ENGINE AUDIT 🏈")
print("="*75)
try:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("\n📥 STAGE 1: INGESTION (Lewis & The Interns)")
    audit_table(cur, "sportsbook_quotes", "Raw Sportsbook Quotes")
    audit_table(cur, "vegas_lines", "Vegas Live Spreads")
    audit_table(cur, "sharp_market_lines", "Sharp Market Odds")
    audit_table(cur, "raw_slate_articles", "Beat Writer Feeds")
    audit_table(cur, "hospital_ward", "Mike's Injury Ward")
    
    print("\n🧠 STAGE 2: GRADING & MATH (Donna)")
    audit_table(cur, "predictions_ledger", "Predictions Ledger")
    audit_table(cur, "model_learning_ledger", "Model Learning Ledger")
    audit_table(cur, "correlation_weights", "Correlation Weights")
    audit_table(cur, "mike_donna_deltas", "Injury Leverage Deltas")
    
    print("\n🚀 STAGE 3: OUTPUT (Tony & Dwight)")
    audit_table(cur, "dfs_classic_lineups", "DFS Classic 9-Man Rosters")
    audit_table(cur, "dfs_showdown_lineups", "DFS Showdown Rosters")
    audit_table(cur, "theoretical_bets", "Sharp Parlay Tickets")
    audit_table(cur, "underdog_slips", "PrizePicks/Underdog Slips")
    
    conn.close()
    print("\n" + "="*75)
    print("🎯 AUDIT COMPLETE. DROP THE SCREENSHOT BELOW.")
    print("="*75 + "\n")
except Exception as e:
    print(f"❌ Database locked or missing: {e}")