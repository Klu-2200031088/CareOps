@echo off
REM CareOps Development Setup Script for Windows

echo 🚀 Starting CareOps Development Environment...
echo.

REM Create backend .env if it doesn't exist
if not exist backend\.env (
    echo Creating backend\.env...
    copy backend\.env.example backend\.env
)

REM Create frontend .env.local if it doesn't exist
if not exist frontend\.env.local (
    echo Creating frontend\.env.local...
    (
        echo NEXT_PUBLIC_API_URL=http://localhost:8000/api
    ) > frontend\.env.local
)

REM Install backend dependencies
echo.
echo 📦 Installing backend dependencies...
cd backend
pip install -q -r requirements.txt
cd ..

REM Install frontend dependencies
echo.
echo 📦 Installing frontend dependencies...
cd frontend
call npm install -q
cd ..

echo.
echo ✅ Setup complete!
echo.
echo To start development:
echo   Terminal 1: cd backend ^&^& python main.py
echo   Terminal 2: cd frontend ^&^& npm run dev
echo.
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
pause
