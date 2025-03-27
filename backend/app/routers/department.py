from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db, get_current_active_user, get_current_hr_user, get_current_admin_user
from app.crud import department as department_crud
from app.schemas.department import DepartmentUpdate, DepartmentResponse, DepartmentBase