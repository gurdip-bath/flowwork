from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db, get_current_active_user, get_current_admin_user
from app.crud import user as user_crud
from app.schemas.user import UserCreate, UserUpdate, UserResponse

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_active_user)]
)

@router.get("/me", response_model=UserResponse)
def read_user_me(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """
    Get the current user's information.
    """
    db_user = user_crud.get_user_by_email(db, email=current_user.get("sub"))
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/", response_model=List[UserResponse])
def read_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    """
    Retrieve users with pagination.
    Admin users only.
    """
    users = user_crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """
    Get a specific user by ID.
    Users can only access their own information unless they are admins.
    """
    # Check if user is requesting their own info or is an admin
    if current_user.get("id") != user_id and current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this user's data"
        )
    
    db_user = user_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    """
    Create a new user.
    Admin users only.
    """
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return user_crud.create_user(db=db, user=user)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int, 
    user: UserUpdate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """
    Update a user.
    Users can only update their own information unless they are admins.
    """
    # Check if user is updating their own info or is an admin
    if current_user.get("id") != user_id and current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this user"
        )
    
    db_user = user_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    updated_user = user_crud.update_user(db=db, user_id=user_id, user=user)
    return updated_user


@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    """
    Delete a user.
    Admin users only.
    """
    db_user = user_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    deleted_user = user_crud.delete_user(db=db, user_id=user_id)
    return deleted_user