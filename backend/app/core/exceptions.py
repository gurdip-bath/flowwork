from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ErrorResponse(BaseModel):
    """
    Base class for error responses.
    """
    status_code: int
    message: str
    error: Optional[str] = None
    timestamp: datetime = datetime.today()