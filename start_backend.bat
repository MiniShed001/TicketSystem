@echo off
title TicketSystem - Start Backend (Django)
netstat -ano | findstr /c:":8000 " | findstr "LISTENING" >nul 2>nul
if not errorlevel 1 (
    echo [ERROR] 端口 8000 已被占用，可能有后端实例已在运行。
    echo         请先关闭旧的后端窗口，或结束占用 8000 的进程，再重新启动。
    pause
    exit /b 1
)
cd /d D:\TicketSystem\backend
echo Starting Django backend on http://0.0.0.0:8000 ...
".venv\Scripts\python.exe" manage.py runserver 0.0.0.0:8000
pause
