# CareOps - Quick Start Guide

## ⚡ 5-Minute Setup

### Windows
```bash
cd d:\development\careops
setup.bat
```

### Mac/Linux
```bash
cd /path/to/careops
chmod +x setup.sh
./setup.sh
```

---

## 🚀 Start Development Servers

### Terminal 1: Backend
```bash
cd backend
python main.py
```
✅ Backend running at `http://localhost:8000`
📖 API docs at `http://localhost:8000/docs`

### Terminal 2: Frontend
```bash
cd frontend
npm run dev
```
✅ Frontend running at `http://localhost:3000`

---

## 📝 Test User Flow

### 1. Register
- Email: `test@example.com`
- Password: `password123`
- Full Name: `Test User`

### 2. Create Workspace
- Name: `My Business`
- Address: `123 Main St`
- Timezone: `UTC`
- Contact Email: `business@example.com`

### 3. Setup Workspace
- Add Booking Type: "Consultation" (60 min)
- Add Contact: "John Doe" (john@example.com)
- Activate Workspace

### 4. View Dashboard
- See today's bookings, pending forms, inventory
- Click on alerts to navigate to detailed views

### 5. Test Inbox
- Go to Inbox page
- Select a conversation
- Send a test message

### 6. Public Booking
- Visit: `http://localhost:3000/book?workspace=1`
- Fill in contact details
- Select booking type and date
- Confirm booking

---

## 🗄️ Database Tables

```sql
-- Users & Auth
users (id, email, hashed_password, full_name, created_at)

-- Workspace & Staff
workspaces (id, name, owner_id, address, timezone, is_active)
staff_users (id, workspace_id, user_id, role, permissions)

-- Customers
contacts (id, workspace_id, name, email, phone, created_at)
conversations (id, workspace_id, contact_id, is_open, created_at)
messages (id, conversation_id, sender_type, content, channel, created_at)

-- Bookings
bookings (id, workspace_id, contact_id, booking_type, scheduled_at, status)

-- Forms
forms (id, workspace_id, name, required_fields)
form_submissions (id, form_id, booking_id, data, status, due_at)

-- Inventory
inventory_items (id, workspace_id, name, quantity, low_threshold)

-- Integrations
integrations (id, workspace_id, provider, is_connected, config)
```

---

## 🔌 API Quick Reference

### Authentication
```
POST /api/auth/register
POST /api/auth/login
GET /api/auth/me
```

### Workspace
```
POST /api/workspace/create
GET /api/workspace/list
GET /api/workspace/{id}
POST /api/workspace/{id}/activate
```

### Contacts & Bookings
```
POST /api/contacts/{workspace_id}/create
GET /api/contacts/{workspace_id}/list

POST /api/bookings/{workspace_id}/{contact_id}/create
GET /api/bookings/{workspace_id}/list
PATCH /api/bookings/{workspace_id}/{booking_id}
```

### Inbox
```
GET /api/inbox/{workspace_id}/conversations
GET /api/inbox/{workspace_id}/conversations/{id}
POST /api/inbox/{workspace_id}/conversations/{id}/send
```

### Dashboard
```
GET /api/dashboard/{workspace_id}
```

---

## 📦 Key Technologies

| Component | Tech | Version |
|-----------|------|---------|
| Backend | FastAPI | 0.104.1 |
| Database | SQLAlchemy | 2.0.23 |
| Frontend | Next.js | 14.0 |
| State | Zustand | 4.4 |
| Styling | Tailwind CSS | 3.3 |
| API Client | Axios | 1.6 |

---

## 🐳 Docker Deployment

### Build & Run with Docker Compose
```bash
docker-compose up --build
```

This will start:
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`
- PostgreSQL: `localhost:5432`

---

## ☁️ Production Deployment

### Backend (Render/Heroku)
```bash
# Ensure requirements.txt is up to date
pip freeze > backend/requirements.txt

# Deploy
git push heroku main
```

### Frontend (Vercel)
```bash
vercel deploy --prod
```

---

## 🧪 Testing Checklist

- [ ] Register new user
- [ ] Create workspace
- [ ] Add booking types
- [ ] Create contacts
- [ ] Activate workspace
- [ ] View dashboard
- [ ] Send inbox message
- [ ] Test public booking page
- [ ] Email notifications (if configured)

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Clear database and restart
rm careops.db
python main.py
```

### Frontend API not connecting
- Check NEXT_PUBLIC_API_URL in `.env.local`
- Ensure backend is running on port 8000
- Check browser console for CORS errors

### Database connection error
- For SQLite (default): Ensure write permissions
- For PostgreSQL: Check DATABASE_URL in `.env`

---

## 📞 Support Resources

- FastAPI Docs: `http://localhost:8000/docs`
- Next.js Docs: https://nextjs.org/docs
- SQLAlchemy Docs: https://docs.sqlalchemy.org
- Tailwind Docs: https://tailwindcss.com/docs

---

## 🎉 Next Steps

1. ✅ Complete basic features
2. 🔄 Add SMS integration (Twilio)
3. 📅 Implement calendar sync
4. 📊 Build advanced reports
5. 🔐 Enhance permissions system
6. 📧 Email template system
7. 📱 Mobile app

---

Built with ❤️ for CareOps Hackathon
