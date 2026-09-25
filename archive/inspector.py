import os, sqlite3, json

DB = r"C:\Users\chuck\the-juicer\action_grid.db"
print("=== DATABASE INSPECTION ===")
if os.path.exists(DB):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    tables = [t[0] for t in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    print(f"Tables found: {tables}")
    for tbl in tables:
        cnt = cur.execute(f"SELECT count(*) FROM {tbl}").fetchone()[0]
        print(f"Table '{tbl}': {cnt} records")
        sample = cur.execute(f"SELECT * FROM {tbl} LIMIT 1").fetchone()
        print(f"  Sample row: {sample}")
    conn.close()
else:
    print("❌ Master database file missing!")

ui_path = r"C:\Users\chuck\the-juicer\ui_components.py"
if os.path.exists(ui_path):
    print(f"\n=== UI_COMPONENTS.PY FOUND ({os.path.getsize(ui_path)} bytes) ===")
    with open(ui_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        print(f"Total lines: {len(lines)}")
        funcs = [line.strip() for line in lines if line.startswith("def render_")]
        print(f"Render functions exposed: {funcs}")
else:
    print("❌ ui_components.py missing!")