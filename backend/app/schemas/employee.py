from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date


class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    department_id: Optional[int] = None
    position: str
    status: str = Field("active", pattern="^(active|inactive|on_leave|terminated)$")

class EmployeeCreate(EmployeeBase):
    user_id: int
    hire_date: Optional[date] = None

class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    department_id: Optional[int] = None
    position: Optional[str] = None
    status: Optional[str] = None

class EmployeeResponse(EmployeeBase):
    id: int
    user_id: int
    hire_date: date

    class Config:
        orm_mode = True

