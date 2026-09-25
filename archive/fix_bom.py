import os

UI_FILE = "ui_components.py"
if os.path.exists(UI_FILE):
    # 'utf-8-sig' automatically reads and strips the hidden BOM
    with open(UI_FILE, "r", encoding="utf-8-sig") as f:
        clean_code = f.read()
        
    # Write it back out as pure, standard utf-8
    with open(UI_FILE, "w", encoding="utf-8") as f:
        f.write(clean_code)
        
    print("✅ Hidden BOM (U+FEFF) successfully stripped from ui_components.py!")
else:
    print(f"⚠️ Error: {UI_FILE} not found.")
