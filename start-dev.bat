@echo off
REM CareOps Development Startup Script
REM This opens backend and frontend in two PowerShell windows

echo.
echo ╔════════════════════════════════════════════╗
echo ║   🎯 CareOps - Starting Development       ║
echo ║   Backend: http://localhost:8000          ║
echo ║   Frontend: http://localhost:3000         ║
echo ╚════════════════════════════════════════════╝
echo.

REM Start Backend in new PowerShell window
echo Starting Backend Server...
start powershell -NoExit -Command "cd d:\development\careops\backend; D:/development/.venv/Scripts/python.exe main.py"

timeout /t 3 /nobreak

REM Start Frontend in new PowerShell window
echo Starting Frontend Server...
start powershell -NoExit -Command "cd d:\development\careops\frontend; npm install --legacy-peer-deps; npm run dev"

echo.
echo ✅ Both servers starting in new windows...
echo    Backend: http://localhost:8000
echo    Frontend: http://localhost:3000
echo    API Docs: http://localhost:8000/docs
echo.
echo Wait 30 seconds for both to fully start, then open frontend link
pause
