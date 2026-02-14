# CareOps - Unified Operations Platform

## 🎯 Project Overview

CareOps is a unified operations platform for service-based businesses. One platform to manage:
- ✅ Customer inquiries and leads
- ✅ Bookings and appointments
- ✅ Email & SMS communication
- ✅ Forms and document management
- ✅ Inventory tracking
- ✅ Business dashboard

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL 13+ (or SQLite for development)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` file:
```
DATABASE_URL=sqlite:///./careops.db
SECRET_KEY=your-secret-key-change-in-production
FRONTEND_URL=http://localhost:3000
```

Run backend:
```bash
python main.py
```

API will be available at `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at `http://localhost:3000`

## 📊 Architecture

```
CareOps/
├── backend/          # FastAPI server
│   ├── app/
│   │   ├── models/   # Database models
│   │   ├── routes/   # API endpoints
│   │   ├── schemas/  # Pydantic schemas
│   │   ├── services/ # Business logic
│   │   └── integrations/ # Email, SMS, etc.
│   └── main.py       # Entry point
│
└── frontend/         # Next.js app
    ├── src/
    │   ├── app/      # Pages
    │   ├── components/ # React components
    │   └── services/ # API client & store
    └── package.json
```

## 🔌 Integrations

- ✅ **Email**: Gmail SMTP
- ⏳ **SMS**: Twilio (configured, not implemented)
- ⏳ **Calendar**: Google Calendar (planned)

## 📝 API Endpoints

### Auth
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login

### Workspace
- `POST /api/workspace/create` - Create workspace
- `GET /api/workspace/list` - List user workspaces
- `POST /api/workspace/{id}/activate` - Activate workspace

### Contacts
- `POST /api/contacts/{workspace_id}/create` - Add contact
- `GET /api/contacts/{workspace_id}/list` - List contacts

### Bookings
- `POST /api/bookings/{workspace_id}/{contact_id}/create` - Create booking
- `GET /api/bookings/{workspace_id}/list` - List bookings
- `PATCH /api/bookings/{workspace_id}/{booking_id}` - Update booking

### Inbox
- `GET /api/inbox/{workspace_id}/conversations` - Get conversations
- `POST /api/inbox/{workspace_id}/conversations/{id}/send` - Send message

### Dashboard
- `GET /api/dashboard/{workspace_id}` - Get dashboard data

## 🧪 Test User Flow

1. Register: `register@example.com` / `password123`
2. Create workspace: "My Business"
3. Add booking types: "Consultation" (60 min), "Meeting" (30 min)
4. Add test contacts
5. Activate workspace
6. View dashboard

## 🔐 Security Notes

- Change `SECRET_KEY` in production
- Use environment variables for all credentials
- Enable HTTPS in production
- Implement rate limiting

## 📦 Database Schema

### Core Tables
- `users` - User accounts
- `workspaces` - Business workspaces
- `contacts` - Customer contacts
- `bookings` - Appointments/bookings
- `conversations` - Customer communication threads
- `messages` - Individual messages
- `forms` - Form templates
- `form_submissions` - Submitted form data
- `inventory_items` - Tracked inventory
- `staff_users` - Workspace staff members
- `integrations` - Connected services

## 🚢 Deployment

### Backend (Vercel/Render)
```bash
cd backend
pip install -r requirements.txt
```

### Frontend (Vercel)
```bash
cd frontend
npm run build
```

## 📞 Support

For issues or questions:
1. Check the API docs at `http://localhost:8000/docs`
2. Review database logs
3. Check browser console for frontend errors

## 🎉 Key Features Implemented

✅ User authentication (JWT)
✅ Workspace creation & management
✅ Contact management
✅ Booking system
✅ Conversation/Inbox
✅ Dashboard with real-time stats
✅ Inventory tracking
✅ Email integration ready
✅ Responsive UI

## ⏳ Features To Do

- [ ] Complete SMS integration (Twilio)
- [ ] Calendar sync (Google Calendar)
- [ ] Form builder & submission tracking
- [ ] Advanced reporting
- [ ] Staff permissions system
- [ ] Automated reminders
- [ ] File uploads/storage

---

Built with ❤️ for the CareOps Hackathon
