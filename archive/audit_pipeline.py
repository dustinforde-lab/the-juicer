import os
import re

report = []
report.append("=" * 70)
report.append("  THE JUICER: PIPELINE & ROSTER GENERATION DEEP AUDIT")
report.append("=" * 70 + "\n")

# 1. Search for any script writing to dfs_rosters
report.append("[1] ALL SCRIPT REFERENCES INSERTING INTO 'dfs_rosters':")
for root, dirs, files in os.walk("."):
    if any(skip in root for skip in [".git", "venv", "__pycache__"]):
        continue
    for file in files:
        if file.endswith(".py") and file != "audit_pipeline.py":
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    for idx, line in enumerate(f, 1):
                        if re.search(r"dfs_rosters", line, re.IGNORECASE) and any(w in line for w in ["INSERT", "insert", "append", "execute", "to_sql"]):
                            report.append(f"  --> {file}:{idx} | {line.strip()}")
            except Exception:
                pass
report.append("\n" + "-" * 70)

# 2. Search for any remaining hardcoded/procedural name lists across all files
report.append("[2] SCRIPT REFERENCES WITH PROCEDURAL NAME LISTS (e.g. first_names, last_names):")
for root, dirs, files in os.walk("."):
    if any(skip in root for skip in [".git", "venv", "__pycache__"]):
        continue
    for file in files:
        if file.endswith(".py") and file != "audit_pipeline.py":
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    if "first_names" in content or "last_names" in content or "Tony Moore" in content:
                        report.append(f"  --> FOUND IN {file}")
            except Exception:
                pass
report.append("\n" + "-" * 70)

# 3. Check what app.py imports or executes on startup
report.append("[3] APP.PY STARTUP ROUTINES & IMPORTS:")
if os.path.exists("app.py"):
    with open("app.py", "r", encoding="utf-8", errors="ignore") as f:
        for idx, line in enumerate(f, 1):
            if any(term in line for term in ["import ", "populate", "sync", "run_", "subprocess", "os.system"]):
                report.append(f"  Line {idx:3d}: {line.strip()}")
else:
    report.append("  app.py not found in current folder.")
report.append("\n" + "-" * 70)

# 4. Check recommendation_engine.py for record_dfs_lineup and batch inserts
report.append("[4] RECOMMENDATION_ENGINE.PY RECORDING LOGIC:")
if os.path.exists("recommendation_engine.py"):
    with open("recommendation_engine.py", "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
        capture = False
        count = 0
        for idx, line in enumerate(lines, 1):
            if "def record_dfs_lineup" in line or "def record_" in line:
                capture = True
            if capture:
                report.append(f"  Line {idx:3d}: {line.rstrip()}")
                count += 1
                if count > 35:
                    capture = False
                    count = 0
else:
    report.append("  recommendation_engine.py not found.")
report.append("\n" + "=" * 70)

with open("audit_report.txt", "w", encoding="utf-8") as out:
    out.write("\n".join(report))

print("Audit report written to audit_report.txt")