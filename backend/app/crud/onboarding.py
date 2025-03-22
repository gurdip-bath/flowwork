from sqlalchemy.orm import Session
from app.models.onboarding import Onboarding
from app.schemas.onboarding import OnboardingCreate, OnboardingUpdate, OnboardingResponse

def get_onboarding(db: Session, onboarding_id: int):
   return db.query(Onboarding).filter(Onboarding.id == onboarding_id).first()