from sqlalchemy.orm import Session
from app.db.models.match_candidate import MatchCandidate, Status
from sqlalchemy import and_
def create_candidate(db:Session,user_id:int,candidate_user_id:int,score:int):
    new_candidate = MatchCandidate(user_id=user_id,candidate_user_id=candidate_user_id,score=score,status=Status.PENDING)
    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)
def get_all_candidates(db:Session,user_id:int):
    candidate = db.query(MatchCandidate).filter(MatchCandidate.user_id==user_id).all()
    return candidate
def update_candidate_status(db:Session,match_candidate_id:int,status:str):
    match_candidate = db.query(MatchCandidate).filter(MatchCandidate.id==match_candidate_id).first()
    mutable_status = status
    opposite_candidate = db.query(MatchCandidate).filter(and_(MatchCandidate.user_id==match_candidate.candidate_user_id,MatchCandidate.candidate_user_id==match_candidate.user_id)).first()
    if opposite_candidate and opposite_candidate.status==Status.REJECTED:
        mutable_status = Status.REJECTED
    elif opposite_candidate and opposite_candidate.status == Status.ACCEPTED and status==Status.ACCEPTED:
        mutable_status = Status.ACCEPTED
        # call match result crud to make a match
    match_candidate.status = mutable_status
