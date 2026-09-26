import sqlite3
import random
import string
import os

def generate_vault_pin():
    """Generates a secure, 4-character ephemeral vault PIN."""
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=4))

def get_vault_path(pin):
    """Returns the sandboxed database path for the given PIN."""
    if not pin or not pin.isalnum() or len(pin) != 4:
        raise ValueError("Invalid Vault PIN format.")
    return f"db_{pin.upper()}.db"

def init_vault(pin):
    """Initializes a private database for the user with necessary tables."""
    db_path = get_vault_path(pin)
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS league_sync_config (
                platform TEXT PRIMARY KEY,
                league_id TEXT,
                team_key TEXT,
                sync_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS private_roster (
                player_name TEXT,
                team TEXT,
                position TEXT,
                acquisition_cost REAL,
                keeper_status TEXT
            )
        """)
        conn.commit()
    return db_path