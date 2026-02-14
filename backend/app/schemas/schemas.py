from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# Auth Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone_number: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    phone_number: Optional[str]
    is_phone_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class SMSVerificationRequest(BaseModel):
    code: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Workspace Schemas
class WorkspaceCreate(BaseModel):
    name: str
    address: Optional[str] = None
    timezone: str = "UTC"
    contact_email: EmailStr

class WorkspaceUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    timezone: Optional[str] = None
    contact_email: Optional[EmailStr] = None

class WorkspaceResponse(BaseModel):
    id: int
    name: str
    address: Optional[str]
    timezone: str
    contact_email: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Contact Schemas
class ContactCreate(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None

class ContactResponse(BaseModel):
    id: int
    name: str
    email: Optional[str]
    phone: Optional[str]
    created_at: datetime
    last_contacted: Optional[datetime]
    
    class Config:
        from_attributes = True

# Booking Schemas
class BookingCreate(BaseModel):
    booking_type: str
    scheduled_at: datetime
    duration_minutes: int = 60
    location: Optional[str] = None
    notes: Optional[str] = None

class BookingUpdate(BaseModel):
    status: str  # confirmed, completed, no_show, cancelled
    notes: Optional[str] = None

class BookingResponse(BaseModel):
    id: int
    booking_type: str
    scheduled_at: datetime
    duration_minutes: int
    location: Optional[str]
    status: str
    contact: ContactResponse
    created_at: datetime
    
    class Config:
        from_attributes = True

# Message Schemas
class MessageCreate(BaseModel):
    content: str
    sender_type: str = "staff"
    channel: str = "system"

class MessageResponse(BaseModel):
    id: int
    sender_type: str
    sender_name: str
    content: str
    channel: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Conversation Schemas
class ConversationResponse(BaseModel):
    id: int
    contact: ContactResponse
    is_open: bool
    messages: List[MessageResponse]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Form Schemas
class FormCreate(BaseModel):
    name: str
    description: Optional[str] = None
    required_fields: List[str]

class FormResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    required_fields: List[str]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class FormSubmissionCreate(BaseModel):
    contact_email: str
    data: dict

class FormSubmissionResponse(BaseModel):
    id: int
    status: str
    submitted_at: Optional[datetime]
    due_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# Inventory Schemas
class InventoryItemCreate(BaseModel):
    name: str
    quantity: int
    quantity_per_booking: int = 1
    low_threshold: int = 5

class InventoryItemResponse(BaseModel):
    id: int
    name: str
    quantity: int
    low_threshold: int
    quantity_per_booking: int
    
    class Config:
        from_attributes = True

# Dashboard Schemas
class DashboardStats(BaseModel):
    today_bookings: int
    upcoming_bookings: int
    new_inquiries: int
    pending_forms: int
    low_inventory_count: int
    total_revenue: float = 0

class DashboardResponse(BaseModel):
    stats: DashboardStats
    alerts: List[dict]
    recent_bookings: List[BookingResponse]
    recent_conversations: List[ConversationResponse]
