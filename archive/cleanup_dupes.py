import ast

with open("ui_components.py", "r", encoding="utf-8-sig") as f:
    source = f.read()

tree = ast.parse(source)
lines = source.splitlines(keepends=True)

funcs = {}
for node in tree.body:
    if isinstance(node, ast.FunctionDef):
        funcs.setdefault(node.name, []).append((node.lineno, node.end_lineno))

lines_to_remove = set()
dupes_removed = 0
for name, occurrences in funcs.items():
    if len(occurrences) > 1:
        for start, end in occurrences[:-1]:
            for ln in range(start, end + 1):
                lines_to_remove.add(ln)
            dupes_removed += 1

new_lines = [line for i, line in enumerate(lines, start=1) if i not in lines_to_remove]
new_source = "".join(new_lines)

try:
    ast.parse(new_source)
except SyntaxError as e:
    print(f"ABORT: cleaned version fails to parse: {e}")
    raise SystemExit(1)

with open("ui_components.py", "w", encoding="utf-8") as f:
    f.write(new_source)

print(f"Removed {dupes_removed} duplicate/dead function definitions.")
print(f"File went from {len(lines)} to {len(new_lines)} lines.")
