@echo off
title TicketSystem - H5 Preview (Fast Mode)
echo ============================================
echo   H5 preview (build mode, fast switching)
echo ============================================
echo.
netstat -ano | findstr /c:":8080 " | findstr "LISTENING" >nul 2>nul
if not errorlevel 1 (
    echo [ERROR] Port 8080 in use. Close old preview first.
    pause
    exit /b 1
)
netstat -ano | findstr /c:":8000 " | findstr "LISTENING" >nul 2>nul
if errorlevel 1 (
    echo [WARN] Backend 8000 is NOT running.
    echo        Start it first: double-click start_backend.bat
    pause
    exit /b 1
)
cd /d D:\TicketSystem
start "Ticket-H5Preview" cmd /k "cd /d D:\TicketSystem && D:\TicketSystem\backend\.venv\Scripts\python.exe deploy\preview_server.py"
echo Waiting for preview server...
set /a tries=0
:wait
set /a tries+=1
if %tries% gtr 30 (
    echo [ERROR] Preview did not start.
    pause
    exit /b 1
)
powershell -NoProfile -Command "try{(Invoke-WebRequest -Uri 'http://127.0.0.1:8080/' -UseBasicParsing -TimeoutSec 2).StatusCode}catch{}" | find "200" >nul
if errorlevel 1 goto wait
echo [OK] Preview ready: http://127.0.0.1:8080
start http://127.0.0.1:8080
echo.
echo Remember: rebuild after code changes (npm run build:h5)
pause