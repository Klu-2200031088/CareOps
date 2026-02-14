from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import InventoryItem, Workspace
from app.schemas.schemas import InventoryItemCreate, InventoryItemResponse

router = APIRouter()

def get_current_user_id(token: str = None) -> int:
    from app.services.auth_service import decode_token
    if not token:
        raise HTTPException(status_code=401, detail="No token provided")
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return int(payload["sub"])

@router.post("/{workspace_id}/create", response_model=InventoryItemResponse)
def create_inventory_item(workspace_id: int, item: InventoryItemCreate, token: str, db: Session = Depends(get_db)):
    user_id = get_current_user_id(token)
    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id,
        Workspace.owner_id == user_id
    ).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    db_item = InventoryItem(
        workspace_id=workspace_id,
        name=item.name,
        quantity=item.quantity,
        quantity_per_booking=item.quantity_per_booking,
        low_threshold=item.low_threshold
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/{workspace_id}/list", response_model=list[InventoryItemResponse])
def list_inventory(workspace_id: int, token: str, db: Session = Depends(get_db)):
    user_id = get_current_user_id(token)
    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id,
        Workspace.owner_id == user_id
    ).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    items = db.query(InventoryItem).filter(InventoryItem.workspace_id == workspace_id).all()
    return items
