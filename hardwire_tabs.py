import re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Hard-wire Tab 2 (Juice Rankings)
tab2_pattern = r'with tabs\[2\]:.*?st\.info\([^\)]+Juice Rankings[^\)]+\)'
tab2_replace = '''with tabs[2]:
    try:
        import ui_components
        ui_components.render_juice_rankings_desk()
    except Exception as e:
        import streamlit as st
        import traceback
        st.error(f"UI Crash in Juice Rankings: {e}")
        st.code(traceback.format_exc())'''
code = re.sub(tab2_pattern, tab2_replace, code, flags=re.DOTALL)

# 2. Hard-wire Tab 3 (Parlay Matrix)
tab3_pattern = r'with tabs\[3\]:.*?st\.info\("Parlay matrix loading\.\.\."\)'
tab3_replace = '''with tabs[3]:
    try:
        import ui_components
        ui_components.render_parlay_matrix()
    except Exception as e:
        import streamlit as st
        st.error(f"UI Crash in Parlay Matrix: {e}")'''
code = re.sub(tab3_pattern, tab3_replace, code, flags=re.DOTALL)

# 3. Hard-wire Tab 5 (PrizePicks)
tab5_pattern = r'with tabs\[5\]:.*?uext\.render_safe_prizepicks\(\)'
tab5_replace = '''with tabs[5]:
    try:
        import ui_components
        ui_components.render_prizepicks_desk()
    except Exception as e:
        import streamlit as st
        st.error(f"UI Crash in PrizePicks Desk: {e}")'''
code = re.sub(tab5_pattern, tab5_replace, code, flags=re.DOTALL)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("✅ Tabs 2, 3, and 5 successfully hard-wired to ui_components.py.")
