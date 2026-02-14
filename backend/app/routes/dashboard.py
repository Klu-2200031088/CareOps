from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database import get_db
from app.models.models import Workspace, Booking, Contact, FormSubmission, InventoryItem, Conversation
from app.schemas.schemas import DashboardStats, DashboardResponse
from datetime import datetime, timedelta

router = APIRouter()

def get_current_user_id(token: str = None) -> int:
    from app.services.auth_service import decode_token
    if not token:
        raise HTTPException(status_code=401, detail="No token provided")
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return int(payload["sub"])

@router.get("/{workspace_id}", response_model=DashboardResponse)
def get_dashboard(workspace_id: int, token: str, db: Session = Depends(get_db)):
    user_id = get_current_user_id(token)
    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id,
        Workspace.owner_id == user_id
    ).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    # Get stats
    today = datetime.utcnow().date()
    today_bookings = db.query(Booking).filter(
        and_(
            Booking.workspace_id == workspace_id,
            Booking.scheduled_at >= datetime.combine(today, datetime.min.time()),
            Booking.scheduled_at < datetime.combine(today + timedelta(days=1), datetime.min.time())
        )
    ).count()
    
    upcoming_bookings = db.query(Booking).filter(
        and_(
            Booking.workspace_id == workspace_id,
            Booking.scheduled_at > datetime.combine(today + timedelta(days=1), datetime.min.time())
        )
    ).count()
    
    new_inquiries = db.query(Conversation).filter(
        and_(
            Conversation.workspace_id == workspace_id,
            Conversation.is_open == True
        )
    ).count()
    
    pending_forms = db.query(FormSubmission).join(Booking).filter(
        and_(
            Booking.workspace_id == workspace_id,
            FormSubmission.status == "pending"
        )
    ).count()
    
    # Get overdue forms count
    overdue_forms = db.query(FormSubmission).join(Booking).filter(
        and_(
            Booking.workspace_id == workspace_id,
            FormSubmission.status == "pending",
            FormSubmission.due_at < datetime.utcnow()
        )
    ).count()
    
    # Get completed forms count
    completed_forms = db.query(FormSubmission).join(Booking).filter(
        and_(
            Booking.workspace_id == workspace_id,
            FormSubmission.status == "completed"
        )
    ).count()
    
    low_inventory = db.query(InventoryItem).filter(
        and_(
            InventoryItem.workspace_id == workspace_id,
            InventoryItem.quantity <= InventoryItem.low_threshold
        )
    ).count()
    
    stats = DashboardStats(
        today_bookings=today_bookings,
        upcoming_bookings=upcoming_bookings,
        new_inquiries=new_inquiries,
        pending_forms=pending_forms,
        low_inventory_count=low_inventory
    )
    
    # Generate alerts
    alerts = []
    if today_bookings == 0:
        alerts.append({"type": "info", "message": "No bookings scheduled for today"})
    if pending_forms > 0:
        alerts.append({"type": "warning", "message": f"{pending_forms} forms pending completion"})
    if overdue_forms > 0:
        alerts.append({"type": "alert", "message": f"{overdue_forms} forms overdue"})
    if low_inventory > 0:
        alerts.append({"type": "alert", "message": f"{low_inventory} inventory items low"})
    
    # Get recent data
    recent_bookings = db.query(Booking).filter(
        Booking.workspace_id == workspace_id
    ).order_by(Booking.created_at.desc()).limit(5).all()
    
    recent_conversations = db.query(Conversation).filter(
        Conversation.workspace_id == workspace_id
    ).order_by(Conversation.updated_at.desc()).limit(5).all()
    
    return DashboardResponse(
        stats=stats,
        alerts=alerts,
        recent_bookings=recent_bookings,
        recent_conversations=recent_conversations
    )
