from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User
from app.schemas.schemas import UserCreate, UserResponse, Token, SMSVerificationRequest
from app.services.auth_service import get_password_hash, verify_password, create_access_token
from app.integrations.sms_service import sms_service
from datetime import timedelta, datetime
import random
import string

router = APIRouter()

def generate_verification_code() -> str:
    """Generate a 6-digit verification code"""
    return ''.join(random.choices(string.digits, k=6))

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # Check if user exists
        db_user = db.query(User).filter(User.email == user.email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Validate input
        if not user.email or not user.password or not user.full_name:
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        if len(user.password) < 6:
            raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
        
        # Create new user
        verification_code = None
        is_phone_verified = False
        
        # If phone provided, generate verification code
        if user.phone_number:
            verification_code = generate_verification_code()
            is_phone_verified = False
        
        db_user = User(
            email=user.email,
            hashed_password=get_password_hash(user.password),
            full_name=user.full_name,
            phone_number=user.phone_number,
            is_active=True,
            is_phone_verified=is_phone_verified,
            verification_code=verification_code,
            verification_code_expires=datetime.utcnow() + timedelta(minutes=10) if verification_code else None
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Send SMS if phone number provided
        if verification_code and user.phone_number:
            sms_result = sms_service.send_verification_code(user.phone_number, verification_code)
            print(f"SMS verification sent: {sms_result}")
        
        return db_user
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Registration error: {e}")
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@router.post("/verify-sms")
def verify_sms(email: str, request: SMSVerificationRequest, db: Session = Depends(get_db)):
    """Verify SMS code and mark phone as verified"""
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if not user.verification_code:
            raise HTTPException(status_code=400, detail="No verification code sent")
        
        if datetime.utcnow() > user.verification_code_expires:
            raise HTTPException(status_code=400, detail="Verification code expired")
        
        if user.verification_code != request.code:
            raise HTTPException(status_code=400, detail="Invalid verification code")
        
        # Mark as verified
        user.is_phone_verified = True
        user.verification_code = None
        user.verification_code_expires = None
        db.commit()
        db.refresh(user)
        
        return {"status": "success", "message": "Phone verified successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")

@router.post("/resend-sms")
def resend_sms(email: str, db: Session = Depends(get_db)):
    """Resend SMS verification code"""
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if not user.phone_number:
            raise HTTPException(status_code=400, detail="No phone number on file")
        
        if user.is_phone_verified:
            raise HTTPException(status_code=400, detail="Phone already verified")
        
        # Generate new code
        verification_code = generate_verification_code()
        user.verification_code = verification_code
        user.verification_code_expires = datetime.utcnow() + timedelta(minutes=10)
        db.commit()
        
        # Send SMS
        sms_result = sms_service.send_verification_code(user.phone_number, verification_code)
        print(f"SMS resent: {sms_result}")
        
        return {"status": "success", "message": "Verification code resent"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Resend failed: {str(e)}")
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": str(user.id), "email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_current_user(token: str, db: Session = Depends(get_db)):
    from app.services.auth_service import decode_token
    payload = decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = int(payload["sub"])
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
