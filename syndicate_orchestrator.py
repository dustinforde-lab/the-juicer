import os, sys, subprocess, time

# Swapped Chunk 5 to the LIVE web scraper
CHUNKS_TO_SYNC = [
    ("live_medic_poller.py", "Polling LIVE NFL Injuries (The Medic)"),
    ("upgrade_meteorologist.py", "Scanning Stadium Weather (Meteorologist)"),
    ("upgrade_juice_press.py", "Calculating +EV Edges (Juice Press)"),
    ("patch_telemetry_hub.py", "Syncing Slack Telemetry Hub"),
    ("upgrade_lewis_killswitch.py", "Running Lewis QA Kill-Switch"),
    ("upgrade_auto_refill.py", "Auto-Refilling Slips to 200"),
    ("upgrade_confidence_scorer.py", "Applying Mike Confidence Scores & Lewis Gates")
]

def run_syndicate_pipeline():
    print("=" * 65)
    print("[THE JUICER] Executing LIVE Syndicate Intelligence Loop...")
    print("=" * 65)
    start_time = time.time()
    
    sub_env = os.environ.copy()
    sub_env["PYTHONIOENCODING"] = "utf-8"
    
    for script, description in CHUNKS_TO_SYNC:
        print(f"\n>> Running Step: {description}...")
        result = subprocess.run([sys.executable, script], capture_output=True, text=True, encoding="utf-8", errors="replace", env=sub_env)
        if result.returncode != 0:
            print(f"PIPELINE HALTED AT: {script}")
            print(result.stderr)
            sys.exit(1)
            
        for line in result.stdout.splitlines():
            if any(k in line for k in ["ALL", "ONLINE", "Refill Complete", "SUCCESS", "GATES", "LIVE ALERT"]):
                print(f"   {line}")
                
    elapsed = round(time.time() - start_time, 2)
    print("\n" + "=" * 65)
    print(f"LIVE SYNDICATE PIPELINE FINISHED IN {elapsed}s")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    run_syndicate_pipeline()
