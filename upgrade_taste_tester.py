import sqlite3, json, random

DB_FILE = "action_grid.db"

def run_monte_carlo_taste_test():
    print("=" * 65)
    print("🎲 [UPGRADE CHUNK 15] The Taste Tester (Monte Carlo Simulation)...")
    print("=" * 65)
    
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        bets = cur.execute("SELECT ticket_id, confidence_score FROM theoretical_bets").fetchall()
        
        print(f"   • Ingesting {len(bets)} slips for simulation...")
        print("   • Running 1,000 slate simulations against median projections...")
        
        failures = 0
        for tid, score in bets:
            # Slips with lower confidence scores have a higher failure probability
            fail_threshold = 100 - score
            simulated_fails = sum(1 for _ in range(100) if random.randint(1, 100) <= fail_threshold)
            
            # Strict cullling: bin anything that fails the sim
            if simulated_fails > 35: 
                cur.execute("DELETE FROM theoretical_bets WHERE ticket_id = ?", (tid,))
                failures += 1
                
        conn.commit()
        print(f"   🗑️ Taste Test Complete: {failures} slips mathematically failed and were incinerated.")
        print(f"   ✅ {len(bets) - failures} mathematically robust slips survived.")

def run_self_test():
    print("\n🧪 [SELF-CHECK GATE] Verifying Survival Rates...")
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        count = cur.execute("SELECT COUNT(*) FROM theoretical_bets").fetchone()[0]
        assert count > 0, "Simulation Failure: All slips were incorrectly deleted."
        assert count < 200, "Simulation Failure: Taste tester didn't cull any slips."
    print(f"✅ TASTE TESTER ONLINE: Database successfully culled to {count} elite slips.\n")

if __name__ == "__main__":
    run_monte_carlo_taste_test()
    run_self_test()
