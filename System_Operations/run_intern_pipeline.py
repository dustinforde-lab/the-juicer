import subprocess
import sys
import time

INTERNS = [
    ("Intern 1 (Vegas Scraper)", "intern_scraper.py"),
    ("Intern 2 (Mike Rankings)", "intern_mike_rankings.py"),
    ("Intern 3 (DFS Optimizer)", "intern_dfs_optimizer.py"),
    ("Intern 4 (Parlay Builder)", "intern_parlays.py"),
    ("Intern 5 (Donna Ledger)", "intern_donna_ledger.py")
]

def run_master_pipeline():
    print("=" * 60)
    print("THE JUICER: EXECUTING FULL WEEK 2 QUANT PIPELINE")
    print("=" * 60)
    
    start_time = time.time()
    
    for name, script in INTERNS:
        print(f"\n>> Activating {name}...")
        result = subprocess.run([sys.executable, script], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[FAILED] {name} encountered an error:\n{result.stderr}")
            return False
        else:
            for line in result.stdout.strip().split("\n"):
                if "===" in line or "[" in line:
                    print(f"   {line}")
                    
    print("\n>> Triggering Donna Autonomous Self-Learning Audit...")
    donna_result = subprocess.run([sys.executable, "self_learning_loop.py"], capture_output=True, text=True)
    if donna_result.returncode == 0:
        for line in donna_result.stdout.strip().split("\n"):
            print(f"   {line}")
    else:
        print(f"[WARNING] Donna loop notice: {donna_result.stderr}")
        
    duration = round(time.time() - start_time, 2)
    print("\n" + "=" * 60)
    print(f"PIPELINE COMPLETE: All tables synced & audited in {duration}s")
    print("=" * 60)
    return True

if __name__ == "__main__":
    run_master_pipeline()
