from fastapi import APIRouter,Depends,Body
from app.schemas.range import AvalRangeCreate,AvalRangeDelete
from app.db.models.user import User
from app.db.crud.range_crud import create_avail_range,get_availability_ranges_user,delete_aval_range
from app.core.security import get_current_user
from app.db.session import get_db
from app.services.matching import match_users
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/create")
async def create_availability_range(aval_range: AvalRangeCreate,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    """
    Create a new availability range for a user.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user.
        start_time (time): The start time of the availability range.
        end_time (time): The end time of the availability range.
        day_week (str): The day of the week for the availability range.

    Returns:
        AvailabilityRange: The created availability range.
    """
    user_id = current_user.id
    
    new_range = create_avail_range(db=db, user_id=user_id, day_week=aval_range.day_of_week,start_time=aval_range.start_time,end_time=aval_range.end_time)
    return new_range
@router.get("")
async def get_availability_range(current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    """
    Get all availability ranges for a user.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user.

    Returns:
        list: A list of availability ranges for the user.
    """
    user_id = current_user.id
    new_range = get_availability_ranges_user(db=db, user_id=user_id)
    return new_range
@router.delete("")
async def delete_availability_range(aval_range: AvalRangeDelete= Body(...), current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    """
    Delete an availability range for the authenticated user.

    Args:
        aval_range_id (int): The ID of the availability range to be deleted.
        db (Session): The database session.
        current_user (User): The currently authenticated user.

    Raises:
        HTTPException: If the availability range is not found or the user is not authorized to delete it.

    Returns:
        AvailabilityRange: The deleted availability range.
    """
    user_id = current_user.id
    return delete_aval_range(db=db, aval_range_id=aval_range.id, user_id=user_id)


