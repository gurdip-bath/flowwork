from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class OnboardingBase(BaseModel):
    employee_id: int
    start_date: date
    status: str = "pending"
    contract_status: str = "unsigned"
    offer_letter_url: Optional[str] = None