from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    department_id: Optional[int] = None
    position: str
    status: str = "active"
    
class EmployeeCreate(EmployeeBase):
    user_id: int
    hire_date: Optional[date] = None