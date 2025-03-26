from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.health_data import HealthDataCreate,HealthDataResponse
from app.db.crud.health_data_crud import create_health_data
from app.core.security import get_current_user 
from app.db.models.user import User

router = APIRouter()

@router.post("/", response_model=HealthDataResponse)
def create_user_health_data(
    health_data: HealthDataCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_health_data(db, current_user.id, health_data)