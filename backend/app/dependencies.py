from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional, Dict

from app.db.session import SessionLocal
from app.core.config import settings
from app.core.security import verify_password
from app.crud import user as user_crud

# OAuth2 scheme for token validation
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")



def get_db():
    """
    Dependency for database session handling.
    Creates a new session for each request and closes it after the request is complete.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def authenticate_user(db: Session, email: str, password: str):
    """
    Authenticate a user with email and password.
    """
    print(f"[AUTH] Attempting to authenticate: {email}")
    user = user_crud.get_user_by_email(db, email=email)
    if not user:
        print(f"[AUTH] User not found: {email}")
        return False
    print(f"[AUTH] User found: {user.email}, ID: {user.id}, Active: {user.is_active}")
    
    password_match = verify_password(password, user.password_hash)
    print(f"[AUTH] Password verification result: {password_match}")
    
    if not password_match:
        print(f"[AUTH] Password mismatch for user: {email}")
        return False
    
    print(f"[AUTH] Authentication successful for: {email}")
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token.
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> Dict:
    """
    Validate access token and return current user data.
    """
    print("get_current_user called")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode JWT token
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        
        # Extract user data
        email: str = payload.get("sub")
        user_id: int = payload.get("id")
        role: str = payload.get("role")
        
        if email is None or user_id is None:
            raise credentials_exception
            
        token_data = {"sub": email, "id": user_id, "role": role}
    except JWTError:
        raise credentials_exception
        
    # Verify user exists in database
    user = user_crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
        
    return token_data


def get_current_active_user(current_user: Dict = Depends(get_current_user)) -> Dict:
    """
    Ensure the current user is active.
    """
    return current_user


def get_current_admin_user(current_user: Dict = Depends(get_current_user)) -> Dict:
    """
    Ensure the current user has admin role.
    """
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Admin role required."
        )
    return current_user


def get_current_hr_user(current_user: Dict = Depends(get_current_user)) -> Dict:
    """
    Ensure the current user has HR or admin role.
    """
    if current_user.get("role") not in ["hr", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. HR or admin role required."
        )
    return current_user
