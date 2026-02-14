from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Booking, Workspace, Contact, InventoryItem, Message, Conversation
from app.schemas.schemas import BookingCreate, BookingResponse, BookingUpdate
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

@router.post("/{workspace_id}/{contact_id}/create", response_model=BookingResponse)
def create_booking(workspace_id: int, contact_id: int, booking: BookingCreate, token: str, db: Session = Depends(get_db)):
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
    
    db_booking = Booking(
        workspace_id=workspace_id,
        contact_id=contact_id,
        booking_type=booking.booking_type,
        scheduled_at=booking.scheduled_at,
        duration_minutes=booking.duration_minutes,
        location=booking.location,
        notes=booking.notes,
        status="confirmed"
    )
    db.add(db_booking)
    
    # Update inventory if applicable
    inventory_items = db.query(InventoryItem).filter(InventoryItem.workspace_id == workspace_id).all()
    for item in inventory_items:
        item.quantity -= item.quantity_per_booking
    
    db.commit()
    db.refresh(db_booking)
    
    # Send booking confirmation email
    try:
        booking_details = {
            'booking_type': db_booking.booking_type,
            'scheduled_at': db_booking.scheduled_at.strftime('%B %d, %Y at %I:%M %p'),
            'duration_minutes': db_booking.duration_minutes,
            'location': db_booking.location or 'Online'
        }
        email_service.send_booking_confirmation(contact.email, booking_details)
    except Exception as e:
        print(f"Email confirmation failed: {e}")
    
    # Send SMS confirmation if phone available
    if contact.phone:
        try:
            sms_service.send_booking_confirmation(contact.phone, booking_details)
        except Exception as e:
            print(f"SMS confirmation failed: {e}")
    
    # Log booking confirmation message to conversation
    try:
        conversation = db.query(Conversation).filter(
            Conversation.contact_id == contact_id,
            Conversation.workspace_id == workspace_id
        ).first()
        if conversation:
            confirm_msg = Message(
                conversation_id=conversation.id,
                sender_type="system",
                sender_name="CareOps",
                content=f"✅ Booking confirmed for {booking_details['booking_type']} on {booking_details['scheduled_at']}",
                channel="system"
            )
            db.add(confirm_msg)
            db.commit()
    except Exception as e:
        print(f"Failed to log confirmation message: {e}")
    
    return db_booking

@router.get("/{workspace_id}/list", response_model=list[BookingResponse])
def list_bookings(workspace_id: int, token: str, db: Session = Depends(get_db)):
    user_id = get_current_user_id(token)
    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id,
        Workspace.owner_id == user_id
    ).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    bookings = db.query(Booking).filter(Booking.workspace_id == workspace_id).all()
    return bookings

@router.patch("/{workspace_id}/{booking_id}", response_model=BookingResponse)
def update_booking(workspace_id: int, booking_id: int, booking_update: BookingUpdate, token: str, db: Session = Depends(get_db)):
    user_id = get_current_user_id(token)
    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id,
        Workspace.owner_id == user_id
    ).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.workspace_id == workspace_id
    ).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    booking.status = booking_update.status
    if booking_update.notes:
        booking.notes = booking_update.notes
    
    db.commit()
    db.refresh(booking)
    return booking
