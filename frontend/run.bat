@echo off
title Dashboard Frontend — DO NOT CLOSE
echo ========================================
echo  Dashboard Frontend  (localhost:3000)
echo  DO NOT CLOSE THIS WINDOW
echo ========================================
echo.
cd /d "%~dp0"
set PATH=C:\Program Files\nodejs;%PATH%
npm run dev
echo.
echo [Frontend stopped. Press any key to exit.]
pause
