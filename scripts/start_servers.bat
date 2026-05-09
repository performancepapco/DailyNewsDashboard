@echo off
echo ============================================================
echo  Daily Executive Intelligence Dashboard
echo ============================================================
echo.
echo  Starting Backend  (localhost:8000)...
start "Dashboard Backend — DO NOT CLOSE" "%~dp0..\backend\run.bat"

echo  Waiting for backend to start...
timeout /t 7 /nobreak >nul

echo  Starting Frontend (localhost:3000)...
start "Dashboard Frontend — DO NOT CLOSE" "%~dp0..\frontend\run.bat"

echo  Browser will open in 25 seconds (Next.js is compiling)...
timeout /t 25 /nobreak >nul
start http://localhost:3000

echo.
echo ============================================================
echo  Two windows are open — DO NOT CLOSE THEM.
echo  Minimise them instead.
echo.
echo  Dashboard: http://localhost:3000
echo ============================================================
pause
