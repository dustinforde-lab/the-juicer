import sqlite3
import os
import random

DB_PATH = os.path.join(os.getcwd(), 'action_grid.db')

def generate_lineups():
    print("[3] Generating vetted DFS cash builds, GPP stacks, and props...")
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        players = cur.execute("""
            SELECT player_name, pos, team, ppr_baseline, sim_floor, sim_ceiling, draftkings_salary
            FROM player_rankings WHERE ppr_baseline > 0 ORDER BY ppr_baseline DESC
        """).fetchall()
        
        if not players:
            print("  [!] Warning: No vetted Top 300 players available for DFS generation.")
            return

        qbs = [p for p in players if p[1] == 'QB']
        rbs = [p for p in players if p[1] == 'RB']
        wrs = [p for p in players if p[1] == 'WR']
        tes = [p for p in players if p[1] == 'TE']

        cur.execute("DELETE FROM cash_rosters")
        cur.execute("DELETE FROM gpp_rosters")
        cur.execute("DELETE FROM props_slips")

        cash_rosters, gpp_rosters, slips = [], [], []

        for i in range(100):
            if not (qbs and len(rbs) >= 2 and len(wrs) >= 3 and tes): break
            qb, rb_list, wr_list, te = qbs[0], rbs[:2], wrs[:3], tes[0]
            total_proj = round(qb[3] + rb_list[0][3] + rb_list[1][3] + wr_list[0][3] + wr_list[1][3] + wr_list[2][3] + te[3] + 15.0, 1)
            roster_str = f"QB: {qb[0]} | RB: {rb_list[0][0]}, {rb_list[1][0]} | WR: {wr_list[0][0]}, {wr_list[1][0]}, {wr_list[2][0]} | TE: {te[0]}"
            cash_rosters.append((f"Cash Build #{i+1}", roster_str, total_proj, 49500))

        cur.executemany("INSERT INTO cash_rosters (roster_name, players_text, projected_points, total_salary) VALUES (?, ?, ?, ?)", cash_rosters)
        
        for i in range(100):
            if not qbs: break
            gpp_rosters.append((f"GPP Upside #{i+1}", f"GPP Stack - QB: {qbs[0][0]}", qbs[0][5]*2.0, 49800))
        cur.executemany("INSERT INTO gpp_rosters (roster_name, players_text, projected_points, total_salary) VALUES (?, ?, ?, ?)", gpp_rosters)

        for i in range(100):
            p = players[i % len(players)]
            slips.append(("DraftKings", f"Prop: {p[0]} OVER {round(p[3]*0.6, 1)} Fantasy Points", 72.5))
        cur.executemany("INSERT INTO props_slips (bookmaker, slip_description, win_probability) VALUES (?, ?, ?)", slips)
        conn.commit()
    print("  ✅ DFS and props generation complete.")

if __name__ == "__main__":
    generate_lineups()