@echo off
REM CareOps Deployment Script for Windows
REM Automated deployment to Vercel & Render

setlocal enabledelayedexpansion

echo.
echo ====================================
echo CareOps Deployment Script (Windows)
echo ====================================
echo.

REM Step 1: Check Git
echo [1/6] Checking Git repository...
git rev-parse --git-dir >nul 2>&1
if errorlevel 1 (
    echo ERROR: Not a git repository. Run 'git init' first
    exit /b 1
)
echo OK: Git repository found
echo.

REM Step 2: Check .env files
echo [2/6] Checking environment configuration...
if not exist "backend\.env" (
    echo ERROR: backend\.env not found
    echo Copy backend\.env.example to backend\.env and fill in values
    exit /b 1
)
echo OK: backend\.env found

if not exist "frontend\.env.local" (
    echo WARNING: frontend\.env.local not found
    copy "frontend\.env.example" "frontend\.env.local" >nul
    echo OK: Created frontend\.env.local from example
)
echo.

REM Step 3: Test Python syntax
echo [3/6] Testing backend syntax...
cd backend
python -m py_compile main.py >nul 2>&1
if errorlevel 1 (
    echo ERROR: Backend syntax error
    exit /b 1
)
echo OK: Backend syntax check passed
cd ..
echo.

REM Step 4: Test frontend build
echo [4/6] Testing frontend build...
cd frontend
echo Building frontend... (this may take ~30 seconds)
call npm run build >nul 2>&1
if errorlevel 1 (
    echo ERROR: Frontend build failed
    echo Run 'npm run build' in frontend directory to see details
    cd ..
    exit /b 1
)
echo OK: Frontend build successful
cd ..
echo.

REM Step 5: Commit to Git
echo [5/6] Committing changes...
git add . >nul 2>&1
git commit -m "Deploy to production" >nul 2>&1
if errorlevel 0 (
    git push origin main >nul 2>&1
    echo OK: Changes committed and pushed
) else (
    echo INFO: No changes to commit
)
echo.

REM Step 6: Show instructions
echo [6/6] Deployment Instructions
echo ====================================
echo.
echo BACKEND DEPLOYMENT (Render)
echo ---------------------------
echo 1. Go to https://render.com
echo 2. Sign in with GitHub
echo 3. Click "New +" -^> "Web Service"
echo 4. Connect your careops repository
echo 5. Fill in:
echo    Name: careops-api
echo    Runtime: Python 3.11
echo    Region: Oregon (us-west)
echo    Branch: main
echo.
echo 6. Click "Advanced" and:
echo    Build Command: pip install -r requirements.txt
echo    Start Command: gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:10000
echo.
echo 7. Add PostgreSQL database:
echo    Click "New +" -^> "PostgreSQL"
echo    Name: careops_db
echo.
echo 8. Set Environment Variables (copy from backend\.env):
echo    DATABASE_URL: (from Render PostgreSQL)
echo    JWT_SECRET: your-secret-key
echo    SMTP_HOST: smtp.gmail.com
echo    SMTP_PORT: 587
echo    SMTP_USER: your-email@gmail.com
echo    SMTP_PASSWORD: your-app-password
echo    FRONTEND_URL: https://careops.vercel.app (update after Vercel deploy)
echo.
echo 9. Click "Create Web Service"
echo 10. Copy your Backend URL: https://careops-api-XXXXX.onrender.com
echo.
echo FRONTEND DEPLOYMENT (Vercel)
echo ----------------------------
echo 1. Go to https://vercel.com
echo 2. Sign in with GitHub
echo 3. Click "Add New" -^> "Project"
echo 4. Import your careops repository
echo 5. Fill in:
echo    Project Name: careops
echo    Framework Preset: Next.js
echo    Root Directory: frontend
echo.
echo 6. Set Environment Variable:
echo    NEXT_PUBLIC_API_URL: https://careops-api-XXXXX.onrender.com (from Render)
echo.
echo 7. Click "Deploy"
echo 8. Copy your Frontend URL: https://careops-XXXXX.vercel.app
echo.
echo TEST AFTER DEPLOYMENT
echo --------------------
echo 1. Visit https://careops-XXXXX.vercel.app
echo 2. Register new account
echo 3. Create workspace
echo 4. Create contact (should send email)
echo 5. Create booking (should send email + SMS)
echo 6. Check inbox and dashboard
echo.
echo DONE!
echo ====================================
echo.
pause
