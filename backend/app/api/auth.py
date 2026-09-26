from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import User
from app.schemas.schemas import UserLogin, UserCreate, TokenResponse, UserResponse
from app.core.security import verify_password, get_password_hash, create_access_token, decode_access_token

router = APIRouter(prefix="/auth", tags=["Authentication & Access Control"])

@router.post("/login", response_model=TokenResponse)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    token = create_access_token({"sub": user.email, "role": user.role, "user_id": user.id})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }

@router.post("/register", response_model=TokenResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    new_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        role=user_in.role,
        phone=user_in.phone,
        village=user_in.village,
        mandal=user_in.mandal,
        district=user_in.district,
        state=user_in.state or "Andhra Pradesh",
        preferred_language=user_in.preferred_language or "en"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    token = create_access_token({"sub": new_user.email, "role": new_user.role, "user_id": new_user.id})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": new_user
    }

@router.post("/switch-role/{role_name}")
def switch_role(role_name: str, db: Session = Depends(get_db)):
    """
    SIH pitch utility: instantly switches role for demonstration
    """
    valid_roles = ["farmer", "expert", "official", "extension_worker"]
    if role_name not in valid_roles:
        raise HTTPException(status_code=400, detail="Invalid role specified")
        
    email_map = {
        "farmer": "farmer@agriraksha.in",
        "expert": "expert@agriraksha.in",
        "official": "official@agriraksha.in",
        "extension_worker": "extension@agriraksha.in"
    }
    user = db.query(User).filter(User.email == email_map[role_name]).first()
    if not user:
        user = db.query(User).filter(User.role == role_name).first()
    if not user:
        raise HTTPException(status_code=404, detail="Demo account for this role not found. Please click 'Load Demo Dataset' first.")
        
    token = create_access_token({"sub": user.email, "role": user.role, "user_id": user.id})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }
