from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from datetime import datetime
import uuid

from app.dependencies import get_db, get_current_active_user, get_current_hr_user
from app.crud import onboarding as onboarding_crud
from app.crud import employee as employee_crud
from app.schemas.onboarding import OnboardingCreate, OnboardingUpdate, OnboardingResponse
from app.core.config import settings

router = APIRouter(
    prefix="/onboarding",
    tags=["onboarding"],
    dependencies=[Depends(get_current_active_user)]
)


@router.get("/", response_model=List[OnboardingResponse])
def read_onboardings(
    skip: int = 0, 
    limit: int = 100, 
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_hr_user)
):
    """
    Retrieve all onboarding records with optional status filter.
    HR or admin users only.
    """
    if status:
        onboardings = onboarding_crud.get_onboardings_by_status(db, status=status)
    else:
        onboardings = onboarding_crud.get_onboardings(db, skip=skip, limit=limit)
    return onboardings


@router.get("/{onboarding_id}", response_model=OnboardingResponse)
def read_onboarding(
    onboarding_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_hr_user)
):
    """
    Get a specific onboarding record by ID.
    HR or admin users only.
    """
    db_onboarding = onboarding_crud.get_onboarding(db, onboarding_id=onboarding_id)
    if db_onboarding is None:
        raise HTTPException(status_code=404, detail="Onboarding record not found")
    return db_onboarding


@router.get("/employee/{employee_id}", response_model=OnboardingResponse)
def read_employee_onboarding(
    employee_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """
    Get onboarding record for a specific employee.
    Users can view their own onboarding status, HR and admins can view all.
    """
    # Check if user is requesting their own info or is HR/admin
    if (current_user.get("role") not in ["hr", "admin"] and 
        employee_crud.get_employee_by_email(db, email=current_user.get("sub")).id != employee_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this employee's onboarding data"
        )
    
    db_onboarding = onboarding_crud.get_onboarding_by_employee(db, employee_id=employee_id)
    if db_onboarding is None:
        raise HTTPException(status_code=404, detail="Onboarding record not found for this employee")
    return db_onboarding


@router.post("/", response_model=OnboardingResponse, status_code=status.HTTP_201_CREATED)
def create_onboarding(
    onboarding: OnboardingCreate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_hr_user)
):
    """
    Create a new onboarding record.
    HR or admin users only.
    """
    # Check if employee exists
    employee = employee_crud.get_employee(db, employee_id=onboarding.employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    # Check if onboarding already exists for this employee
    existing_onboarding = onboarding_crud.get_onboarding_by_employee(db, employee_id=onboarding.employee_id)
    if existing_onboarding:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Onboarding record already exists for this employee"
        )
    
    return onboarding_crud.create_onboarding(db=db, onboarding=onboarding)


@router.put("/{onboarding_id}", response_model=OnboardingResponse)
def update_onboarding(
    onboarding_id: int, 
    onboarding: OnboardingUpdate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_hr_user)
):
    """
    Update an onboarding record.
    HR or admin users only.
    """
    db_onboarding = onboarding_crud.get_onboarding(db, onboarding_id=onboarding_id)
    if db_onboarding is None:
        raise HTTPException(status_code=404, detail="Onboarding record not found")
    
    updated_onboarding = onboarding_crud.update_onboarding(
        db=db, onboarding_id=onboarding_id, onboarding=onboarding
    )
    return updated_onboarding


@router.delete("/{onboarding_id}", response_model=OnboardingResponse)
def delete_onboarding(
    onboarding_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_hr_user)
):
    """
    Delete an onboarding record.
    HR or admin users only.
    """
    db_onboarding = onboarding_crud.get_onboarding(db, onboarding_id=onboarding_id)
    if db_onboarding is None:
        raise HTTPException(status_code=404, detail="Onboarding record not found")
    
    deleted_onboarding = onboarding_crud.delete_onboarding(db=db, onboarding_id=onboarding_id)
    return deleted_onboarding


@router.post("/{onboarding_id}/upload-offer-letter", response_model=OnboardingResponse)
def upload_offer_letter(
    onboarding_id: int,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_hr_user)
):
    """
    Upload an offer letter for an onboarding employee.
    HR or admin users only.
    """
    db_onboarding = onboarding_crud.get_onboarding(db, onboarding_id=onboarding_id)
    if db_onboarding is None:
        raise HTTPException(status_code=404, detail="Onboarding record not found")
    
    # Save file with a unique name
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
    
    # Create directory if it doesn't exist
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # Write file
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    
    # Update onboarding record with file URL
    update_data = OnboardingUpdate(
        offer_letter_url=f"/uploads/{unique_filename}"
    )
    
    updated_onboarding = onboarding_crud.update_onboarding(
        db=db, onboarding_id=onboarding_id, onboarding=update_data
    )
    return updated_onboarding


@router.post("/{onboarding_id}/send-contract", response_model=OnboardingResponse)
def send_contract(
    onboarding_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_hr_user)
):
    """
    Send a contract for signature using DocuSign.
    HR or admin users only.
    """
    db_onboarding = onboarding_crud.get_onboarding(db, onboarding_id=onboarding_id)
    if db_onboarding is None:
        raise HTTPException(status_code=404, detail="Onboarding record not found")
    
    # Get employee details
    employee = employee_crud.get_employee(db, employee_id=db_onboarding.employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    # Update contract status
    update_data = OnboardingUpdate(contract_status="sent")
    updated_onboarding = onboarding_crud.update_onboarding(
        db=db, onboarding_id=onboarding_id, onboarding=update_data
    )
    
    return updated_onboarding


@router.post("/{onboarding_id}/complete", response_model=OnboardingResponse)
def complete_onboarding(
    onboarding_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_hr_user)
):
    """
    Mark an onboarding process as complete.
    HR or admin users only.
    """
    db_onboarding = onboarding_crud.get_onboarding(db, onboarding_id=onboarding_id)
    if db_onboarding is None:
        raise HTTPException(status_code=404, detail="Onboarding record not found")
    
    # Check if contract is signed
    if db_onboarding.contract_status != "signed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot complete onboarding until contract is signed"
        )
    
    # Update onboarding status
    update_data = OnboardingUpdate(status="completed")
    updated_onboarding = onboarding_crud.update_onboarding(
        db=db, onboarding_id=onboarding_id, onboarding=update_data
    )
    
    return updated_onboarding