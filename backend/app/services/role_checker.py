"""
Role-based access control utilities
"""
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.models import StaffUser, Workspace
from app.services.auth_service import decode_token

class RoleChecker:
    """
    Enforces role-based permissions across the API
    """
    
    @staticmethod
    def check_workspace_owner(workspace_id: int, token: str, db: Session) -> int:
        """
        Verify that the token belongs to the workspace owner
        Returns: user_id if authorized, raises HTTPException otherwise
        """
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No authentication token provided"
            )
        
        payload = decode_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        
        user_id = int(payload["sub"])
        workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
        
        if not workspace:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Workspace not found"
            )
        
        if workspace.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this workspace"
            )
        
        return user_id
    
    @staticmethod
    def check_staff_permission(workspace_id: int, token: str, permission: str, db: Session) -> int:
        """
        Verify that the token belongs to a staff member with the required permission
        
        permission options: 'inbox', 'bookings', 'inventory'
        Returns: user_id if authorized, raises HTTPException otherwise
        """
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No authentication token provided"
            )
        
        payload = decode_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        
        user_id = int(payload["sub"])
        
        # Check if user is owner (owners can do everything)
        workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
        if not workspace:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Workspace not found"
            )
        
        if workspace.owner_id == user_id:
            return user_id
        
        # Check if user is staff with this permission
        staff_user = db.query(StaffUser).filter(
            StaffUser.workspace_id == workspace_id,
            StaffUser.user_id == user_id
        ).first()
        
        if not staff_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not a staff member of this workspace"
            )
        
        # Check specific permission
        permission_map = {
            'inbox': staff_user.can_manage_inbox,
            'bookings': staff_user.can_manage_bookings,
            'inventory': staff_user.can_view_inventory
        }
        
        if permission not in permission_map:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown permission: {permission}"
            )
        
        if not permission_map[permission]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"You do not have '{permission}' permission in this workspace"
            )
        
        return user_id
    
    @staticmethod
    def get_current_user_id(token: str) -> int:
        """
        Extract and validate user ID from token
        """
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No authentication token provided"
            )
        
        payload = decode_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        
        return int(payload["sub"])
