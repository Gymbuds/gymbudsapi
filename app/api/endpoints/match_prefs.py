from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import get_current_user
from app.db.crud.match_preferences_crud import (
    create_match_preference,
    get_match_preference,
    update_match_preference,
)
from app.db.models.user import User
from app.schemas.match import MatchPreferenceUpdate

router = APIRouter()

# Create match preference
# @router.post("")
# def create_match_pref(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     """
#     create match preference for the current user.
#     to be called when user account is first created.
#     """
#     return create_match_preference(db=db, user_id=current_user.id)

# Get match preference
@router.get("")
def get_match_pref(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    match_pref = get_match_preference(db=db, user_id=current_user.id)
    if not match_pref:
        raise HTTPException(status_code=404, detail="Match preference not found")
    return match_pref

# Update match preference
@router.patch("")
def update_match_pref(
    update_data: MatchPreferenceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    return update_match_preference(
        db=db,
        user_id=current_user.id,
        gender=update_data.gender,
        start_weight=update_data.start_weight,
        end_weight=update_data.end_weight,
        max_location_distance_miles=update_data.max_location_distance_miles
    )
