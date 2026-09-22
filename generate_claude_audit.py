import os, sqlite3, glob

db_path = r"C:\Users\chuck\the-juicer\action_grid.db"
output_lines = []

output_lines.append("# CLAUDE MASTER REPO & BACKEND-TO-FRONTEND AUDIT")
output_lines.append("## Objective: Merge Local SQLite Backend with Production Streamlit Frontend Layout\n")

output_lines.append("---")
output_lines.append("## 1. DATABASE & SCHEMA AUDIT (`action_grid.db`)")
if os.path.exists(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        tables = [t[0] for t in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
        output_lines.append(f"- **Database Status**: Connected Successfully (`{db_path}`)")
        output_lines.append(f"- **Total Tables Found**: {len(tables)}")
        output_lines.append(f"- **Table List**: `{tables}`\n")

        for tbl in tables:
            cnt = cur.execute(f"SELECT count(*) FROM {tbl}").fetchone()[0]
            output_lines.append(f"### Table: `{tbl}` ({cnt} rows)")
            cols = [info[1] for info in cur.execute(f"PRAGMA table_info({tbl})").fetchall()]
            output_lines.append(f"- **Columns**: `{cols}`")
            sample_rows = cur.execute(f"SELECT * FROM {tbl} LIMIT 2").fetchall()
            output_lines.append(f"- **Sample Data**: `{sample_rows}`\n")
        conn.close()
    except Exception as e:
        output_lines.append(f"- **Database Error**: {e}\n")
else:
    output_lines.append("- **Status**: ❌ Database file not found.\n")

output_lines.append("---")
output_lines.append("## 2. PYTHON FILE INVENTORY & SOURCE CODE AUDIT")
py_files = glob.glob("*.py")
output_lines.append(f"- **Python Files Located**: `{py_files}`\n")

for file in py_files:
    if file.startswith("inspector") or file.startswith("run_"):
        continue
    try:
        file_size = os.path.getsize(file)
        output_lines.append(f"### File: `{file}` ({file_size} bytes)")
        with open(file, "r", encoding="utf-8-sig", errors="ignore") as f:
            code_content = f.read()
            output_lines.append(f"```python\n{code_content}\n```\n")
    except Exception as e:
        output_lines.append(f"- **Error reading {file}**: {e}\n")

report_content = "\n".join(output_lines)

# Robust desktop path resolution avoiding OneDrive redirection failures
user_profile = os.environ.get("USERPROFILE", r"C:\Users\chuck")
desktop_candidates = [
    os.path.join(user_profile, "Desktop"),
    os.path.join(user_profile, "OneDrive", "Desktop"),
    r"C:\Users\chuck\Desktop"
]

target_desktop = desktop_candidates[0]
for d in desktop_candidates:
    if os.path.exists(d):
        target_desktop = d
        break

output_filepath = os.path.join(target_desktop, "audit for Claude.txt")

with open(output_filepath, "w", encoding="utf-8") as out:
    out.write(report_content)

print(f"✅ Full audit successfully dropped to your Desktop at: {output_filepath}")