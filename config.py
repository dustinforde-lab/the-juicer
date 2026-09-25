import os
APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.environ.get("JUICER_DB_PATH", os.path.join(APP_DIR, "action_grid.db"))
SIM_FILE = os.environ.get("JUICER_SIM_PATH", os.path.join(APP_DIR, "dfs_sim_curve.json"))
LEARNING_MIN_SAMPLE_SIZE = 8
LEARNING_TARGET_HIT_RATE = 0.80  # CLAUDE CHUNK 007: aligned to stated goal (was 0.58)