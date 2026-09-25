import re

with open("app.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Target and obliterate the exact "Donna's Leverage Matrix loading" phrase (and variants)
code = re.sub(r'(?i)donna[\'’]?s leverage( matrix)?( loading[\.]{0,3})?', '⚡ Juice Rankings', code)

# 2. Ensure the UI function call is correctly mapped to the third tab (tabs[2])
code = code.replace("ui.render_donna_matrix()", "ui.render_juice_rankings()")
code = code.replace("hasattr(ui, 'render_donna_matrix')", "hasattr(ui, 'render_juice_rankings')")

# 3. Clean up any leftover st.write or st.spinner calls that might be trapping the UI
code = re.sub(r'st\.spinner\([\'"]⚡ Juice Rankings[\'"]\)', 'st.spinner("Compiling rankings...")', code)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(code)

print("✅ Scrubbed legacy loading text and hard-routed Tab 3 to the new Evaluator Desk.")
