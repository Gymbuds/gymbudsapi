from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.models.user import User
from app.db.models.match_result import MatchResult

def create_match(db:Session, user_id: int, matched_user_id:int)->MatchResult:
    if user_id == matched_user_id:
        raise HTTPException(status_code=400, detail="Cannot match with yourself")
    
    matched_user = db.query(User).filter(User.id == matched_user_id).first()
    if not matched_user:
        raise HTTPException(status_code=404, detail="Matched user does not exist.")
    
    user1_id, user2_id = sorted([user_id,matched_user_id])
    
    existing_match = db.query(MatchResult).filter_by(user_id1=user1_id, user_id2=user2_id).first()
    if existing_match:
        raise HTTPException(status_code=400, detail="Match already exists.")
    
    match = MatchResult(user_id1 = user1_id, user_id2 = user2_id)
    db.add(match)
    db.commit()
    db.refresh(match)
    return match

def delete_match(db:Session, user_id:int, match_id:int)->None:
    match = db.query(MatchResult).filter(MatchResult.id==match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    if user_id not in [match.user_id1,match.user_id2]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this match")
    
    db.delete(match)
    db.commit()

def get_matches(db:Session, user_id:int):
    matches = db.query(MatchResult).filter((MatchResult.user_id1==user_id)|(MatchResult.user_id2==user_id)).all()
    return matches