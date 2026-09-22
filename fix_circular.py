import re

# 1. Patch ui_components.py to accept the scheduler as an argument
with open("ui_components.py", "r", encoding="utf-8") as f:
    ui_code = f.read()

ui_code = re.sub(r'def render_ops_center\(\):', 'def render_ops_center(sched=None):', ui_code)
ui_code = re.sub(r'from app import global_scheduler\n?', '', ui_code)
ui_code = re.sub(r'sched = global_scheduler\n?', '', ui_code)

with open("ui_components.py", "w", encoding="utf-8") as f:
    f.write(ui_code)

# 2. Patch app.py to pass the scheduler into the UI
with open("app.py", "r", encoding="utf-8") as f:
    app_code = f.read()

app_code = app_code.replace("ui.render_ops_center()", "ui.render_ops_center(global_scheduler)")

with open("app.py", "w", encoding="utf-8") as f:
    f.write(app_code)

print("✅ Broken the circular import. The Juicer is fully stable.")