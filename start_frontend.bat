@echo off
chcp 65001 >nul
title TicketSystem - Start Frontend (Uni-app H5)
cd /d D:\TicketSystem\frontend
echo Starting H5 dev server on http://localhost:5173 ...
npm run dev:h5
pause
