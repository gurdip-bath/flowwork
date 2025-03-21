from sqlalchemy.orm import Session
from app.models.employee import Employee
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash

def get_employee(db: Session, employee_id: int):
    return db.query(Employee).filter(Employee.id == employee_id).first()

def get_employee_by_email(db: Session, email: str):
    return db.query(Employee).filter(Employee.email == email).first()

def get_employees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Employee).offset(skip).limit(limit).all()