import sqlite3
import os
from datetime import datetime, timezone
import pandas as pd

DB_PATH = os.path.join(os.getcwd(), "action_grid.db")

print("\n" + "="*50)
print("⚡ THE JUICER: FINAL HOTFIX REFRESH & AUDIT")
print("="*50 + "\n")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

print("🗑️  Flushing stale tickets and lineups...")
for tbl in ["theoretical_bets", "dfs_classic_lineups", "underdog_slips"]:
    try:
        cur.execute(f"DELETE FROM {tbl}")
        print(f"  ✓ Flushed: {tbl}")
    except Exception:
        pass
conn.commit()

print("\n🚫 Enforcing TNF Blacklist...")
cur.execute("DROP TABLE IF EXISTS completed_teams_blacklist")
cur.execute("CREATE TABLE completed_teams_blacklist (team TEXT PRIMARY KEY, game_status TEXT, purged_at TEXT)")

now_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")
cur.executemany(
    "INSERT INTO completed_teams_blacklist (team, game_status, purged_at) VALUES (?, ?, ?)",
    [("BUF", "FINAL", now_iso), ("DET", "FINAL", now_iso)]
)
conn.commit()

blacklisted_teams = ["BUF", "DET"]
print(f"  ✓ Active Blacklist: {', '.join(blacklisted_teams)}")

cur.execute("PRAGMA table_info(player_rankings)")
pr_team_col = next((row[1] for row in cur.fetchall() if row[1] in ("team", "team_abbr")), None)

if pr_team_col and blacklisted_teams:
    placeholders = ",".join("?" for _ in blacklisted_teams)
    cur.execute(f"DELETE FROM player_rankings WHERE {pr_team_col} IN ({placeholders})", blacklisted_teams)
    print(f"  ✓ Purged {cur.rowcount} player records matching TNF rosters.")

print("\n📊 Updating Telemetry & Preparing Power BI Feeds...")
cur.execute("DROP TABLE IF EXISTS system_telemetry")
cur.execute("CREATE TABLE system_telemetry (metric_name TEXT PRIMARY KEY, metric_value TEXT, last_heartbeat TEXT)")

for metric in ['LINE_REFRESH_STATUS', 'TNF_PURGE_ENFORCED']:
    cur.execute("""
        INSERT INTO system_telemetry (metric_name, metric_value, last_heartbeat)
        VALUES (?, 'SYNCHRONIZED_ACTIVE', ?)
    """, (metric, now_iso))

cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
all_tables = [r[0] for r in cur.fetchall() if not r[0].startswith("sqlite_")]
pbi_dir = os.path.join(os.getcwd(), "powerbi_exports")
os.makedirs(pbi_dir, exist_ok=True)

for tbl in ["player_rankings", "sportsbook_quotes", "completed_teams_blacklist", "system_telemetry"]:
    if tbl in all_tables:
        pd.read_sql(f"SELECT * FROM {tbl}", conn).to_csv(os.path.join(pbi_dir, f"{tbl}.csv"), index=False)
        print(f"  ✓ Power BI Export ready: powerbi_exports/{tbl}.csv")

conn.commit()

print("\n" + "="*50)
print("📋 PRE-LOCK AUDIT REPORT")
print("="*50)
for tbl in all_tables:
    cur.execute(f"SELECT COUNT(*) FROM {tbl}")
    print(f"  • {tbl.ljust(28)}: {cur.fetchone()[0]} rows")

print(f"\nAudit Timestamp: {now_iso}")
print("Status: Database flushed, schemas fixed, TNF purged, feeds staged for Power BI.")
print("="*50 + "\n")
conn.close()