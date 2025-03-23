from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    """
    Schema for authentication token response.
    """
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    """
    Schema for JWT token payload.
    """
    sub: Optional[str] = None
    id: Optional[int] = None
    role: Optional[str] = None
    exp: Optional[int] = None