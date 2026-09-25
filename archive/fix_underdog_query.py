import sqlite3
import os
import shutil

conn = sqlite3.connect("action_grid.db")
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(underdog_slips);")
cols = [c[1] for c in cursor.fetchall()]
print(f"🔍 Underdog slips actual columns: {cols}")
conn.close()

id_col = 'slip_id' if 'slip_id' in cols else ('id' if 'id' in cols else cols[0])
odds_col = 'odds' if 'odds' in cols else cols[1]

ui_path = "ui_components.py"
shutil.copy(ui_path, "ui_components_schema_backup.py")

with open(ui_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace the mismatched underdog query with the dynamically mapped column names
old_q = "SELECT ticket_id, odds, slip_json FROM underdog_slips WHERE ticket_id NOT LIKE 'SBOX%'"
new_q = f"SELECT {id_col}, {odds_col}, slip_json FROM underdog_slips WHERE {id_col} NOT LIKE 'SBOX%'"
content = content.replace(old_q, new_q)

# Built-in check system with automatic rollback
try:
    compile(content, ui_path, 'exec')
    with open(ui_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ SUCCESS: underdog_slips query mapped to '{id_col}' and compiled cleanly!")
except Exception as e:
    print(f"❌ Compilation Error: {e}")
    shutil.copy("ui_components_schema_backup.py", ui_path)
    print("⚠️ Reverted safely to backup.")
