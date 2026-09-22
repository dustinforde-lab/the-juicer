import os

file_path = "ui_components.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_string = """    try: st.dataframe(_read_sql_cached("SELECT * FROM sportsbook_quotes LIMIT 12"), use_container_width=True)
    except: pass"""

new_string = """    # Raw sportsbook_quotes dataframe deleted for a cleaner UI"""

if old_string in content:
    content = content.replace(old_string, new_string)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Successfully removed the raw data table from the Scoreboard tab.")
else:
    print("⚠️ Could not find the exact string to replace. It may have already been removed.")