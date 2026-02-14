# CareOps - Architecture & Component Guide

## 🏗️ Project Structure

```
careops/
├── backend/                    # FastAPI server
│   ├── app/
│   │   ├── models/            # SQLAlchemy ORM models
│   │   │   └── models.py      # 11 database tables
│   │   ├── routes/            # API endpoints
│   │   │   ├── auth.py        # JWT auth
│   │   │   ├── workspace.py   # Workspace CRUD
│   │   │   ├── contacts.py    # Contact management
│   │   │   ├── bookings.py    # Booking system
│   │   │   ├── inbox.py       # Messaging
│   │   │   ├── dashboard.py   # Analytics
│   │   │   ├── forms.py       # Form management
│   │   │   └── inventory.py   # Inventory tracking
│   │   ├── schemas/           # Pydantic validators
│   │   │   └── schemas.py     # Request/response models
│   │   ├── services/          # Business logic
│   │   │   └── auth_service.py # JWT & password hashing
│   │   ├── integrations/      # External services
│   │   │   └── email_service.py # Email via SMTP
│   │   └── database.py        # SQLAlchemy config
│   ├── main.py               # FastAPI app entry
│   ├── requirements.txt       # Dependencies
│   ├── .env                   # Configuration
│   └── Dockerfile
│
├── frontend/                  # Next.js app
│   ├── src/
│   │   ├── app/              # Next.js pages
│   │   │   ├── page.tsx      # Home
│   │   │   ├── login/        # Authentication
│   │   │   ├── register/
│   │   │   ├── workspaces/   # Workspace selection
│   │   │   ├── workspace-setup/ # Setup wizard
│   │   │   ├── dashboard/    # Main dashboard
│   │   │   ├── inbox/        # Messaging UI
│   │   │   ├── book/         # Public booking page
│   │   │   ├── layout.tsx
│   │   │   └── globals.css
│   │   ├── services/
│   │   │   ├── api.ts        # Axios API client
│   │   │   └── store.ts      # Zustand state
│   │   └── components/       # Reusable components (future)
│   ├── public/               # Static files
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── next.config.js
│   └── .env.local
│
├── docker-compose.yml        # Multi-container setup
├── setup.bat                 # Windows setup
├── setup.sh                  # Unix setup
├── README.md                 # Main documentation
├── QUICKSTART.md             # Quick reference
└── ARCHITECTURE.md           # This file
```

---

## 📊 Database Schema

### User Management
```
users
├── id (PK)
├── email (UNIQUE)
├── hashed_password
├── full_name
└── created_at

workspaces
├── id (PK)
├── name
├── owner_id (FK → users)
├── address
├── timezone
├── contact_email
├── is_active
└── created_at
```

### Customer Management
```
contacts
├── id (PK)
├── workspace_id (FK)
├── name
├── email
├── phone
├── last_contacted
└── created_at

conversations
├── id (PK)
├── workspace_id (FK)
├── contact_id (FK)
├── is_open
├── created_at
└── updated_at

messages
├── id (PK)
├── conversation_id (FK)
├── sender_type (customer|staff|system)
├── sender_name
├── content
├── channel (email|sms|system)
└── created_at
```

### Booking System
```
bookings
├── id (PK)
├── workspace_id (FK)
├── contact_id (FK)
├── booking_type
├── scheduled_at
├── duration_minutes
├── location
├── status (confirmed|completed|no_show|cancelled)
├── forms_sent
└── created_at
```

### Forms & Documents
```
forms
├── id (PK)
├── workspace_id (FK)
├── name
├── description
├── required_fields (JSON)
├── is_active
└── created_at

form_submissions
├── id (PK)
├── form_id (FK)
├── booking_id
├── contact_email
├── data (JSON)
├── submitted_at
├── status (pending|completed|overdue)
├── due_at
└── created_at
```

### Inventory & Resources
```
inventory_items
├── id (PK)
├── workspace_id (FK)
├── name
├── quantity
├── quantity_per_booking
├── low_threshold
└── last_restocked
```

### Staff & Permissions
```
staff_users
├── id (PK)
├── workspace_id (FK)
├── user_id (FK)
├── role (staff|manager)
├── can_manage_inbox (BOOL)
├── can_manage_bookings (BOOL)
├── can_view_inventory (BOOL)
└── created_at
```

### Integrations
```
integrations
├── id (PK)
├── workspace_id (FK)
├── provider (gmail|twilio|calendar)
├── is_connected (BOOL)
├── config (JSON - encrypted)
└── created_at
```

---

## 🔐 Authentication Flow

```
User Login
↓
POST /api/auth/login (email, password)
↓
Verify password (bcrypt)
↓
Generate JWT token (HS256)
↓
Return {access_token, token_type}
↓
Store in localStorage (frontend)
↓
Include in Authorization header for future requests
```

**Token Structure:**
```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "exp": 1702500000,
  "iat": 1702498800
}
```

---

## 🌊 API Request Flow

```
Frontend (React)
↓
axios API client
↓ (HTTP + JWT)
FastAPI Router
↓
Dependency injection (get_db, token validation)
↓
Business logic (services)
↓
Database queries (SQLAlchemy)
↓
PostgreSQL/SQLite
↓
Response (JSON/Pydantic)
↓
Frontend state update (Zustand)
```

---

## 🔄 Workspace Setup Flow

```
1. User Registration
   └─→ Create User account

2. Create Workspace
   └─→ Create Workspace record
   └─→ Set owner

3. Setup Wizard (Step-by-step)
   └─→ Add booking types
   └─→ Add test contacts
   └─→ Configure integrations
   └─→ Review settings

4. Activation
   └─→ Verify prerequisites met
   └─→ Set is_active = true
   └─→ Public URLs become available

5. Operations
   └─→ Receive bookings
   └─→ Manage inbox
   └─→ Track inventory
   └─→ View dashboard
```

---

## 💬 Messaging System

```
Contact submits form
↓
System creates Contact + Conversation
↓
Auto-send welcome message (system channel)
↓
Staff member reads inbox
↓
Staff replies via UI
↓
Message stored (sender_type = "staff")
↓
Email sent to contact (via integration)
↓
Customer can reply via email
↓
Reply parsed and added to conversation
```

---

## 📈 Dashboard Data Aggregation

```
GET /api/dashboard/{workspace_id}
↓
Fetch from database:
├─ COUNT bookings (today) → today_bookings
├─ COUNT bookings (future) → upcoming_bookings
├─ COUNT conversations (open) → new_inquiries
├─ COUNT form_submissions (pending) → pending_forms
├─ COUNT inventory (low stock) → low_inventory_count
│
├─ Query bookings (last 5) → recent_bookings
├─ Query conversations (last 5) → recent_conversations
│
├─ Generate alerts:
│   ├─ If today_bookings == 0 → "No bookings today"
│   ├─ If pending_forms > 0 → "X forms pending"
│   └─ If low_inventory > 0 → "X items low stock"
│
└─ Return aggregated DashboardResponse
```

---

## 🧬 State Management (Zustand)

### AuthStore
```typescript
{
  token: string | null
  user: User | null
  setAuth(token, user): void
  logout(): void
}
```

### WorkspaceStore
```typescript
{
  currentWorkspace: Workspace | null
  setWorkspace(workspace): void
}
```

**Usage in Components:**
```typescript
const { token } = useAuthStore();
const { currentWorkspace } = useWorkspaceStore();
```

---

## 🚀 Deployment Architecture

### Development
```
localhost:3000 (Frontend)
↕ (API calls)
localhost:8000 (Backend)
↕
SQLite (careops.db)
```

### Production (Docker)
```
Docker Network
├─ Frontend Container (Node 18)
│  └─ Next.js on port 3000
├─ Backend Container (Python 3.11)
│  └─ FastAPI on port 8000
└─ PostgreSQL Container
   └─ Port 5432
```

### Production (Cloud)
```
Vercel (Frontend)
↕ (HTTPS)
Render/Heroku (Backend)
↕
AWS RDS PostgreSQL
```

---

## 🔌 Integration Points

### Email Service
```
app/integrations/email_service.py
├─ send_email(to, subject, body)
├─ send_booking_confirmation()
├─ send_welcome_message()
└─ send_form_reminder()
```

**Flow:**
```
Event triggers (new booking, new contact)
↓
EmailService method called
↓
SMTP connection to Gmail/provider
↓
Email sent
↓
Logged in system
```

### SMS Service (Planned)
```
- Twilio integration
- Booking reminders
- Form reminders
- Alert notifications
```

### Calendar Integration (Planned)
```
- Google Calendar sync
- Booking conflicts
- Availability sync
```

---

## 🛡️ Security Considerations

1. **Password Hashing:** bcrypt (passlib)
2. **JWT Tokens:** HS256 algorithm, 30-min expiry
3. **Database:** Parameterized queries (SQLAlchemy)
4. **CORS:** Configured for frontend domain
5. **Input Validation:** Pydantic schemas
6. **Environment Variables:** Sensitive data in .env
7. **HTTPS:** Required in production

---

## ⚡ Performance Optimizations

1. **Database Indexing:** Foreign keys auto-indexed
2. **API Response Pagination:** Implement in future
3. **Caching:** Consider Redis for sessions
4. **Query Optimization:** Select only needed fields
5. **Frontend:** Next.js image optimization, code splitting

---

## 📋 API Response Format

### Success (2xx)
```json
{
  "id": 1,
  "name": "Consultation",
  "duration_minutes": 60,
  "created_at": "2024-02-14T10:30:00"
}
```

### Error (4xx/5xx)
```json
{
  "detail": "Error message describing what went wrong"
}
```

### List Response
```json
[
  { "id": 1, "name": "Item 1" },
  { "id": 2, "name": "Item 2" }
]
```

---

## 🔄 Data Flow Examples

### Create Booking
```
Frontend form → POST /api/bookings/{ws}/{contact}/create
↓
Routes: bookings.py receives request
↓
Validates token & workspace access
↓
Creates Booking record
↓
Updates inventory (qty - qty_per_booking)
↓
Returns BookingResponse
↓
Frontend updates state & shows confirmation
↓
Email sent to contact (via integration)
```

### Send Message
```
Frontend chat UI → POST /api/inbox/{ws}/conversations/{id}/send
↓
Routes: inbox.py validates access
↓
Creates Message record
↓
Updates conversation.updated_at
↓
Returns message status
↓
Frontend adds message to UI
↓
(Future) Email/SMS forwarded to customer
```

---

## 📚 Code Examples

### Creating a Custom Endpoint
```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

@router.get("/example")
def get_example(db: Session = Depends(get_db)):
    # Your logic here
    return {"data": "example"}
```

### Using API Client
```typescript
import { api } from '@/services/api';

const response = await api.get('/bookings/1/list', {
  headers: { Authorization: `Bearer ${token}` }
});
```

### Accessing State
```typescript
import { useAuthStore } from '@/services/store';

export function MyComponent() {
  const { token, logout } = useAuthStore();
  
  return <button onClick={logout}>Logout</button>;
}
```

---

## 🧪 Testing Endpoints

### Using cURL
```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"pass123","full_name":"Test"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -d "email=test@example.com&password=pass123"

# List workspaces
curl http://localhost:8000/api/workspace/list \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 📞 Troubleshooting Architecture

| Issue | Likely Cause | Solution |
|-------|--------------|----------|
| API 401 errors | Token expired | Refresh token or re-login |
| CORS errors | Frontend domain not allowed | Check CORS config in main.py |
| Database locked | Concurrent access | Ensure single SQLite writer |
| No emails sent | Integration not configured | Set SMTP credentials in .env |
| Slow queries | Missing indexes | Check database indexes |

---

Built with precision for CareOps Hackathon 🎯
