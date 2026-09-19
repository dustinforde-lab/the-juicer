import os
import subprocess
import sys

def launch_war_room():
    print("="*65)
    print("🚀 [MASTER LAUNCHER] Booting The Juicer War Room...")
    print("="*65)
    
    # 1. Run Lewis's Watchdog Health Check
    print("🤖 Step 1: Running Lewis's Watchdog & System Diagnostics...")
    if os.path.exists("lewis_watchdog.py"):
        subprocess.run([sys.executable, "lewis_watchdog.py"])
    
    # 2. Run Team-Level Auto-Cleanser
    print("\n🛡️ Step 2: Executing Donna's Team-Level Slate Cleanse...")
    if os.path.exists("team_cleanser.py"):
        subprocess.run([sys.executable, "team_cleanser.py"])

    # 3. Terminate any existing Streamlit processes on port 8501
    print("\n🧹 Step 3: Clearing port 8501...")
    subprocess.run([
        "powershell", 
        "-Command", 
        "Get-NetTCPConnection -LocalPort 8501 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }"
    ], capture_output=True)

    # 4. Launch Streamlit War Room
    print("\n🔥 Step 4: Launching Streamlit Master Application...")
    print("="*65)
    print("🎯 War Room active at: http://localhost:8501")
    print("="*65)
    subprocess.run(["streamlit", "run", "app.py", "--server.port", "8501", "--server.enableCORS", "false", "--server.enableXsrfProtection", "false"])

if __name__ == "__main__":
    launch_war_room()
