try:
    with open('app.py', 'r', encoding='utf-8') as f:
        code = f.read()

    # Exact string replacements to map Tab 3 to the new desk
    code = code.replace("ui.render_donna_matrix()", "ui.render_juice_rankings_desk()")
    code = code.replace("hasattr(ui, 'render_donna_matrix')", "hasattr(ui, 'render_juice_rankings_desk')")
    
    # Update any lingering title text cleanly
    code = code.replace("Donna's Leverage", "⚡ Juice Rankings")
    code = code.replace("Donna’s Leverage", "⚡ Juice Rankings")
    
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print("✅ Phase 3 Complete: app.py successfully routed to the Benchmark Desk.")
except Exception as e:
    print(f"Error: {e}")
