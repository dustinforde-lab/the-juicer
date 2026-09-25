import os, sqlite3

DB = r"C:\Users\chuck\the-juicer\action_grid.db"
output_lines = []

output_lines.append("==================================================")
output_lines.append("🏈 THE JUICER: MASTER SYSTEM AUDIT REPORT 🏈")
output_lines.append("==================================================")

if os.path.exists(DB):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    tables = [t[0] for t in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    output_lines.append(f"\n[DATABASE] Connected: {DB}")
    output_lines.append(f"Tables located: {tables}\n")
    
    for tbl in tables:
        cnt = cur.execute(f"SELECT count(*) FROM {tbl}").fetchone()[0]
        output_lines.append(f"--- Table: {tbl} ({cnt} records) ---")
        rows = cur.execute(f"SELECT * FROM {tbl} LIMIT 2").fetchall()
        for r in rows:
            output_lines.append(f"  {r}")
        output_lines.append("")
    conn.close()
else:
    output_lines.append("❌ Master database file missing!")

ui_path = r"C:\Users\chuck\the-juicer\ui_components.py"
if os.path.exists(ui_path):
    output_lines.append(f"\n[UI COMPONENTS] File size: {os.path.getsize(ui_path)} bytes")
    with open(ui_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        output_lines.append(f"Total lines: {len(lines)}")
        funcs = [line.strip() for line in lines if line.startswith("def render_")]
        output_lines.append(f"Render functions exposed: {funcs}")

report_content = "\n".join(output_lines)
print(report_content)

local_path = os.path.join(os.getcwd(), "the_juicer_audit_report.txt")
with open(local_path, "w", encoding="utf-8") as out:
    out.write(report_content)

print(f"\n✅ Audit report successfully saved locally to: {local_path}")