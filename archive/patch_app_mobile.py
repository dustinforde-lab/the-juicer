with open("app.py", "r", encoding="utf-8") as f:
    code = f.read()

header_code = """
    # Initialize Mobile-First Styles and Sticky Header
    try:
        import ui_components
        ui_components.apply_mobile_css()
        st.markdown('''
        <div class="mobile-header">
            <div style="letter-spacing: 1px;">👑 THE JUICER</div>
            <div style="font-size: 12px; opacity: 0.8; font-weight: normal;">Bankroll: $1,450 &nbsp;|&nbsp; <span style="color: #2ed573; font-weight: bold;">LIVE</span></div>
        </div>
        ''', unsafe_allow_html=True)
    except Exception:
        pass
"""

if "apply_mobile_css" not in code and "st.set_page_config" in code:
    parts = code.split("st.set_page_config", 1)
    end_of_config = parts[1].find(")") + 1
    new_code = parts[0] + "st.set_page_config" + parts[1][:end_of_config] + "\n" + header_code + parts[1][end_of_config:]
    
    with open("app.py", "w", encoding="utf-8") as f:
        f.write(new_code)
    print("✅ Sticky header and mobile CSS initialized in app.py")
else:
    print("⚠️ Mobile header already initialized or target not found.")