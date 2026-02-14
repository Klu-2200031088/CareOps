# CareOps - Production Deployment Guide

## 🚀 Deploy to Production in 15 minutes

### Option A: Vercel (Frontend) + Render (Backend)

---

## ✅ Prerequisites

1. GitHub account (for code hosting)
2. Vercel account (free tier)
3. Render account (free tier with email confirmation)
4. PostgreSQL database (Render or ElephantSQL)
5. SMTP credentials (Gmail, SendGrid, etc.)

---

## 📦 Step 1: Prepare Code

### 1.1 Create GitHub Repository

```bash
cd d:\development\careops
git init
git add .
git commit -m "Initial CareOps commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/careops.git
git push -u origin main
```

### 1.2 Update Backend Requirements
```bash
cd backend
pip freeze > requirements.txt
cd ..
```

### 1.3 Add Production Config Files

**backend/gunicorn_config.py**
```python
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
bind = "0.0.0.0:8000"
timeout = 60
```

---

## 🎯 Step 2: Deploy Backend to Render

### 2.1 Create Render Service

1. Go to https://render.com
2. Sign up / Log in
3. Click "New +" → "Web Service"
4. Connect GitHub repository
5. Fill in:
   - **Name:** `careops-api`
   - **Region:** Choose closest
   - **Branch:** `main`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port 8000`

### 2.2 Add Environment Variables

Click "Environment" and add:

```
DATABASE_URL=postgresql://user:password@host:5432/careops
SECRET_KEY=your-production-secret-key-here
FRONTEND_URL=https://careops.vercel.app
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_PHONE_NUMBER=+1234567890
```

### 2.3 Add PostgreSQL Database

1. In Render dashboard: "New +" → "PostgreSQL"
2. Fill in:
   - **Name:** `careops-db`
   - **Database:** `careops`
   - **User:** `careops`
   - **Region:** Same as API
3. Copy connection string → use as DATABASE_URL above

### 2.4 Deploy

Click "Create Web Service" and wait 5-10 minutes.

✅ Your backend is now live at `https://careops-api.onrender.com`

---

## 🎨 Step 3: Deploy Frontend to Vercel

### 3.1 Create Vercel Project

1. Go to https://vercel.com
2. Sign up / Log in
3. Click "Add New..." → "Project"
4. Select GitHub repository
5. In **Project Settings**:
   - **Framework:** Next.js
   - **Root Directory:** `./frontend`

### 3.2 Add Environment Variables

In project settings, add:

```
NEXT_PUBLIC_API_URL=https://careops-api.onrender.com/api
```

### 3.3 Deploy

Click "Deploy" and wait 2-3 minutes.

✅ Your frontend is now live at `https://careops.vercel.app`

---

## 📧 Step 4: Configure Email (Gmail)

### 4.1 Enable Gmail App Password

1. Go to https://myaccount.google.com/security
2. Enable 2-Step Verification
3. Create "App Password" for "Mail" and "Windows"
4. Copy the generated 16-character password
5. Use in `SMTP_PASSWORD` environment variable

### 4.2 Test Email

```bash
# SSH into Render backend
render ssh careops-api

# Test email
python -c "
from app.integrations.email_service import email_service
result = email_service.send_email('test@example.com', 'Test', 'Hello World!')
print(result)
"
```

---

## 📱 Step 5: Configure SMS (Twilio) - Optional

### 5.1 Create Twilio Account

1. Go to https://www.twilio.com/
2. Sign up for free trial
3. Get:
   - Account SID
   - Auth Token
   - Phone number

### 5.2 Add to Environment Variables

```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your-token-here
TWILIO_PHONE_NUMBER=+1234567890
```

---

## 🔍 Step 6: Verify Deployment

### 6.1 Test Backend API

```bash
curl https://careops-api.onrender.com/health
# Should return: {"status": "healthy"}
```

### 6.2 Test Frontend

Visit `https://careops.vercel.app`
- Should see login page
- Try registering new account
- Create workspace
- Check dashboard

### 6.3 Monitor Logs

**Render:**
```
Dashboard → careops-api → Logs
```

**Vercel:**
```
Dashboard → careops → Deployments → Logs
```

---

## 🔐 Security Checklist

- [ ] Change `SECRET_KEY` to random 32-character string
- [ ] Use strong database password
- [ ] Enable HTTPS (automatic on Vercel/Render)
- [ ] Set `FRONTEND_URL` to production domain
- [ ] Use environment variables for all secrets
- [ ] Disable debug mode (`DEBUG=False`)
- [ ] Setup CORS for frontend domain only
- [ ] Rotate API keys monthly

---

## 📊 Production Architecture

```
User (Browser)
    ↓ (HTTPS)
    Vercel (Frontend)
    ↓ (HTTPS API calls)
    Render (Backend)
    ↓
    PostgreSQL (Render)
    
    +
    
Email Service (SMTP)
SMS Service (Twilio)
```

---

## ⚙️ Additional Configurations

### Add Custom Domain to Vercel

1. Go to Project Settings → Domains
2. Add your domain (e.g., app.careops.com)
3. Update DNS records as instructed
4. Wait for SSL certificate

### Add Custom Domain to Render

1. Go to Web Service Settings → Custom Domains
2. Add domain
3. Update DNS CNAME record

### Setup CI/CD Pipeline

Both Vercel and Render auto-deploy on `git push main`

### Monitor Performance

**Vercel Analytics:**
```
Dashboard → careops → Analytics
```

**Render Metrics:**
```
Dashboard → careops-api → Metrics
```

---

## 🆘 Troubleshooting Deployment

### Frontend shows "API unreachable"
- Check `NEXT_PUBLIC_API_URL` environment variable
- Verify backend is running on Render
- Check CORS settings in `main.py`
- Ensure firewall allows requests

### Backend returns 502 error
- Check Render logs for errors
- Verify DATABASE_URL is correct
- Ensure all required env vars are set
- Restart web service

### Database connection timeout
- Check PostgreSQL is running
- Verify DATABASE_URL syntax
- Check IP whitelist on database
- Test connection string locally

### Email not sending
- Verify SMTP credentials
- Check Gmail 2FA and app password
- Ensure firewall allows SMTP
- Check Render logs for errors

---

## 💾 Backup & Recovery

### Backup PostgreSQL

```bash
# Using Render backup feature:
# Dashboard → careops-db → Backups
```

### Manual Backup

```bash
pg_dump -U careops -h host -d careops > backup.sql
```

### Restore

```bash
psql -U careops -h host -d careops < backup.sql
```

---

## 💰 Cost Estimation

| Service | Free Tier | Paid (if needed) |
|---------|-----------|-----------------|
| Vercel | Yes | $20/mo |
| Render | Free tier (limited) | $7/mo for always-on |
| PostgreSQL | $15/mo | $50+/mo |
| Email (Gmail) | Free | $6/mo for SendGrid |
| SMS (Twilio) | $1/mo credit | Pay as you go |
| **Total** | **$15/mo** | **$80+/mo** |

---

## 🚀 Performance Tips

1. **Enable Caching:** Render auto-caches static assets
2. **Database Query Optimization:** Add indexes
3. **Frontend Code Splitting:** Next.js does automatically
4. **API Rate Limiting:** Add in production
5. **CDN:** Both Vercel and Render use CDN

---

## 📈 Scaling to Production

As your user base grows:

1. **Database:** Upgrade PostgreSQL plan
2. **Backend:** Increase Render plan
3. **Frontend:** Vercel handles auto-scaling
4. **Cache:** Add Redis for sessions
5. **Storage:** Add S3 for file uploads

---

## 📞 Support Links

- Vercel Docs: https://vercel.com/docs
- Render Docs: https://render.com/docs
- PostgreSQL: https://www.postgresql.org/docs/
- FastAPI: https://fastapi.tiangolo.com/
- Next.js: https://nextjs.org/docs

---

## ✨ Post-Deployment

1. ✅ Share deployment link with team
2. ✅ Update README with production URL
3. ✅ Setup monitoring/alerts
4. ✅ Create incident response plan
5. ✅ Document deployment process
6. ✅ Setup automated backups
7. ✅ Monitor usage and costs

---

**Deployed with ❤️ - CareOps is now live! 🎉**

Production URL: `https://careops.vercel.app`
API URL: `https://careops-api.onrender.com`
