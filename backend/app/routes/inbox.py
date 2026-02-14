from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database import get_db
from app.models.models import Conversation, Message, Workspace, Contact, StaffUser
from app.schemas.schemas import MessageCreate, ConversationResponse
from app.services.role_checker import RoleChecker
from app.services.automation_service import automation_service
from datetime import datetime

router = APIRouter()

def get_current_user_id(token: str = None) -> int:
    from app.services.auth_service import decode_token
    if not token:
        raise HTTPException(status_code=401, detail="No token provided")
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return int(payload["sub"])

@router.get("/{workspace_id}/conversations", response_model=list[ConversationResponse])
def get_conversations(workspace_id: int, token: str, db: Session = Depends(get_db)):
    # Check if owner or staff with inbox permission
    try:
        user_id = RoleChecker.check_staff_permission(workspace_id, token, 'inbox', db)
    except HTTPException:
        # If not staff, check if owner
        user_id = RoleChecker.check_workspace_owner(workspace_id, token, db)
    
    conversations = db.query(Conversation).filter(Conversation.workspace_id == workspace_id).all()
    return conversations

@router.post("/{workspace_id}/conversations/{conversation_id}/send", response_model=dict)
def send_message(workspace_id: int, conversation_id: int, message: MessageCreate, token: str, db: Session = Depends(get_db)):
    # Check if owner or staff with inbox permission
    try:
        user_id = RoleChecker.check_staff_permission(workspace_id, token, 'inbox', db)
    except HTTPException:
        # If not staff, check if owner
        user_id = RoleChecker.check_workspace_owner(workspace_id, token, db)
    
    workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    conversation = db.query(Conversation).filter(
        and_(
            Conversation.id == conversation_id,
            Conversation.workspace_id == workspace_id
        )
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    db_message = Message(
        conversation_id=conversation_id,
        sender_type=message.sender_type,
        sender_name="Staff User",
        content=message.content,
        channel=message.channel
    )
    db.add(db_message)
    
    # Update conversation
    conversation.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_message)
    
    # Trigger automation on staff reply
    if message.sender_type == "staff":
        try:
            automation_service.on_staff_reply(db_message, conversation, db)
        except Exception as e:
            print(f"Automation trigger failed: {e}")
    
    return {"status": "sent", "message_id": db_message.id}

@router.get("/{workspace_id}/conversations/{conversation_id}", response_model=ConversationResponse)
def get_conversation(workspace_id: int, conversation_id: int, token: str, db: Session = Depends(get_db)):
    # Check if owner or staff with inbox permission
    try:
        user_id = RoleChecker.check_staff_permission(workspace_id, token, 'inbox', db)
    except HTTPException:
        # If not staff, check if owner
        user_id = RoleChecker.check_workspace_owner(workspace_id, token, db)
    
    workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    conversation = db.query(Conversation).filter(
        and_(
            Conversation.id == conversation_id,
            Conversation.workspace_id == workspace_id
        )
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return conversation
