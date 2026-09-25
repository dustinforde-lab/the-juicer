import sqlite3
import os

print("🔍 [PARLAY DIAGNOSTIC] Checking Parlay Data Source...")

# Check active database connections
prod_db = "action_grid.db"
sandbox_db = os.path.join("firm_sandbox", "sandbox_grid.db")

print(f"   📂 Production DB exists: {os.path.exists(prod_db)}")
print(f"   📂 Sandbox DB exists: {os.path.exists(sandbox_db)}")

conn = sqlite3.connect(prod_db)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [t[0] for t in cursor.fetchall()]

if "theoretical_bets" in tables:
    cursor.execute("SELECT COUNT(*) FROM theoretical_bets;")
    count = cursor.fetchone()[0]
    print(f"   ✅ Prod 'theoretical_bets' table active with {count} live records.")
else:
    print("   ⚠️ Prod 'theoretical_bets' table missing.")

conn.close()
print("🎯 DIAGNOSTIC COMPLETE: Switch app configuration from sandbox mode to live production feed.")
