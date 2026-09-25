import sqlite3
import os

DB_PATH = os.path.join(os.getcwd(), "action_grid.db")
conn = sqlite3.connect(DB_PATH)
conn.execute("DROP TABLE IF EXISTS correlation_weights")
conn.commit()
conn.close()
print("✅ Cleared legacy correlation_weights table.")