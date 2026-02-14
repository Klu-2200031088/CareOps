from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Workspace, User, Contact, Booking, Form, InventoryItem
from app.schemas.schemas import WorkspaceCreate, WorkspaceResponse, DashboardStats, DashboardResponse
from datetime import datetime, timedelta

router = APIRouter()

def get_current_user_id(token: str = None) -> int:
    # This is simplified - in production use proper dependency injection
    from app.services.auth_service import decode_token
    if not token:
        raise HTTPException(status_code=401, detail="No token provided")
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return int(payload["sub"])

@router.post("/create", response_model=WorkspaceResponse)
def create_workspace(workspace: WorkspaceCreate, token: str, db: Session = Depends(get_db)):
    user_id = get_current_user_id(token)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_workspace = Workspace(
        name=workspace.name,
        owner_id=user_id,
        address=workspace.address,
        timezone=workspace.timezone,
        contact_email=workspace.contact_email,
        is_active=False
    )
    db.add(db_workspace)
    db.commit()
    db.refresh(db_workspace)
    return db_workspace

@router.get("/list", response_model=list[WorkspaceResponse])
def list_workspaces(token: str, db: Session = Depends(get_db)):
    user_id = get_current_user_id(token)
    workspaces = db.query(Workspace).filter(Workspace.owner_id == user_id).all()
    return workspaces

@router.get("/{workspace_id}", response_model=WorkspaceResponse)
def get_workspace(workspace_id: int, token: str, db: Session = Depends(get_db)):
    user_id = get_current_user_id(token)
    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id,
        Workspace.owner_id == user_id
    ).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return workspace

@router.post("/{workspace_id}/activate")
def activate_workspace(workspace_id: int, token: str, db: Session = Depends(get_db)):
    user_id = get_current_user_id(token)
    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id,
        Workspace.owner_id == user_id
    ).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    # Verify prerequisites for activation
    validation_errors = []
    
    # Check if at least one booking type exists
    bookings = db.query(Booking).filter(Booking.workspace_id == workspace_id).first()
    if not bookings:
        validation_errors.append("At least one booking type must be created")
    
    # Check if communication channel is set up (email address available)
    if not workspace.contact_email:
        validation_errors.append("Communication channel (email) must be configured")
    
    # Check if at least contact form is ready (forms exist for this workspace)
    forms = db.query(Form).filter(Form.workspace_id == workspace_id).first()
    if not forms:
        validation_errors.append("At least one form template should be created for customers")
    
    if validation_errors:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot activate workspace: {'; '.join(validation_errors)}"
        )
    
    # All checks passed - activate workspace
    workspace.is_active = True
    db.commit()
    return {"status": "activated", "message": "Workspace is now live!"}
