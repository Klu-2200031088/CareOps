# Deployment Guide - Complete Step-by-Step

**Status:** Ready to deploy  
**Estimated Time:** 30 minutes (both platforms)  
**Difficulty:** Easy (following this guide)

---

## 🎯 DEPLOYMENT OVERVIEW

```
Your Local Machine
        ↓
    GitHub
        ↓
    ┌───────────────────────┐
    │   Vercel (Frontend)   │ ← https://careops.vercel.app
    │   Render (Backend)    │ ← https://careops-api.onrender.com
    └───────────────────────┘
```

---

## 📋 PRE-DEPLOYMENT CHECKLIST

Before you start, verify:

- [ ] GitHub account created
- [ ] Vercel account created (signup with GitHub)
- [ ] Render account created (signup with GitHub)
- [ ] All code committed to GitHub
- [ ] `.env` file configured locally
- [ ] Backend runs locally without errors
- [ ] Frontend builds locally without errors

---

## ✅ PHASE 1: PREPARE SOURCE CODE

### Step 1.1: Create GitHub Repository

```bash
# In careops folder
cd careops

# Initialize git if not already done
git init

# Add remote (replace with your GitHub URL)
git remote add origin https://github.com/YOUR_USERNAME/careops.git

# Create .gitignore
echo "__pycache__/
*.pyc
*.egg-info/
.env
.venv/
venv/
node_modules/
.next/
dist/
build/
*.log
.DS_Store" > .gitignore

# Commit everything
git add .
git commit -m "🚀 Initial commit - CareOps MVP ready for deployment"

# Push to GitHub (main branch)
git branch -M main
git push -u origin main
```

### Step 1.2: Verify .env Files

**Backend (.env) - NEEDED FOR LOCAL, NOT GITHUB:**
```env
# Database
DATABASE_URL=sqlite:///./careops.db

# JWT
JWT_SECRET=your-random-secret-key-here

# Email (Gmail SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# SMS (Twilio - optional)
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=+1234567890

# Frontend URL
FRONTEND_URL=http://localhost:3000
```

**Frontend (.env.local) - LOCAL ONLY:**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🚀 PHASE 2: DEPLOY BACKEND TO RENDER

### Step 2.1: Create Render Account

1. Go to https://render.com
2. Sign up with GitHub
3. Authorize Render to access your GitHub

### Step 2.2: Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Select your **`careops`** repository
3. Fill in configuration:

```
Name: careops-api
Environment: Python 3
Region: Oregon (us-west)
Branch: main
Repo Dir: backend (if folder structure is backend/ separate)
```

### Step 2.3: Configure Build & Run

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:10000
```

> **Note:** Click on "Advanced" to add these as separate fields

### Step 2.4: Add Environment Variables

In Render dashboard → Environment:

```
DATABASE_URL = postgresql://...:...@...:5432/careops_db
JWT_SECRET = your-production-secret-key-change-this
SMTP_HOST = smtp.gmail.com
SMTP_PORT = 587
SMTP_USER = your-email@gmail.com
SMTP_PASSWORD = your-app-password
TWILIO_ACCOUNT_SID = your_sid
TWILIO_AUTH_TOKEN = your_token
TWILIO_PHONE_NUMBER = +1234567890
FRONTEND_URL = https://careops.vercel.app
```

### Step 2.5: Add PostgreSQL Database

1. Click **"New +"** → **"PostgreSQL"**
2. Name: `careops_db`
3. Create instance
4. Copy the **connection string**
5. Add to environment variables as `DATABASE_URL`

### Step 2.6: Deploy

1. Click **"Create Web Service"**
2. Wait for deployment (2-3 minutes)
3. Once **"Live"** status appears, copy the URL

```
https://careops-api-xxxxx.onrender.com
```

**Test the backend:**
```bash
curl https://careops-api-xxxxx.onrender.com/docs
# Should show Swagger API docs
```

---

## 📦 PHASE 3: DEPLOY FRONTEND TO VERCEL

### Step 3.1: Create Vercel Account

1. Go to https://vercel.com
2. Sign up with GitHub
3. Authorize Vercel to access your GitHub

### Step 3.2: Import Project

1. Click **"New Project"** or **"Add New..."**
2. Select your **`careops`** repository
3. Click **"Import"**

### Step 3.3: Configure Frontend

**Framework Preset:** Next.js (auto-detected)

**Root Directory:** `frontend`

**Build Settings:**
- Build Command: `npm run build`
- Output Directory: `.next`
- Install Command: `npm ci`

### Step 3.4: Add Environment Variables

In Vercel project settings → Environment Variables:

```
NEXT_PUBLIC_API_URL = https://careops-api-xxxxx.onrender.com
```

> **Important:** Use the Render backend URL from Phase 2

### Step 3.5: Deploy

1. Click **"Deploy"**
2. Wait for deployment (1-2 minutes)
3. Once complete, you get a URL:

```
https://careops.vercel.app
https://careops-xxxxx.vercel.app
```

**Test the frontend:**
```bash
Visit https://careops.vercel.app in your browser
Should load the login page
```

---

## 🔗 PHASE 4: CONNECT FRONTEND & BACKEND

### Step 4.1: Update Backend CORS

Go to Render dashboard → Environment Variables

Update `FRONTEND_URL`:
```
FRONTEND_URL = https://careops-xxxxx.vercel.app
```

### Step 4.2: Verify Connection

**In Vercel:**
1. Go to your frontend URL
2. Register new account
3. Should successfully create workspace
4. Create contact → should not error

**If getting CORS errors:**
- Check `FRONTEND_URL` in Render environment
- Trigger redeploy in Render (Settings → Deploy)

---

## ✅ PHASE 5: VERIFICATION CHECKLIST

### Frontend Tests
```
[ ] Frontend loads at https://careops.vercel.app
[ ] Can navigate to login page
[ ] Can register new user
[ ] Can create workspace
[ ] Can create contact
[ ] Dashboard loads without API errors
[ ] Responsive design works on mobile
[ ] No 404 errors in console
```

### Backend Tests
```
[ ] API docs available at /docs
[ ] Health check: GET /
[ ] Users can register
[ ] JWT tokens generated correctly
[ ] Database queries work
[ ] Email integration active
[ ] SMS integration active
[ ] CORS allows frontend origin
```

### Integration Tests
```
[ ] Frontend successfully calls backend APIs
[ ] User authentication flow works end-to-end
[ ] Workspace creation saves to database
[ ] Contact creation triggers email
[ ] Booking creation triggers email + SMS
[ ] Inbox messaging works
[ ] Dashboard stats accurate
[ ] Inventory tracking works
```

---

## 🚨 TROUBLESHOOTING

### Backend won't deploy
```
❌ Problem: Build fails
✅ Solution: Check logs in Render → Deployments
           Verify requirements.txt has all dependencies
           Check for Python syntax errors

❌ Problem: Runtime crashes
✅ Solution: Check if DATABASE_URL is set
           Verify SMTP credentials are correct
           Check if gunicorn is installed
```

### Frontend won't deploy
```
❌ Problem: Build fails
✅ Solution: Check logs in Vercel → Deployments
           Verify all imports are correct
           Check for TypeScript errors
           Run 'npm run build' locally first

❌ Problem: Can't connect to backend
✅ Solution: Check NEXT_PUBLIC_API_URL in Vercel settings
           Verify backend Render URL is correct
           Check browser console for CORS errors
           Make sure backend is running (Render status)
```

### Backend crashes after deployment
```
❌ Problem: Database errors
✅ Solution: Verify PostgreSQL is running on Render
           Check if migrations are needed
           Check DATABASE_URL format

❌ Problem: Email not sending
✅ Solution: Verify SMTP credentials are correct
           Gmail requires app password (16 chars)
           Check Render logs for email errors

❌ Problem: CORS errors
✅ Solution: Update FRONTEND_URL in Render
           Redeploy backend after changing env vars
           Check if frontend URL has trailing slash
```

---

## 📊 DEPLOYMENT CHECKLIST

```
GITHUB
[ ] All code committed
[ ] .gitignore prevents uploading .env
[ ] Repository is public (or private, up to you)

RENDER (BACKEND)
[ ] Web Service created
[ ] PostgreSQL database created
[ ] Environment variables set
[ ] Build command configured
[ ] Start command configured
[ ] Deployment successful (Status: Live)
[ ] API docs accessible at /docs
[ ] Backend URL: ___________________

VERCEL (FRONTEND)
[ ] Project imported
[ ] Next.js detected
[ ] Root directory set to 'frontend'
[ ] NEXT_PUBLIC_API_URL set
[ ] Deployment successful
[ ] Frontend loads without errors
[ ] Frontend URL: ___________________

INTEGRATION
[ ] Frontend and backend connected
[ ] CORS configured correctly
[ ] Full E2E flow tested
[ ] Email/SMS working in production
[ ] Dashboard displays correctly
```

---

## 🎬 AFTER DEPLOYMENT

### 1. Update Your Demo Video
If you already recorded a demo with localhost URLs, update it to show:
- Live frontend URL
- Live backend API
- Full workflow in production

### 2. Test Everything

**Create new account in production:**
```
1. Visit https://careops.vercel.app
2. Register with your email
3. Create workspace
4. Try all features (contacts, bookings, inbox)
5. Verify emails/SMS are sent
6. Check dashboard
```

### 3. Share Live Links

**For hackathon submission, provide:**
```
Frontend: https://careops-xxxxx.vercel.app
Backend API: https://careops-api-xxxxx.onrender.com/docs
Demo Video: [URL to YouTube/Google Drive]
GitHub Repo: https://github.com/YOUR_USERNAME/careops
```

---

## ⚡ QUICK REFERENCE

### Production URLs
```
Frontend:  https://careops.vercel.app
Backend:   https://careops-api-xxxxx.onrender.com
API Docs:  https://careops-api-xxxxx.onrender.com/docs
```

### Environment Variables by Platform

**Vercel (Frontend)**
```
NEXT_PUBLIC_API_URL=https://careops-api-xxxxx.onrender.com
```

**Render (Backend)**
```
DATABASE_URL=postgresql://user:pass@host:5432/careops_db
JWT_SECRET=your-production-secret
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=+1234567890
FRONTEND_URL=https://careops-xxxxx.vercel.app
```

### Helpful Links
```
Render Docs: https://render.com/docs
Vercel Docs: https://vercel.com/docs
Next.js Guide: https://nextjs.org/docs
FastAPI Deployment: https://fastapi.tiangolo.com/deployment/
```

---

## ⏱️ TIMELINE

| Step | Time | Total |
|------|------|-------|
| Push to GitHub | 2 min | 2 min |
| Deploy backend (Render) | 5 min | 7 min |
| Deploy frontend (Vercel) | 5 min | 12 min |
| Configure environments | 3 min | 15 min |
| Test & verify | 10 min | 25 min |
| Record production demo | 15 min | 40 min |

**Total: ~40 minutes to fully deployed + recorded**

---

## 🏆 YOU'RE READY!

Once you complete this guide, you'll have:
✅ Code in GitHub (backed up)
✅ Backend running on Render (live)
✅ Frontend running on Vercel (live)
✅ Both connected and working
✅ Production-ready for submission

**Next step:** Follow PHASE 1 below to get started!
