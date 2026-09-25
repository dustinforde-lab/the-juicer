import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PATHS = {
    "DATABASE": os.path.join(BASE_DIR, "action_grid.db"),
    "JEFF_200_CSV": os.path.join(BASE_DIR, "Jeff_Rankings_TOP_200_PPR__SQL_.csv"),
}

SESSION_KEYS = [
    "dfs_engine_slate", "dfs_lab_slate", "dfs_lab_type", 
    "rankings_slate", "parlay_slate", "prizepicks_slate",
    "locked_core_anchors", "live_game_state"
]

def init_session_state(st):
    for key in SESSION_KEYS:
        if key not in st.session_state:
            st.session_state[key] = None
