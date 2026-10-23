@echo off
title TicketSystem - Start All
echo ============================================
echo   Ticket System - one-click launcher
echo ============================================
echo.

rem ===== 端口占用预检：防止重复启动出两个实例 =====
netstat -ano | findstr /c:":8000 " | findstr "LISTENING" >nul 2>nul
if not errorlevel 1 (
    echo [ERROR] 端口 8000 已被占用，可能有后端实例已在运行。
    echo         请先关闭旧的后端窗口，或结束占用 8000 的进程，再重新启动。
    pause
    exit /b 1
)
netstat -ano | findstr /c:":5173 " | findstr "LISTENING" >nul 2>nul
if not errorlevel 1 (
    echo [ERROR] 端口 5173 已被占用，可能有前端实例已在运行。
    echo         请先关闭旧的前端窗口，或结束占用 5173 的进程，再重新启动。
    pause
    exit /b 1
)

cd /d D:\TicketSystem\backend
start "Ticket-Backend" cmd /k "cd /d D:\TicketSystem\backend && .venv\Scripts\python.exe manage.py runserver 0.0.0.0:8000"
echo [1/3] Django backend starting...  http://127.0.0.1:8000

cd /d D:\TicketSystem\frontend
start "Ticket-Frontend" cmd /k "cd /d D:\TicketSystem\frontend && npm run dev:h5"
echo [2/3] Uni-app H5 starting...      http://localhost:5173

echo.
echo Waiting for services to be ready (first start may take 10-30s)...
set /a tries=0

:wait_backend
set /a tries+=1
if %tries% gtr 90 (
    echo.
    echo [ERROR] Backend did not start within 90s. Check the "Ticket-Backend" window.
    pause
    exit /b 1
)
powershell -NoProfile -Command "try{(Invoke-WebRequest -Uri 'http://127.0.0.1:8000/api/events/' -UseBasicParsing -TimeoutSec 2).StatusCode}catch{}" | find "200" >nul
if errorlevel 1 goto wait_backend
echo [OK] Backend ready (8000)

set /a tries=0
:wait_frontend
set /a tries+=1
if %tries% gtr 120 (
    echo.
    echo [ERROR] Frontend did not start within 120s. Check the "Ticket-Frontend" window.
    pause
    exit /b 1
)
powershell -NoProfile -Command "try{(Invoke-WebRequest -Uri 'http://127.0.0.1:5173/' -UseBasicParsing -TimeoutSec 2).StatusCode}catch{}" | find "200" >nul
if errorlevel 1 goto wait_frontend
echo [OK] Frontend ready (5173)

echo [3/3] Opening browser...
start http://localhost:5173
echo.
echo Admin backend:  http://127.0.0.1:8000/admin/  (admin / admin123456)
echo Frontend H5:    http://localhost:5173
echo.
echo Done! Close the two service windows to stop the servers.
pause
