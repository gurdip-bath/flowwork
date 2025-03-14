from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Onboarding(Base):
    __tablename__ = "onboarding"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), unique=True, nullable=False)
    start_date = Column(Date, nullable=False)
    status = Column(String, nullable=False, default="pending")
    offer_letter_url = Column(String, nullable=True)
    contract_status = Column(String, nullable=False, default="unsigned")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    employee = relationship("Employee", back_populates="onboarding")