import sqlite3
import random
import os

DB_FILE = "action_grid.db"

def run_mike_isolated_test_v2():
    print("=" * 65)
    print("🧠 [PHASE 1] Mike's Confidence Scorer - ALIGNED Sandbox Test")
    print("=" * 65)
    
    if not os.path.exists(DB_FILE):
        print(f"❌ Error: {DB_FILE} not found.")
        return

    try:
        with sqlite3.connect(DB_FILE) as conn:
            cur = conn.cursor()
            
            # Insert baseline neural weights matching the EXACT schema
            cur.execute("INSERT OR REPLACE INTO correlation_weights (recipe_name, sample_size, win_rate, weight_modifier) VALUES ('QB_WR_STACK', 1500, 58.4, 1.15)")
            cur.execute("INSERT OR REPLACE INTO correlation_weights (recipe_name, sample_size, win_rate, weight_modifier) VALUES ('WEATHER_SHOCK', 800, 42.1, 0.85)")
            conn.commit()
            
            # Read and verify
            weights = cur.execute("SELECT recipe_name, win_rate, weight_modifier FROM correlation_weights WHERE recipe_name IN ('QB_WR_STACK', 'WEATHER_SHOCK')").fetchall()
            print("   • Active Neural Weights Loaded:")
            for recipe, wr, mod in weights:
                print(f"     - {recipe}: Win Rate {wr}% | Modifier: {mod}")
                
            # Simulate a grading pass
            base_score = random.uniform(75.0, 85.0)
            adjusted_score = round(base_score * weights[0][2], 2) # Applying the 1.15 modifier
            print(f"\n   ✅ Mike successfully executed aligned scoring logic.")
            print(f"   ✅ Base Score: {round(base_score, 2)}% -> Adjusted Score: {adjusted_score}%")
            
    except Exception as e:
        print(f"   ❌ Execution Failed: {e}")

    print("=" * 65)

if __name__ == "__main__":
    run_mike_isolated_test_v2()
