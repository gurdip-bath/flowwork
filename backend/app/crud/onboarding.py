from sqlalchemy.orm import Session
from app.models.onboarding import Onboarding
from app.schemas.onboarding import OnboardingCreate, OnboardingUpdate, OnboardingResponse

def get_onboarding(db: Session, onboarding_id: int):
   return db.query(Onboarding).filter(Onboarding.id == onboarding_id).first()

def get_onboarding_by_employee(db: Session, employee_id: int):
   return db.query(Onboarding).filter(Onboarding.employee_id == employee_id).first()