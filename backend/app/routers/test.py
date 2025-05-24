from fastapi import APIRouter
from app.services.email_service import send_email

router = APIRouter(prefix="/test", tags=["testing"])

@router.get("/send-basic-email")
def test_email():
    """Send test email"""
    result = send_email()
    return {"message": "Email sent", "status": result['status_code']}