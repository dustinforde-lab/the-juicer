import os, sqlite3

print("=== 🛠️ THE JUICER: FULL SYSTEM AUDIT ===\n")

print("📂 FILE SYNTAX CHECK:")
for file in ["app.py", "ui_components.py"]:
    if not os.path.exists(file):
        print(f"  [MISSING] {file} not found!")
        continue
    try:
        with open(file, 'r', encoding='utf-8') as f:
            compile(f.read(), file, 'exec')
        print(f"  [✅ OK] {file} compiles perfectly.")
    except SyntaxError as e:
        print(f"  [❌ ERROR] {file} syntax broken at line {e.lineno}: {e.msg}")

print("\n🗄️ DATABASE SCHEMA AUDIT:")
try:
    conn = sqlite3.connect("action_grid.db")
    c = conn.cursor()
    
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in c.fetchall()]
    print(f"  Found Tables: {', '.join(tables)}")

    for table in tables:
        if table == 'theoretical_bets' or 'dfs' in table.lower() or 'lineup' in table.lower():
            c.execute(f"PRAGMA table_info({table});")
            cols = [row[1] for row in c.fetchall()]
            print(f"  -> '{table}' columns: {', '.join(cols)}")
            
            try:
                c.execute(f"SELECT * FROM {table} LIMIT 1;")
                row = c.fetchone()
                if row:
                    print(f"     [Sample Data Snapshot]: {str(row)[:100]}...")
            except:
                pass
except Exception as e:
    print(f"  [❌ DB ERROR] {e}")

print("\n==========================================")
