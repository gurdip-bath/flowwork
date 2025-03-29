from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db, get_current_active_user, get_current_hr_user, get_current_admin_user
from app.crud import department as department_crud
from app.schemas.department import DepartmentUpdate, DepartmentResponse, DepartmentBase

router = APIRouter(
    prefix="/departments",
    tags=["departments"],
    dependencies=[Depends(get_current_active_user)]
)


@router.get("/", response_model=List[DepartmentResponse])
def read_departments(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """
    Retrieve all departments.
    All active users can view department information.
    """
    departments = department_crud.get_departments(db, skip=skip, limit=limit)
    return departments

@router.get("/{department_id}", response_model=DepartmentResponse)
def read_department(
    department_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """
    Get a specific department by ID.
    """
    db_department = department_crud.get_department(db, department_id=department_id)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return db_department
