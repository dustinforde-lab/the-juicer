import os

UI_FILE = "ui_components.py"
if os.path.exists(UI_FILE):
    with open(UI_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    with open(UI_FILE, "w", encoding="utf-8") as f:
        for line in lines:
            if "Underdog Fantasy Prop Hub" in line and "st.markdown" in line:
                # Replaces the broken line with a safely single-quoted Python string
                line = "    st.markdown('<h2 style=\"color:#00e5ff; margin-bottom:4px;\">⚡ Underdog Fantasy Prop Hub</h2>', unsafe_allow_html=True)\n"
            f.write(line)
            
    print("✅ Syntax error fixed! HTML double quotes are now safely wrapped inside Python single quotes.")
else:
    print("⚠️ ui_components.py not found.")
