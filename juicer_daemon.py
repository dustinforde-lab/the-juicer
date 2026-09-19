import time
import subprocess
import sys
import os
from datetime import datetime

# Set interval in seconds (900 seconds = 15 minutes)
SYNC_INTERVAL = 900 

def start_daemon():
    print("=" * 65)
    print("🤖 [AUTOPILOT ENGAGED] The Juicer Daemon is now LIVE.")
    print("=" * 65)
    print(f"   • Auto-syncing injuries, weather & +EV lines every {SYNC_INTERVAL // 60} minutes.")
    print("   • Auto-purging and refilling slips continuously.")
    print("   • Press Ctrl+C to stop the daemon.\n")
    
    sub_env = os.environ.copy()
    sub_env["PYTHONIOENCODING"] = "utf-8"
    
    cycle_count = 1
    
    try:
        while True:
            now = datetime.now().strftime("%I:%M:%S %p")
            print(f"[{now}] 🔄 [CYCLE {cycle_count}] Initiating Background Syndicate Sync...")
            
            # Run the orchestrator. We suppress stdout so it doesn't flood the terminal,
            # but keep stderr in case of critical crashes.
            result = subprocess.run(
                [sys.executable, "syndicate_orchestrator.py"],
                env=sub_env,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True
            )
            
            if result.returncode != 0:
                print(f"   ❌ CRITICAL ERROR in Cycle {cycle_count}:")
                print(result.stderr)
            else:
                now_done = datetime.now().strftime("%I:%M:%S %p")
                print(f"[{now_done}] ✅ Cycle Complete. Database optimized. Sleeping...")
                
            cycle_count += 1
            time.sleep(SYNC_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n🛑 [AUTOPILOT DISABLED] Juicer Daemon powering down.")

if __name__ == "__main__":
    start_daemon()
