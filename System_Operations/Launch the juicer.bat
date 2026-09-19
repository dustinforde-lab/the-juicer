@echo off 
title The Juicer // Quantitative War Room 
color 0A 
cd /d "%%~dp0" 
cls 
echo ======================================================== 
echo    STARTING THE JUICER // LIVE QUANTITATIVE TERMINAL 
echo ======================================================== 
echo [1/2] Fetching live market snapshot and weather feeds... 
python fetcher.py 
echo. 
echo [2/2] Launching Streamlit War Room UI... 
python -m streamlit run app.py 
pause 
