# -*- coding: utf-8 -*-
import streamlit as st
import address_book

st.set_page_config(page_title="The Juicer | War Room", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<style>.stApp { background-color: #06090e; color: #c9d1d9; } header, footer { visibility: hidden; }</style>", unsafe_allow_html=True)
address_book.init_session_state(st)

# Safe Module Imports - Note the updated tab_juice_rankings import
import ui_scoreboard, ui_dfs, ui_lineup_lab, tab_juice_rankings, ui_parlay_mix, ui_season_long, ui_prizepicks, ui_film_room, ui_ops, ui_sim_audit

tabs = st.tabs(["🏟️ Scoreboard", "🧬 DFS Engine", "🧪 DFS Lab", "⚡ The Rankings", "🔀 Parlay Mix", "🏈 Season Long", "🎟️ PrizePicks", "🎥 Film Room", "⚙️ Ops", "🎲 Learning"])

tab_modules = {
    0: ui_scoreboard.render_scoreboard_tab,
    1: ui_dfs.render_dfs_tab,
    2: ui_lineup_lab.render_lineup_lab_tab,
    3: tab_juice_rankings.render_the_rankings,
    4: ui_parlay_mix.render_parlay_mix,
    5: ui_season_long.render_season_long,
    6: ui_prizepicks.render_prizepicks,
    7: ui_film_room.render_film_room,
    8: ui_ops.render_ops_desk,
    9: ui_sim_audit.render_sim_audit_tab
}

for tab_idx, render_func in tab_modules.items():
    with tabs[tab_idx]:
        try:
            render_func()
        except Exception as e:
            st.error(f"⚠️ UI Guardrail Activated: Tab {tab_idx} intercepted an error: {e}. The other 9 tabs remain fully operational.")
