path = "ui_components.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

lines = text.splitlines()
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    if "pd.read_sql" in line and "theoretical_bets" in line:
        # Replace the broken multi-line sql call with a single clean line
        clean_stmt = '    df = pd.read_sql("SELECT ticket_id, weight_class, odds, border_color, ticket_json, created_at, confidence_score FROM theoretical_bets WHERE ticket_id NOT LIKE \'SBOX%\'", conn)'
        new_lines.append(clean_stmt)
        
        # Skip the broken continuation lines until the closing parenthesis
        i += 1
        while i < len(lines) and ")" not in lines[i]:
            i += 1
        if i < len(lines):
            i += 1 # skip closing line
        continue
        
    new_lines.append(line)
    i += 1

final_content = "\n".join(new_lines) + "\n"

# Verify compilation before writing
compile(final_content, path, 'exec')
with open(path, "w", encoding="utf-8") as f:
    f.write(final_content)

print("✅ SUCCESS: Multi-line string literal fixed and compiled cleanly!")
