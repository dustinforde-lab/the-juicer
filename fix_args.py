with open("ui_components.py", "r", encoding="utf-8") as f:
    code = f.read()

# Force the function to accept the scheduler argument
if "def render_ops_center():" in code:
    code = code.replace("def render_ops_center():", "def render_ops_center(sched=None):")
    with open("ui_components.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("✅ Function signature updated in ui_components.py.")
elif "def render_ops_center(sched=None):" in code:
    print("✅ Function already updated. Please restart your Streamlit server.")
else:
    print("⚠️ Could not find the function definition.")