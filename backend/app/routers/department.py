from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db, get_current_active_user, get_current_hr_user, get_current_admin_user
from app.crud import department as department_crud
from app.schemas.department import DepartmentResponse, DepartmentUpdate, DepartmentBase

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

@router.put("/{department_id}", response_model=DepartmentResponse)
def update_department(
    department_id: int, 
    department: DepartmentUpdate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_hr_user)
):
    """
    Update a department.
    HR or admin users only.
    """
    db_department = department_crud.get_department(db, department_id=department_id)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    
    # If name is being updated, check it's not already in use
    if department.name and department.name != db_department.name:
        existing_name = department_crud.get_department_by_name(db, name=department.name)
        if existing_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Department with this name already exists"
            )
    
    updated_department = department_crud.update_department(
        db=db, department_id=department_id, department=department
    )
    return updated_department


@router.delete("/{department_id}", response_model=DepartmentResponse)
def delete_department(
    department_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    """
    Delete a department.
    Admin users only.
    """
    db_department = department_crud.get_department(db, department_id=department_id)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    
    deleted_department = department_crud.delete_department(db=db, department_id=department_id)
    return deleted_department