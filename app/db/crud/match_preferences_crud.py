from sqlalchemy.orm import Session
from app.db.models.match_preferences import MatchPreference
from app.schemas.match import GenderPref
from app.db.crud.user_crud import get_user_info_by_id
from fastapi import HTTPException,status

def create_match_preference(db:Session,user_id:int):
    user = get_user_info_by_id(db=db,user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    pot_match_pref = db.query(MatchPreference).filter(MatchPreference.user_id==user_id).first()
    if pot_match_pref is not None:
         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User Match Pref exists already")
    match_pref = MatchPreference(
        user_id=user_id,
        gender=GenderPref.BOTH,
        start_weight=0,
        end_weight = 500,
        max_location_distance_miles=25,
    )
    db.add(match_pref)
    db.commit()
    db.refresh(match_pref)

def update_match_preference(db:Session,user_id:int,gender:GenderPref | None, start_weight:int  | None,end_weight:int| None,max_location_distance_miles:int| None):
    match_pref = db.query(MatchPreference).filter(MatchPreference.user_id==user_id).first()
    if not match_pref:
        raise HTTPException(status_code=404, detail="Match Preference not found")
    if gender:
        match_pref.gender = gender
    if start_weight:
        match_pref.start_weight = start_weight
    if end_weight:
        match_pref.end_weight = end_weight
    if max_location_distance_miles:
        match_pref.max_location_distance_miles = max_location_distance_miles
    db.commit()
    db.refresh(match_pref)
    return match_pref
def get_match_preference(db:Session,user_id:int):
    match_pref = db.query(MatchPreference).filter(MatchPreference.user_id==user_id).first()
    return match_pref
