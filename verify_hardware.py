import sqlite3

db_path = "action_grid.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [t[0] for t in cursor.fetchall()]

print("="*60)
print("🔍 THE JUICER: HARDWARE & DATABASE AUDIT REPORT")
print("="*60)

for table in tables:
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"📁 Table: {table:<32} | 📊 Rows: {count}")
    except Exception as e:
        print(f"📁 Table: {table:<32} | ⚠️ Error: {e}")

print("="*60)
conn.close()
