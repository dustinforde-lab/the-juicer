import streamlit as st
import importlib
import address_book

def dispatch_tab(tab_name):
    """
    Looks up the tab in the Master Address Book, tries all function aliases,
    and checks fallback modules to eliminate AttributeError and ModuleNotFoundError.
    """
    if tab_name not in address_book.TAB_DISPATCH_REGISTRY:
        st.error(f"🚨 Address missing: '{tab_name}' not registered in address_book.py")
        return

    route = address_book.TAB_DISPATCH_REGISTRY[tab_name]
    target_modules = [route["module"]]
    if "fallback_module" in route:
        target_modules.append(route["fallback_module"])

    executed = False
    last_err = None

    for mod_name in target_modules:
        try:
            mod = importlib.import_module(mod_name)
            for func_name in route["entrypoints"]:
                if hasattr(mod, func_name):
                    getattr(mod, func_name)()
                    executed = True
                    break
            if executed:
                break
        except Exception as e:
            last_err = e

    if not executed:
        st.error(f"⚠️ Routing failure for '{tab_name}'")
        if last_err:
            st.caption(f"Error details: {last_err}")
            st.code(f"Checked Modules: {target_modules}\nChecked Functions: {route['entrypoints']}")

# Component Wrappers for app.py
def render_vegas_wall(): dispatch_tab("Scoreboard")
def render_dfs_engine(): dispatch_tab("DFS Engine")
def render_dfs_lab(): dispatch_tab("DFS Lab")
def render_the_rankings(): dispatch_tab("The Rankings")
def render_parlay_mix(): dispatch_tab("Parlay Mix")
def render_season_long(): dispatch_tab("Season Long")
def render_prizepicks(): dispatch_tab("PrizePicks")
def render_film_room(): dispatch_tab("Film Room")
def render_ops(): dispatch_tab("Ops")
def render_learning(): dispatch_tab("Learning")
