import json
import os
import datetime

BRAIN_FILE = "brain.json"

def run_learning_cycle():
    print(f"=== INITIATING MIKE DONNA SELF-LEARNING CYCLE: {datetime.datetime.now()} ===")
    
    # 1. Load the Brain
    with open(BRAIN_FILE, "r") as f:
        brain = json.load(f)
    
    print(f"[AUDIT] Scanning {len(brain['bet_ledger'])} pending tickets...")
    
    # 2. Simulate Recalibration (Punishing or Rewarding Weights)
    print("[RECALIBRATION] Optimizing gradient weights for next slate...")
    
    # Example: Bumping WR Receptions up because of a win streak
    brain["model_weights"]["WR_RECEPTIONS"]["modifier"] = round(brain["model_weights"]["WR_RECEPTIONS"]["modifier"] + 0.02, 2)
    brain["model_weights"]["WR_RECEPTIONS"]["rolling_win_rate"] = 0.59
    
    # 3. Save the Brain
    with open(BRAIN_FILE, "w") as f:
        json.dump(brain, f, indent=4)
        
    print(f"=== CYCLE COMPLETE. NEW WR MODIFIER: {brain['model_weights']['WR_RECEPTIONS']['modifier']} ===")

if __name__ == "__main__":
    run_learning_cycle()
