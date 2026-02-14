from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Contact, Workspace, Conversation, Message
from app.schemas.schemas import ContactCreate, ContactResponse
from datetime import datetime
from app.integrations.email_service import email_service
from app.integrations.sms_service import sms_service

router = APIRouter()

def get_current_user_id(token: str = None) -> int:
    from app.services.auth_service import decode_token
    if not token:
        raise HTTPException(status_code=401, detail="No token provided")
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return int(payload["sub"])

@router.post("/{workspace_id}/create", response_model=ContactResponse)
def create_contact(workspace_id: int, contact: ContactCreate, token: str, db: Session = Depends(get_db)):
    user_id = get_current_user_id(token)
    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id,
        Workspace.owner_id == user_id
    ).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    db_contact = Contact(
        workspace_id=workspace_id,
        name=contact.name,
        email=contact.email,
        phone=contact.phone,
        last_contacted=datetime.utcnow()
    )
    db.add(db_contact)
    db.commit()
    
    # Create conversation
    db_conversation = Conversation(
        workspace_id=workspace_id,
        contact_id=db_contact.id
    )
    db.add(db_conversation)
    
    # Send welcome message (system)
    welcome_msg = Message(
        conversation_id=db_conversation.id,
        sender_type="system",
        sender_name="CareOps",
        content=f"Welcome {contact.name}! We've received your inquiry and will get back to you shortly.",
        channel="system"
    )
    db.add(welcome_msg)
    db.commit()
    db.refresh(db_contact)
    
    # Send welcome email
    try:
        email_service.send_welcome_message(contact.email, contact.name)
    except Exception as e:
        print(f"Welcome email failed: {e}")
    
    # Send welcome SMS if phone provided
    if contact.phone:
        try:
            sms_msg = f"👋 Hi {contact.name}! Thank you for reaching out. Our team will contact you within 24 hours."
            sms_service.send_sms(contact.phone, sms_msg)
        except Exception as e:
            print(f"Welcome SMS failed: {e}")
    
    return db_contact

@router.get("/{workspace_id}/list", response_model=list[ContactResponse])
def list_contacts(workspace_id: int, token: str, db: Session = Depends(get_db)):
    user_id = get_current_user_id(token)
    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id,
        Workspace.owner_id == user_id
    ).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    contacts = db.query(Contact).filter(Contact.workspace_id == workspace_id).all()
    return contacts

@router.get("/{workspace_id}/{contact_id}", response_model=ContactResponse)
def get_contact(workspace_id: int, contact_id: int, token: str, db: Session = Depends(get_db)):
    user_id = get_current_user_id(token)
    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id,
        Workspace.owner_id == user_id
    ).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    contact = db.query(Contact).filter(
        Contact.id == contact_id,
        Contact.workspace_id == workspace_id
    ).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    return contact
