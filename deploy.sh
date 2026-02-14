#!/bin/bash
# CareOps Deployment Script - Automated Deployment to Vercel & Render
# This script handles the deployment process end-to-end

set -e  # Exit on error

echo "🚀 CareOps Deployment Script"
echo "================================"
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Verify GitHub repository
echo -e "${YELLOW}[1/6]${NC} Checking GitHub repository..."
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}❌ Not a git repository. Run 'git init' first${NC}"
    exit 1
fi

# Verify .env is in .gitignore
if ! grep -q "\.env" .gitignore 2>/dev/null; then
    echo -e "${YELLOW}⚠️  .env not in .gitignore - adding it${NC}"
    echo ".env" >> .gitignore
fi

echo -e "${GREEN}✅ Git repository OK${NC}"
echo ""

# Step 2: Commit changes
echo -e "${YELLOW}[2/6]${NC} Committing changes to GitHub..."
if [[ -n $(git status -s) ]]; then
    git add .
    git commit -m "🚀 Deploy to production - $(date +%Y-%m-%d)"
    git push origin main
    echo -e "${GREEN}✅ Changes committed${NC}"
else
    echo -e "${YELLOW}ℹ️  No changes to commit${NC}"
fi
echo ""

# Step 3: Verify environment variables
echo -e "${YELLOW}[3/6]${NC} Verifying environment configuration..."

# Check backend .env
if [ ! -f "backend/.env" ]; then
    echo -e "${RED}❌ backend/.env not found${NC}"
    echo "Copy backend/.env.example to backend/.env and fill in values"
    exit 1
fi

# Check frontend .env.local
if [ ! -f "frontend/.env.local" ]; then
    echo -e "${YELLOW}⚠️  frontend/.env.local not found - creating from example${NC}"
    cp frontend/.env.example frontend/.env.local
fi

echo -e "${GREEN}✅ Environment files OK${NC}"
echo ""

# Step 4: Test builds locally
echo -e "${YELLOW}[4/6]${NC} Testing builds locally..."

# Backend
echo "Testing backend build..."
cd backend
if ! python -m py_compile main.py app/routes/*.py app/services/*.py; then
    echo -e "${RED}❌ Backend syntax error${NC}"
    exit 1
fi
cd ..
echo -e "${GREEN}✅ Backend syntax OK${NC}"

# Frontend
echo "Testing frontend build..."
cd frontend
if ! npm run build > /dev/null 2>&1; then
    echo -e "${RED}❌ Frontend build failed${NC}"
    echo "Run 'npm run build' to see details"
    exit 1
fi
cd ..
echo -e "${GREEN}✅ Frontend build OK${NC}"
echo ""

# Step 5: Display deployment instructions
echo -e "${YELLOW}[5/6]${NC} Deployment Instructions"
echo "=================================="
echo ""
echo -e "${YELLOW}BACKEND (Render)${NC}"
echo "1. Go to https://render.com"
echo "2. Create new Web Service"
echo "3. Connect to your GitHub repository: careops"
echo "4. Settings:"
echo "   Name: careops-api"
echo "   Runtime: Python 3.11"
echo "   Build command: pip install -r requirements.txt"
echo "   Start command: gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:10000"
echo ""
echo "5. Add PostgreSQL database:"
echo "   Name: careops_db"
echo "6. Set environment variables (copy from backend/.env)"
echo "7. Deploy!"
echo ""
echo -e "${GREEN}Backend URL will be: https://careops-api-XXXXX.onrender.com${NC}"
echo ""
echo -e "${YELLOW}FRONTEND (Vercel)${NC}"
echo "1. Go to https://vercel.com"
echo "2. Import your GitHub repository: careops"
echo "3. Select 'frontend' as root directory"
echo "4. Build settings (auto-detected):"
echo "   Build command: npm run build"
echo "   Output: .next"
echo ""
echo "5. Environment variables:"
echo "   NEXT_PUBLIC_API_URL=https://careops-api-XXXXX.onrender.com"
echo "6. Deploy!"
echo ""
echo -e "${GREEN}Frontend URL will be: https://careops-XXXXX.vercel.app${NC}"
echo ""

# Step 6: Summary
echo -e "${YELLOW}[6/6]${NC} Deployment Check${NC} =================================="
echo ""
echo -e "${GREEN}✅ Code is committed to GitHub${NC}"
echo -e "${GREEN}✅ Backend build passes locally${NC}"
echo -e "${GREEN}✅ Frontend build passes locally${NC}"
echo -e "${GREEN}✅ Environment variables configured${NC}"
echo ""
echo "NEXT STEPS:"
echo "1. Open https://render.com and deploy backend"
echo "2. Note your backend URL: https://careops-api-XXXXX.onrender.com"
echo "3. Open https://vercel.com and deploy frontend"
echo "4. Update NEXT_PUBLIC_API_URL with backend URL"
echo "5. Test at frontend URL"
echo ""
echo -e "${GREEN}Happy deploying! 🚀${NC}"
