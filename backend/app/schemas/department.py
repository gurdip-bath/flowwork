from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DepartmentBase(BaseModel):
    name: str
    description: Optional[str] = None
    manager_id: Optional[int] = None

class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    manager_id: Optional[int] = None

class DepartmentResponse(DepartmentBase):
    id: int

    class Config:
        orm_mode = True