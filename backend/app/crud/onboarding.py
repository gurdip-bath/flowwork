from sqlalchemy.orm import Session
from app.models.onboarding import Onboarding
from app.schemas.onboarding import OnboardingCreate, OnboardingUpdate, OnboardingResponse

def get_onboarding(db: Session, onboarding_id: int):
   return db.query(Onboarding).filter(Onboarding.id == onboarding_id).first()

def get_onboarding_by_employee(db: Session, employee_id: int):
   return db.query(Onboarding).filter(Onboarding.employee_id == employee_id).first()

def get_onboardings(db: Session, skip: int = 0, limit: int = 100):
   return db.query(Onboarding).offset(skip).limit(limit).all()

def get_onboardings_by_status(db: Session, status: str):
   return db.query(Onboarding).filter(Onboarding.status == status).all()

def create_onboarding(db: Session, onboarding: OnboardingCreate):
   db_onboarding = Onboarding(
       employee_id=onboarding.employee_id,
       start_date=onboarding.start_date,
       status=onboarding.status,
       
   )
   db.add(db_onboarding)
   db.commit()
   db.refresh(db_onboarding)
   return db_onboarding

def update_onboarding(db: Session, onboarding_id: int, onboarding: OnboardingUpdate):
   db_onboarding = get_onboarding(db, onboarding_id)
   if not db_onboarding:
       return None
   
   update_data = onboarding.model_dump(exclude_unset=True)
   for key, value in update_data.items():
       setattr(db_onboarding, key, value)
   
   db.commit()
   db.refresh(db_onboarding)
   return db_onboarding

def delete_onboarding(db: Session, onboarding_id: int):
   db_onboarding = get_onboarding(db, onboarding_id)
   if not db_onboarding:
       return None
   
   db.delete(db_onboarding)
   db.commit()
   return db_onboarding