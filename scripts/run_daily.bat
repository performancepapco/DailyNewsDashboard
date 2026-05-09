@echo off
REM This script is called by Windows Task Scheduler at 09:00 AM IST daily.
REM It triggers the FastAPI /api/refresh endpoint to fetch fresh news.

curl -s -X POST http://localhost:8000/api/refresh >nul 2>&1
if %errorlevel% equ 0 (
    echo [%date% %time%] Daily refresh triggered successfully. >> "%~dp0..\data\refresh.log"
) else (
    echo [%date% %time%] ERROR: Could not reach backend. Is it running? >> "%~dp0..\data\refresh.log"
)
