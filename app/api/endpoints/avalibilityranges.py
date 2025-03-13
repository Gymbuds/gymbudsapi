from fastapi import APIRouter,Depends
from app.schemas.range import AvalRangeCreate
from app.db.models.user import User
from app.db.crud.range_crud import create_avail_range,get_availability_ranges_user
from app.core.security import get_current_user
from app.db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/create")
async def createAvailabilityRange(aval_range: AvalRangeCreate,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    user_id = current_user.id
    
    new_range = create_avail_range(db=db, user_id=user_id, day_week=aval_range.day_of_week,start_time=aval_range.start_time,end_time=aval_range.end_time)
    return new_range
@router.get("")
async def get_aval_range(current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    user_id = current_user.id
    new_range = get_availability_ranges_user(db=db, user_id=user_id)
    return new_range
