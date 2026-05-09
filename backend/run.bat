@echo off
title Dashboard Backend — DO NOT CLOSE
echo ========================================
echo  Dashboard Backend  (localhost:8000)
echo  DO NOT CLOSE THIS WINDOW
echo ========================================
echo.
cd /d "%~dp0"
call .venv\Scripts\activate.bat
python main.py
echo.
echo [Backend stopped. Press any key to exit.]
pause
