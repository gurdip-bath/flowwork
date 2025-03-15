from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    role: str
    is_active: bool = True

class UserCreate(UserBase):
    password: str  # Only for creation


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None  # Optional for updates

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True