import sqlite3
import os
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "action_grid.db")
with sqlite3.connect(DB_PATH) as conn:
    conn.execute("DROP TABLE IF EXISTS vegas_lines")
