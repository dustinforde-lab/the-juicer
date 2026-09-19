import os

APP_FILE = "app.py"
CSS_INJECTION = """

# --- MASSIVE BLENDER CSS OVERRIDE ---
import streamlit as st
st.markdown('''
    <style>
        /* Targets the Juicer Logo and scales it up */
        div[data-testid="stImage"] img {
            max-width: 250px !important;
            margin: 0 auto;
            display: block;
        }
    </style>
''', unsafe_allow_html=True)
"""

def enlarge_blender():
    if not os.path.exists(APP_FILE):
        print(f"❌ Error: {APP_FILE} not found.")
        return
        
    with open(APP_FILE, "r", encoding="utf-8") as f:
        code = f.read()
        
    if "MASSIVE BLENDER CSS OVERRIDE" not in code:
        with open(APP_FILE, "a", encoding="utf-8") as f:
            f.write(CSS_INJECTION)
        print("✅ SUCCESS: Blender size CSS injected into app.py!")
    else:
        print("⚡ NOTE: Blender size is already enlarged in app.py.")

if __name__ == "__main__":
    enlarge_blender()
