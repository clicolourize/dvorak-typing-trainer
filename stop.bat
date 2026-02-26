@echo off
REM Windows stop script for Dvorak Typing Trainer

echo ========================================
echo   Stopping Dvorak Typing Trainer
echo ========================================
echo.

REM Kill Flask processes
echo Stopping Python/Flask processes...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im pythonw.exe >nul 2>&1

REM Kill any process running on port 5000
echo Checking for processes on port 5000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5000 ^| findstr LISTENING') do (
    echo Killing process %%a on port 5000...
    taskkill /F /PID %%a >nul 2>&1
)

echo.
echo Server stopped.
echo.
pause
