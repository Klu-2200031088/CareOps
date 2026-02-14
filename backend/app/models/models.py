from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Float, Enum, JSON
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import enum

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    phone_number = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_phone_verified = Column(Boolean, default=False)
    verification_code = Column(String, nullable=True)
    verification_code_expires = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    workspaces = relationship("Workspace", back_populates="owner")
    staff_roles = relationship("StaffUser", back_populates="user")

class Workspace(Base):
    __tablename__ = "workspaces"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    address = Column(String)
    timezone = Column(String, default="UTC")
    contact_email = Column(String)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="workspaces")
    contacts = relationship("Contact", back_populates="workspace", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="workspace", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="workspace", cascade="all, delete-orphan")
    forms = relationship("Form", back_populates="workspace", cascade="all, delete-orphan")
    inventory_items = relationship("InventoryItem", back_populates="workspace", cascade="all, delete-orphan")
    staff_users = relationship("StaffUser", back_populates="workspace", cascade="all, delete-orphan")
    integrations = relationship("Integration", back_populates="workspace", cascade="all, delete-orphan")

class Contact(Base):
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"))
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_contacted = Column(DateTime)
    
    workspace = relationship("Workspace", back_populates="contacts")
    conversations = relationship("Conversation", back_populates="contact", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="contact")

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"))
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    is_open = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    workspace = relationship("Workspace", back_populates="conversations")
    contact = relationship("Contact", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    sender_type = Column(String)  # "customer", "system", "staff"
    sender_name = Column(String)
    content = Column(Text)
    channel = Column(String)  # "email", "sms", "system"
    created_at = Column(DateTime, default=datetime.utcnow)
    
    conversation = relationship("Conversation", back_populates="messages")

class BookingTypeEnum(str, enum.Enum):
    CONSULTATION = "consultation"
    MEETING = "meeting"
    SERVICE = "service"

class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"))
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    booking_type = Column(String)  # consultation, meeting, service
    scheduled_at = Column(DateTime)
    duration_minutes = Column(Integer, default=60)
    location = Column(String)
    status = Column(String, default="confirmed")  # confirmed, completed, no_show, cancelled
    notes = Column(Text)
    forms_sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    workspace = relationship("Workspace", back_populates="bookings")
    contact = relationship("Contact", back_populates="bookings")

class Form(Base):
    __tablename__ = "forms"
    
    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"))
    name = Column(String)
    description = Column(Text)
    required_fields = Column(JSON)  # List of field names
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    workspace = relationship("Workspace", back_populates="forms")
    submissions = relationship("FormSubmission", back_populates="form", cascade="all, delete-orphan")

class FormSubmission(Base):
    __tablename__ = "form_submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    form_id = Column(Integer, ForeignKey("forms.id"))
    booking_id = Column(Integer)
    contact_email = Column(String)
    data = Column(JSON)
    submitted_at = Column(DateTime)
    status = Column(String, default="pending")  # pending, completed, overdue
    due_at = Column(DateTime)
    
    form = relationship("Form", back_populates="submissions")

class InventoryItem(Base):
    __tablename__ = "inventory_items"
    
    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"))
    name = Column(String)
    quantity = Column(Integer)
    quantity_per_booking = Column(Integer, default=1)
    low_threshold = Column(Integer, default=5)
    last_restocked = Column(DateTime)
    
    workspace = relationship("Workspace", back_populates="inventory_items")

class StaffUser(Base):
    __tablename__ = "staff_users"
    
    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String, default="staff")  # staff, manager
    can_manage_inbox = Column(Boolean, default=True)
    can_manage_bookings = Column(Boolean, default=True)
    can_view_inventory = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    workspace = relationship("Workspace", back_populates="staff_users")
    user = relationship("User", back_populates="staff_roles")

class Integration(Base):
    __tablename__ = "integrations"
    
    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"))
    provider = Column(String)  # "gmail", "twilio", "calendar"
    is_connected = Column(Boolean, default=False)
    config = Column(JSON)  # Encrypted credentials
    created_at = Column(DateTime, default=datetime.utcnow)
    
    workspace = relationship("Workspace", back_populates="integrations")
