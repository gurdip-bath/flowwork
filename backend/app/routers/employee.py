from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.dependencies import get_db, get_current_active_user, get_current_admin_user, get_current_hr_user
from app.crud import employee as employee_crud
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse

router = APIRouter(
    prefix="/employees",
    tags=["employees"],
    dependencies=[Depends(get_current_active_user)]
)


@router.get("/", response_model=List[EmployeeResponse])
def read_employees(
    skip: int = 0, 
    limit: int = 100, 
    department_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """
    Retrieve employees with optional filtering by department.
    All active users can access basic employee information.
    """
    if department_id:
        employees = employee_crud.get_employees_by_department(db, department_id=department_id)
    else:
        employees = employee_crud.get_employees(db, skip=skip, limit=limit)
    return employees


@router.get("/{employee_id}", response_model=EmployeeResponse)
def read_employee(
    employee_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """
    Get a specific employee by ID.
    """
    db_employee = employee_crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee


@router.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(
    employee: EmployeeCreate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_hr_user)
):
    """
    Create a new employee.
    HR or admin users only.
    """
    db_employee_email = employee_crud.get_employee_by_email(db, email=employee.email)
    if db_employee_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered to an employee"
        )
    
    return employee_crud.create_employee(db=db, employee=employee)


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int, 
    employee: EmployeeUpdate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_hr_user)
):
    """
    Update an employee.
    HR or admin users only.
    """
    db_employee = employee_crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # If email is being updated, check it's not already in use
    if employee.email and employee.email != db_employee.email:
        existing_email = employee_crud.get_employee_by_email(db, email=employee.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered to another employee"
            )
    
    updated_employee = employee_crud.update_employee(db=db, employee_id=employee_id, employee=employee)
    return updated_employee


@router.delete("/{employee_id}", response_model=EmployeeResponse)
def delete_employee(
    employee_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    """
    Delete an employee.
    Admin users only.
    """
    db_employee = employee_crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    deleted_employee = employee_crud.delete_employee(db=db, employee_id=employee_id)
    return deleted_employee


@router.get("/me", response_model=EmployeeResponse)
def read_employee_me(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """
    Get the current employee's information.
    """
    db_employee = employee_crud.get_employee_by_email(db, email=current_user.get("sub"))
    if db_employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Employee profile not found for current user"
        )
    return db_employee