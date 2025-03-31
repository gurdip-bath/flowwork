from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    """Enum for user roles to ensure consistency"""
    ADMIN = "admin"
    HR = "hr"
    USER = "user"


class UserBase(BaseModel):
    email: EmailStr
    role: UserRole = UserRole.USER  # Default role
    is_active: bool = True


class UserCreate(UserBase):
    password: str  # Only for creation
    
    @field_validator('password')
    def password_min_length(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None  # Optional for updates
    
    @field_validator('password')
    def password_min_length(cls, v):
        if v is not None and len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True