with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open("app.py", "w", encoding="utf-8") as f:
    in_target_block = False
    for line in lines:
        # Detect the start of the injected block
        if line.startswith("    # Initialize Mobile-First Styles"):
            in_target_block = True
            
        if in_target_block:
            # Strip exactly 4 leading spaces from the injected lines
            if line.startswith("    "):
                f.write(line[4:])
            else:
                f.write(line)
            
            # Stop formatting once we hit the end of the block
            if line.strip() == "pass":
                in_target_block = False
        else:
            f.write(line)

print("✅ Indentation permanently fixed in app.py")