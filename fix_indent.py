import py_compile

print("=" * 65)
print("🔧 [HOTFIX] Repairing IndentationError in app.py...")
print("=" * 65)

try:
    with open("app.py", "r", encoding="utf-8") as f:
        lines = f.readlines()

    fixed = False
    for i in range(1, len(lines)):
        if "st.markdown(clean_card" in lines[i]:
            prev_line = lines[i-1]
            if "clean_card =" in prev_line:
                # Capture the exact whitespace from the line above
                correct_indent = prev_line[:len(prev_line) - len(prev_line.lstrip())]
                lines[i] = correct_indent + "st.markdown(clean_card, unsafe_allow_html=True)\n"
                fixed = True

    if fixed:
        with open("app.py", "w", encoding="utf-8") as f:
            f.writelines(lines)
        print("   ✅ Indentation automatically realigned.")
    else:
        print("   ⚠️ Could not find the specific clean_card lines to fix.")

    # Verify the syntax is now flawless
    py_compile.compile("app.py", doraise=True)
    print("   ✅ app.py compiled with ZERO syntax errors!")

except Exception as e:
    print(f"   ❌ Error: {e}")

print("=" * 65)
