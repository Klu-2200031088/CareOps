from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Form, Workspace
from app.schemas.schemas import FormCreate, FormResponse

router = APIRouter()

def get_current_user_id(token: str = None) -> int:
    from app.services.auth_service import decode_token
    if not token:
        raise HTTPException(status_code=401, detail="No token provided")
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return int(payload["sub"])

@router.post("/{workspace_id}/create", response_model=FormResponse)
def create_form(workspace_id: int, form: FormCreate, token: str, db: Session = Depends(get_db)):
    user_id = get_current_user_id(token)
    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id,
        Workspace.owner_id == user_id
    ).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    db_form = Form(
        workspace_id=workspace_id,
        name=form.name,
        description=form.description,
        required_fields=form.required_fields,
        is_active=True
    )
    db.add(db_form)
    db.commit()
    db.refresh(db_form)
    return db_form

@router.get("/{workspace_id}/list", response_model=list[FormResponse])
def list_forms(workspace_id: int, token: str, db: Session = Depends(get_db)):
    user_id = get_current_user_id(token)
    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id,
        Workspace.owner_id == user_id
    ).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    forms = db.query(Form).filter(Form.workspace_id == workspace_id).all()
    return forms
