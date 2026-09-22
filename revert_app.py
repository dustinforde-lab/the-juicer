with open("app.py", "r", encoding="utf-8") as f:
    code = f.read()

# Reconnect the severed Parlay and Pick'em wires
code = code.replace("ui.render_parlay_matrix()", "ui.render_real_parlay_matrix()")
code = code.replace("ui.render_pickem_slips(target_platform='PRIZEPICKS')", "ui.render_prizepicks_underdog()")

with open("app.py", "w", encoding="utf-8") as f:
    f.write(code)
print("✅ SUCCESS: The severed wires in app.py have been spliced back to your original functions.")