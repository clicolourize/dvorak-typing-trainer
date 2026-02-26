@echo off
REM Windows startup script for Dvorak Typing Trainer
setlocal

echo ========================================
echo   Dvorak Typing Trainer
echo ========================================
echo.

REM Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment. Is Python installed?
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment.
    pause
    exit /b 1
)

REM Install dependencies if needed
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)

REM Set Flask environment variables
set FLASK_APP=app.py
set FLASK_ENV=development

REM Start Flask in background and capture output
echo.
echo Starting Flask server...
start /b cmd /c "python -m flask run --host=0.0.0.0 --port=5000 > flask.log 2>&1"

REM Wait for server to start
echo Waiting for server to start...
timeout /t 3 /nobreak >nul

REM Check if Flask started successfully
findstr /C:"Running on" flask.log >nul
if errorlevel 1 (
    echo ERROR: Failed to start Flask server.
    echo Check flask.log for details.
    type flask.log
    pause
    exit /b 1
)

REM Get the actual URL from Flask output
for /f "tokens=4" %%a in ('findstr /C:"Running on" flask.log') do set FLASK_URL=%%a

echo.
echo ========================================
echo   Server started successfully!
echo ========================================
echo.
echo Opening browser at: %FLASK_URL%
echo.
echo Press any key to stop the server...
echo.

REM Open the default browser
start %FLASK_URL%

REM Wait for user to press a key
pause >nul

REM Cleanup on exit
echo.
echo Stopping server...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im flask.exe >nul 2>&1
deactivate 2>nul
endlocal
