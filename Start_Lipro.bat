@echo off
echo ===================================================
echo     LIPRO - SIH 2026 PROTOTYPE LAUNCHER
echo ===================================================
echo.
set "PROJECT_ROOT=%~dp0"

echo [1/4] Checking Backend AI Environment...
cd /d "%PROJECT_ROOT%backend"
if not exist ".venv" (
    echo Building Python AI Environment ^(This will take 1-2 minutes the first time^)...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    echo Backend environment is ready!
)

echo.
echo [2/4] Checking Frontend UI Environment...
cd /d "%PROJECT_ROOT%frontend"
if not exist "node_modules" (
    echo Installing React dependencies ^(This will take 1 minute the first time^)...
    call npm install
) else (
    echo Frontend environment is ready!
)

echo.
echo [3/4] Starting Lipro AI Backend...
cd /d "%PROJECT_ROOT%backend"
set PYTHONPATH=%PROJECT_ROOT%backend
start "Lipro Backend Engine" cmd /k "call .venv\Scripts\activate.bat && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000"

timeout /t 4 > nul

echo.
echo [4/4] Starting Lipro UI Frontend...
cd /d "%PROJECT_ROOT%frontend"
start "Lipro Frontend Dashboard" cmd /k "npm run dev"

echo.
echo ===================================================
echo Everything is running! Opening your web browser...
echo ===================================================
timeout /t 4 > nul
start http://localhost:5173
