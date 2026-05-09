@echo off
echo ============================================================
echo  Daily Executive Intelligence Dashboard — One-Time Setup
echo ============================================================
echo.

REM ── Step 1: Check / install Python ──────────────────────────────────────────
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Python not found. Installing via winget...
    winget install Python.Python.3.12 --accept-package-agreements --accept-source-agreements
    echo [INFO] Close and reopen this window after Python installs, then re-run setup.bat
    pause
    exit /b
)
echo [OK] Python found.

REM ── Step 2: Check / install Node.js ─────────────────────────────────────────
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Node.js not found. Installing via winget...
    winget install OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements
    echo [INFO] Close and reopen this window after Node.js installs, then re-run setup.bat
    pause
    exit /b
)
echo [OK] Node.js found.

REM ── Step 3: Backend venv + packages ─────────────────────────────────────────
echo.
echo [STEP] Setting up Python backend...
cd /d "%~dp0..\backend"

if not exist ".venv" (
    python -m venv .venv
    echo [OK] Virtual environment created.
)

call .venv\Scripts\activate.bat
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo [OK] Python packages installed.

REM ── Step 4: NLTK data (needed by sumy) ──────────────────────────────────────
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)"
echo [OK] NLTK data downloaded.

REM ── Step 5: Copy .env ────────────────────────────────────────────────────────
if not exist ".env" (
    copy .env.example .env >nul
    echo [OK] .env file created. Edit backend\.env to add your OpenWeatherMap key.
) else (
    echo [OK] .env already exists.
)

REM ── Step 6: Create data directories ──────────────────────────────────────────
if not exist "..\data\archives" mkdir "..\data\archives"
echo [OK] Data directories ready.

REM ── Step 7: Frontend npm install ─────────────────────────────────────────────
echo.
echo [STEP] Installing frontend packages...
cd /d "%~dp0..\frontend"
call npm install --legacy-peer-deps
echo [OK] Frontend packages installed.

echo.
echo ============================================================
echo  Setup complete!
echo.
echo  Next steps:
echo  1. Edit backend\.env  →  add your OPENWEATHERMAP_API_KEY
echo  2. Run:  scripts\start_servers.bat
echo  3. Open: http://localhost:3000
echo  4. Click "Refresh Now" to load today's data.
echo.
echo  To schedule auto-refresh: run scripts\setup_task_scheduler.bat
echo ============================================================
pause
