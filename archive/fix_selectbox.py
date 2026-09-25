with open("ui_components.py", "r", encoding="utf-8") as f:
    code = f.read()

old_line = "selected_league_str = st.selectbox(\"Select League Workspace:\", league_options)"
new_line = "selected_league_str = st.selectbox(\"Select League Workspace:\", league_options, key=\"season_long_league_selector\")"

if old_line in code:
    code = code.replace(old_line, new_line)
    with open("ui_components.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("✅ Permanently added unique key to league selectbox.")
else:
    print("⚠️ Could not find the target selectbox. Check ui_components.py manually.")