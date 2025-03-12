from fastapi import APIRouter,Depends,HTTPException,status
from app.schemas.range import AvalRangeCreate
from app.db.models.user import User
from app.db.crud.range_crud import createavalRange
from app.db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/create")
async def createAvalibilityRange(aval_range: AvalRangeCreate,db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == aval_range.user_email).first()
    if existing_user:
        user_id = existing_user.id
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User Does not exist"
        )
    new_range = createavalRange(db=db, user_id=user_id, day_week=aval_range.day_of_week,start_time=aval_range.start_time,end_time=aval_range.end_time)
    return new_range