@echo off
TITLE The Juicer - Master War Room Launcher
cd /d C:\Users\chuck\the-juicer

echo ===================================================
echo [1/3] Launching Mike & Donna + Intern Data Engine...
echo ===================================================
start "The Juicer - Engine & Ledger" cmd /k "python run_intern_pipeline.py && python self_learning_loop.py"

echo ===================================================
echo [2/3] Launching Streamlit War Room Dashboard...
echo ===================================================
:: Added CORS and XSRF flags to allow Ngrok tunnel connections
start "The Juicer - UI Dashboard" cmd /k "streamlit run app.py --server.port 8501 --server.headless false --server.enableCORS false --server.enableXsrfProtection false"

echo ===================================================
echo [3/3] Opening Desktop and Mobile Interfaces...
echo ===================================================
timeout /t 5 >nul

start http://localhost:8501
start msedge --app=http://localhost:8501 --window-size=414,896 2>nul || start chrome --app=http://localhost:8501 --window-size=414,896

echo ===================================================
echo All systems operational for Week 2 kickoff!
echo ===================================================
pause
