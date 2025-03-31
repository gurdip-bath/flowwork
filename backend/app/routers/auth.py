from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.dependencies import get_db, authenticate_user, create_access_token
from app.core.config import settings
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse
from app.crud import user as user_crud

router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)


@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Authenticate user and provide a JWT access token.
    
    This endpoint:
    1. Takes username (email) and password from form data
    2. Validates the credentials against the database
    3. Returns a JWT token if authentication succeeds
    """
    # Authenticate user (email is used as username)
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token with expiration time
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "id": user.id, "role": user.role},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_new_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user account.
    
    This endpoint:
    1. Takes user details including email and password
    2. Checks if the email is already registered
    3. Creates a new user with hashed password
    4. Returns the created user info (without password)
    """
    # Check if user already exists
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user with regular user role by default
    # You can customize this if needed, e.g., first user is admin
    user_data = user.model_dump() 
    if "role" not in user_data or not user_data["role"]:
        user_data["role"] = "user"  # Default role
    
    # Create user in database
    return user_crud.create_user(db=db, user=UserCreate(**user_data))