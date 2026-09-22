with open("app.py", "r", encoding="utf-8") as f:
    code = f.read()

old_line = "master_slate = st.selectbox(\"🌐 MASTER COMMAND SLATE:\", [\"Sunday Main Slate (Classic 9-Man)\", \"Prime-Time Showdowns\", \"Full Week\"])"
new_line = "master_slate = st.selectbox(\"🌐 MASTER COMMAND SLATE:\", [\"Sunday Main Slate (Classic 9-Man)\", \"Prime-Time Showdowns\", \"Full Week\"], key=\"master_slate_selector\")"

if old_line in code:
    code = code.replace(old_line, new_line)
    with open("app.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("✅ Permanently added unique key to Master Slate selectbox in app.py.")
else:
    print("⚠️ Could not find the exact line. Open app.py in notepad and add key='master_slate_selector' to line 49.")