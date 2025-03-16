from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date

class OnboardingBase(BaseModel):
    employee_id: int
    start_date: date
    status: str = "pending"
    contract_status: str = "unsigned"
    offer_letter_url: Optional[str] = None

class OnboardingCreate(OnboardingBase):
    pass

class OnboardingUpdate(BaseModel):
    start_date: Optional[date] = None
    status: Optional[str] = None
    contract_status: Optional[str] = None
    offer_letter_url: Optional[str] = None

class OnboardingResponse(OnboardingBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True