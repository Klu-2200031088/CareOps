# 🚀 Quick Deployment Reference

**This file has everything you need for deployment at a glance.**

---

## 📋 DEPLOYMENT CHECKLIST

### Before You Start
- [ ] GitHub account created
- [ ] Vercel account created (link GitHub)
- [ ] Render account created (link GitHub)
- [ ] Code committed to GitHub main branch
- [ ] `backend/.env` configured locally
- [ ] `frontend/.env.local` configured locally
- [ ] Backend runs: `python main.py` ✅
- [ ] Frontend runs: `npm run dev` ✅

### Phase 1: Backend (Render) - 10 minutes
- [ ] Go to https://render.com
- [ ] Create Web Service (connect careops repo)
- [ ] Set build command: `pip install -r requirements.txt`
- [ ] Set start command: `gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:10000`
- [ ] Create PostgreSQL database
- [ ] Copy DATABASE_URL from PostgreSQL
- [ ] Add all env vars from backend/.env
- [ ] Deploy → Wait for "Live" status
- [ ] Copy backend URL: `https://careops-api-XXXXX.onrender.com`
- [ ] Test: Visit `https://careops-api-XXXXX.onrender.com/docs` → Shows API docs ✅

### Phase 2: Frontend (Vercel) - 5 minutes
- [ ] Go to https://vercel.com
- [ ] Import careops repository
- [ ] Set root directory: `frontend`
- [ ] Framework: Next.js (auto-detected)
- [ ] Add env var: `NEXT_PUBLIC_API_URL=https://careops-api-XXXXX.onrender.com`
- [ ] Deploy → Wait for completion
- [ ] Copy frontend URL: `https://careops-XXXXX.vercel.app`
- [ ] Test: Visit frontend URL → Shows login page ✅

### Phase 3: Integration - 10 minutes
- [ ] Update Render backend FRONTEND_URL: `https://careops-XXXXX.vercel.app`
- [ ] Trigger Render redeploy (Settings → Deploy)
- [ ] Wait for redeploy to complete
- [ ] Test full E2E flow:
  - [ ] Register new user
  - [ ] Create workspace
  - [ ] Create contact (should send email)
  - [ ] Create booking (should send email/SMS)
  - [ ] View inbox
  - [ ] Check dashboard

### Phase 4: Final Verification - 5 minutes
- [ ] Frontend loads without 404s
- [ ] Can register and login
- [ ] Can create workspace and contacts
- [ ] Dashboard shows correct stats
- [ ] Email/SMS confirmations sent
- [ ] No API errors in browser console
- [ ] No database errors in Render logs

---

## 🔑 ENVIRONMENT VARIABLES AT A GLANCE

### Backend (Render Dashboard → Environment)

```ini
# Database
DATABASE_URL=postgresql://user:pass@db.onrender.com:5432/careops_db

# JWT
JWT_SECRET=change-me-to-random-string

# Email (Gmail)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=16-char-app-password

# SMS (Twilio - optional)
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=+1234567890

# Frontend URL (for CORS)
FRONTEND_URL=https://careops-XXXXX.vercel.app
```

### Frontend (Vercel Dashboard → Settings → Environment)

```ini
NEXT_PUBLIC_API_URL=https://careops-api-XXXXX.onrender.com
```

---

## ⏱️ QUICK TIMELINE

| Task | Time | Cumulative |
|------|------|-----------|
| Setup Render backend | 10 min | 10 min |
| Setup Vercel frontend | 5 min | 15 min |
| Configure integrations | 10 min | 25 min |
| Test end-to-end | 10 min | 35 min |
| **TOTAL** | **35 min** | **35 min** |

---

## 🔗 IMPORTANT LINKS

### Your Accounts
- GitHub: https://github.com/YOUR_USERNAME/careops
- Render Dashboard: https://dashboard.render.com
- Vercel Dashboard: https://vercel.com/dashboard
- Gmail App Passwords: https://myaccount.google.com/apppasswords
- Twilio Console: https://www.twilio.com/console

### Your Deployment URLs (Fill these in)
```
Backend API: https://careops-api-XXXXX.onrender.com
Frontend App: https://careops-XXXXX.vercel.app
API Docs: https://careops-api-XXXXX.onrender.com/docs
```

---

## 🆘 QUICK TROUBLESHOOTING

### Backend won't start
```
Problem: Build fails
→ Check Render logs for error
→ Verify requirements.txt has all packages
→ Try: pip install -r requirements.txt (locally first)

Problem: Runtime crashes
→ Check DATABASE_URL is set
→ Check PostgreSQL is running
→ Check SMTP credentials
```

### Frontend won't load
```
Problem: CORS errors
→ Check FRONTEND_URL is set in Render
→ Redeploy backend after changing env var
→ Check frontend URL has no trailing slash

Problem: API connection refused
→ Check NEXT_PUBLIC_API_URL in Vercel
→ Verify backend is actually running
→ Check backend URL is correct in env var
```

### Email not sending
```
Problem: Gmail says "Invalid credentials"
→ You must use 16-char app password (not regular password)
→ Get from: https://myaccount.google.com/apppasswords
→ Make sure 2FA is enabled on Gmail account

Problem: Email sends but recipient not in To field
→ Check SMTP_USER matches sender
→ Verify contact.email is correct
```

---

## ✨ VERIFICATION COMMANDS

### Test Backend is Running
```bash
# Should return Swagger UI
curl https://careops-api-XXXXX.onrender.com/docs

# Should return API version
curl https://careops-api-XXXXX.onrender.com/
```

### Test Frontend is Running
```bash
# Should return HTML (login page)
curl https://careops-XXXXX.vercel.app
```

### Test Database Connection
```bash
# Via Render dashboard → Database → Connect
# Copy connection string and test locally
psql postgresql://...
```

---

## 📤 SUBMISSION REQUIREMENTS

When submitting to hackathon, you need:

1. **Frontend URL**
   ```
   https://careops-XXXXX.vercel.app
   ```

2. **Backend API URL**
   ```
   https://careops-api-XXXXX.onrender.com
   ```

3. **GitHub Repository**
   ```
   https://github.com/YOUR_USERNAME/careops
   ```

4. **Demo Video** (4-5 minutes)
   - Show automation working
   - Show staff features
   - Show dashboard
   - Upload to YouTube/Google Drive

5. **Brief Description**
   - What your app does
   - Key features implemented
   - Any AI tools used

---

## 🎯 SUCCESS INDICATORS

### Green lights (you're good)
- ✅ Frontend loads without errors
- ✅ Can register and login
- ✅ Can create workspace
- ✅ Contact creation triggers email
- ✅ Booking creation triggers email + SMS
- ✅ Dashboard shows real data
- ✅ Inbox displays conversations
- ✅ No red errors in browser console
- ✅ No 5xx errors in Render logs

### Red flags (something's wrong)
- ❌ 404 errors on frontend load
- ❌ CORS errors in console
- ❌ Cannot login with credentials
- ❌ Dashboard returns 500 error
- ❌ Email not being sent
- ❌ Database connection errors
- ❌ API returning 401 Unauthorized

---

## 📝 NOTES

1. **First deployment takes 2-3 minutes**
   - Vercel: ~1-2 min
   - Render: ~2-3 min (includes building dependencies)

2. **Subsequent deployments are faster** (1-2 min)

3. **Building frontend locally verifies** everything works before pushing to GitHub

4. **Always test locally first** before deploying

5. **Render free tier has limits** but is fine for MVP/demo

6. **Vercel free tier is unlimited** for personal projects

---

## 🏆 YOU'VE GOT THIS!

Follow this checklist and you'll have a live, production-ready app in under 1 hour.

Questions? Check DEPLOYMENT_GUIDE.md for detailed instructions.
