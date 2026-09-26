import os
import re

print("🛠️ INITIATING SYSTEM REPAIR...")
ui_dir = r"C:\Users\Chuck\the-juicer"

# Fix the missing 'f' string in the UI
for root, _, files in os.walk(ui_dir):
    for file in files:
        if file.endswith(".py"):
            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Look for the exact broken string and inject the 'f'
            if re.search(r'(?<!f)([\'"])MODE: \{st\.session_state', content):
                new_content = re.sub(r'(?<!f)([\'"])(MODE: \{st\.session_state)', r'f\g<1>\g<2>', content)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"✅ Patched missing f-string in {file}")

# Fix the Stale Data Path in data_service.py
ds_path = os.path.join(ui_dir, "data_service.py")
if os.path.exists(ds_path):
    with open(ds_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    new_content = re.sub(
        r'db_path\s*=\s*[\'"]action_grid\.db[\'"]', 
        r'db_path = r"C:\\Users\\Chuck\\the-juicer\\action_grid.db"', 
        content
    )
    with open(ds_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("✅ Locked absolute DB path to fix Stale Data warning")
