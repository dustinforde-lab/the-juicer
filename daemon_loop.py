import os
import time
from datetime import datetime
import subprocess

def run_pipeline_cycle():
    current_time = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    print(f"\n[!] BACKGROUND DAEMON PULSE: {current_time}")
    
    steps = [
        ("Live Ingest", ["python", "live_ingest.py"]),
        ("Donna Learning Recalibration", ["python", "-c", "import learning_loop; print(learning_loop.recalculate_weights())"]),
        ("Monte Carlo Evaluator V2", ["python", "mike_evaluator_v2.py"]),
        ("DFS & Slips Generator", ["python", "generate_dfs.py"])
    ]
    
    for name, cmd in steps:
        print(f"  -> Executing {name}...")
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"     [X] Error in {name}: {res.stderr.strip()[:150]}")
            return False
        else:
            print(f"     [✓] {name} completed successfully.")
            
    print(f"  ✅ CYCLE COMPLETE. Next hourly pulse in 60 minutes.\n")
    return True

if __name__ == "__main__":
    print("\n" + "="*65)
    print(" 🕰️ SMART-SCHEDULED BACKGROUND DAEMON ACTIVATED")
    print("="*65)
    print(" Running hybrid ingest and simulation loop every 60 minutes.")
    print(" Close this window to terminate the background process.")
    print("="*65 + "\n")
    
    consecutive_errors = 0
    while True:
        try:
            success = run_pipeline_cycle()
            if not success:
                consecutive_errors += 1
            else:
                consecutive_errors = 0
                
            # Back off for 5 minutes if we hit 3 consecutive errors
            sleep_time = 300 if consecutive_errors >= 3 else 3600
            if consecutive_errors >= 3:
                print(f"  [!] Warning: {consecutive_errors} consecutive failures. Backing off for 5 minutes...")
                
            time.sleep(sleep_time)
        except KeyboardInterrupt:
            print("\n[!] Daemon terminated by user.")
            break
        except Exception as e:
            print(f"\n[X] Critical Daemon Exception: {e}. Retrying in 60 seconds...")
            time.sleep(60)