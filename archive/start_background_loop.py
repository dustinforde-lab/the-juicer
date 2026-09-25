import os
import time
import subprocess
from datetime import datetime

def run_continuous_loop():
    print("=" * 65)
    print("🔄 [24/7 BACKGROUND RUNNER] Initializing Continuous Syndication Loop...")
    print("Press Ctrl+C to safely pause the background loop at any time.")
    print("=" * 65)
    
    cycle_count = 0
    try:
        while True:
            cycle_count += 1
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"\n⏱️ [{current_time}] Triggering Background Daemon Cycle #{cycle_count}...")
            
            # Execute the live master daemon script
            result = subprocess.run(["python", "master_daemon_live.py"], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("   ✅ Cycle completed successfully. All contingencies armed.")
            else:
                print(f"   ⚠️ Cycle warning detected. Check logs:\n{result.stderr}")
                
            print(f"   💤 Sleeping for 15 minutes before next scheduled sweep...")
            
            # Wait 15 minutes (900 seconds) between cycles
            # (For immediate testing, you can shorten this, but 15 mins is standard for sports syndicates)
            time.sleep(900)
            
    except KeyboardInterrupt:
        print("\n" + "=" * 65)
        print("🛑 [BACKGROUND RUNNER] Paused safely by Managing Partner.")
        print("=" * 65)

if __name__ == "__main__":
    run_continuous_loop()
