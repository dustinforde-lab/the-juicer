import os
import re

UI_FILE = "ui_components.py"

if os.path.exists(UI_FILE):
    with open(UI_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    counter = 0
    def replace_purge_btn(match):
        global counter
        counter += 1
        return f'st.button("🧹 Force Slate Purge & Refresh", key="btn_slate_purge_unique_{counter}")'

    pattern = r'st\.button\([\'"][^\'"]*Force Slate Purge[^\'"]*[\'"](?:,\s*key=[\'"][^\'"]*[\'"])?\)'
    updated_content = re.sub(pattern, replace_purge_btn, content)

    with open(UI_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"✅ Successfully assigned distinct keys to {counter} purge buttons across ui_components.py.")
else:
    print("⚠️ ui_components.py not found.")
