from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    manager_id = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)
    
    # Relationships
    employees = relationship("Employee", back_populates="department", foreign_keys="[Employee.department_id]")
    manager = relationship("Employee", foreign_keys=[manager_id], post_update=True)