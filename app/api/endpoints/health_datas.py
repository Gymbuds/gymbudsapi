from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.health_data import HealthDataCreate,HealthDataResponse
from app.db.crud.health_data_crud import create_health_data, get_health_data_by_date, update_health_data,get_all_health_data_by_id
from app.core.security import get_current_user 
from app.db.models.user import User
from typing import List
router = APIRouter()

@router.post("", response_model=HealthDataResponse)
def create_user_health_data(
    health_data: HealthDataCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_health_data(db, current_user.id, health_data)

@router.get("/{date}", response_model=HealthDataResponse)
def get_user_health_data(
    date: str,  
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_health_data_by_date(db, current_user.id, date)

@router.patch("/{health_id}", response_model=HealthDataResponse)
def update_user_health_data(
    health_id: int,
    health_data: HealthDataCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_health_data(db, health_id, current_user.id, health_data)

@router.get("",response_model = List[HealthDataResponse])
def get_all_health_datas_for_user(db:Session= Depends(get_db),current_user: User= Depends(get_current_user)):
    return get_all_health_data_by_id(db,current_user.id)