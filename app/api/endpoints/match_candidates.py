from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.match_candidate import MatchCandidate
from app.db.models.user import User
from app.schemas.match import CandidateCreate,StatusUpdate
from app.db.crud.candidate_crud import create_candidate,get_all_candidates,update_candidate_status
from app.core.security import get_current_user
from typing import List

router = APIRouter()



# @router.post("/", response_model=dict)
# def create_match_candidate(data: CandidateCreate, db: Session = Depends(get_db)):
#     create_candidate(
#         db,
#         user_id=data.user_id,
#         candidate_user_id=data.candidate_user_id,
#         score=data.score,
#     )
#     return {"message": "Candidate created"}

@router.get("")
def get_candidates(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return get_all_candidates(db=db, user_id=current_user.id)

@router.put("/status", response_model=dict)
def update_match_status(data: StatusUpdate, db: Session = Depends(get_db)):
    update_candidate_status(
        db,
        match_candidate_id=data.match_candidate_id,
        status=data.status,
    )
    return {"message": "Status updated"}
