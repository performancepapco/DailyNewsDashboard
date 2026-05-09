@echo off
echo ============================================================
echo  Setting up Windows Task Scheduler for 09:00 AM IST daily
echo ============================================================
echo.
echo [INFO] This creates a scheduled task called "DailyIntelligenceDashboard"
echo        that runs run_daily.bat at 09:00 AM IST (09:00 local time).
echo.
echo [INFO] NOTE: The backend must be running before the task fires.
echo        Start it manually with start_servers.bat, or set up NSSM
echo        to run it as a Windows service (see README).
echo.

schtasks /create ^
  /tn "DailyIntelligenceDashboard" ^
  /tr "\"%~dp0run_daily.bat\"" ^
  /sc DAILY ^
  /st 09:00 ^
  /f ^
  /rl HIGHEST

if %errorlevel% equ 0 (
    echo.
    echo [OK] Task created successfully!
    echo      Name:    DailyIntelligenceDashboard
    echo      Runs at: 09:00 AM (local IST time) every day
    echo      Script:  %~dp0run_daily.bat
) else (
    echo.
    echo [ERROR] Failed to create task. Try running this script as Administrator.
    echo         Right-click setup_task_scheduler.bat → "Run as administrator"
)

pause
