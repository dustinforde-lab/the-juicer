import os

UI_FILE = "ui_components.py"
if os.path.exists(UI_FILE):
    with open(UI_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    with open(UI_FILE, "w", encoding="utf-8") as f:
        for line in lines:
            if "st.button" in line and "Force Slate Purge" in line and "key=" not in line:
                # Safely injects the unique key right before the closing parenthesis/colon
                line = line.replace('"):', '", key="unique_purge_btn_key"):')
            f.write(line)
            
    print("✅ Duplicate widget error eliminated! The button now has a unique key.")
else:
    print("⚠️ ui_components.py not found.")
