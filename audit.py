import sqlite3

with sqlite3.connect("action_grid.db") as conn:
    cur = conn.cursor()
    
    cash = cur.execute("SELECT COUNT(*) FROM dfs_rosters WHERE lineup_type = 'CASH'").fetchone()[0]
    gpp = cur.execute("SELECT COUNT(*) FROM dfs_rosters WHERE lineup_type = 'GPP'").fetchone()[0]
    parlays = cur.execute("SELECT COUNT(*) FROM slips WHERE platform = 'SPORTSBOOK_PARLAY'").fetchone()[0]
    prizepicks = cur.execute("SELECT COUNT(*) FROM slips WHERE platform = 'PRIZEPICKS'").fetchone()[0]
    underdog = cur.execute("SELECT COUNT(*) FROM slips WHERE platform = 'UNDERDOG'").fetchone()[0]
    
    print(f"  -> Cash Rosters:       {cash} / 100")
    print(f"  -> GPP Rosters:        {gpp} / 100")
    print(f"  -> Sportsbook Parlays: {parlays} / 200")
    print(f"  -> PrizePicks Slips:   {prizepicks} / 100")
    print(f"  -> Underdog Slips:     {underdog} / 100")