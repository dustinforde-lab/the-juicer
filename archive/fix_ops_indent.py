import re

with open("ui_components.py", "r", encoding="utf-8") as f:
    content = f.read()

# Find the damaged block between Autonomous Engine Status and Scheduled Jobs
pattern = r'([ \t]*)st\.markdown\("#### Autonomous Engine Status"\).*?st\.markdown\("#### Scheduled Jobs"\)'

def replacer(match):
    indent = match.group(1)
    if not indent.endswith('\n'):
        indent = '\n' + indent
        
    return (indent + 'st.markdown("#### Autonomous Engine Status")' +
           indent + 'if sched:' +
           indent + '    status_color = "#ff4757" if sched.is_paused else "#2ed573"' +
           indent + '    status_text = "PAUSED (KILL SWITCH ENGAGED)" if sched.is_paused else "ACTIVE (POLLING LIVE)"' +
           indent + '    st.markdown(f"<div style=\'font-size: 14px; margin-bottom: 15px; padding: 10px; border-left: 4px solid {status_color}; background: rgba(255,255,255,0.05);\'>{status_text}</div>", unsafe_allow_html=True)' +
           indent + '    col1, col2 = st.columns(2)' +
           indent + '    with col1:' +
           indent + '        if st.button("⏸️ ENGAGE KILL SWITCH", use_container_width=True):' +
           indent + '            sched.pause()' +
           indent + '            st.rerun()' +
           indent + '    with col2:' +
           indent + '        if st.button("▶️ RESUME AUTONOMY", use_container_width=True):' +
           indent + '            sched.resume()' +
           indent + '            st.rerun()' +
           indent + 'st.markdown("#### Scheduled Jobs")')

new_content = re.sub(pattern, replacer, content, flags=re.DOTALL)

with open("ui_components.py", "w", encoding="utf-8") as f:
    f.write(new_content)

print("✅ Ops Center indentation completely rebuilt and secured.")