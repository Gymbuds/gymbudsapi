from sqlalchemy.orm import Session
from app.db.models.match_candidate import MatchCandidate, Status
from fastapi import HTTPException,status
from app.db.crud.match_crud import create_match
from sqlalchemy import and_
def create_candidate(db: Session, user_id: int, candidate_scores: dict[int, float]):
    if not candidate_scores:
        return

    candidate_user_ids = list(candidate_scores.keys())

    existing_candidates = db.query(MatchCandidate).filter(
        MatchCandidate.user_id == user_id,
        MatchCandidate.candidate_user_id.in_(candidate_user_ids)
    ).all()

    existing_map = {mc.candidate_user_id: mc for mc in existing_candidates}

    for candidate_user_id, score in candidate_scores.items():
        if candidate_user_id in existing_map:
            existing_map[candidate_user_id].score = score
        else:
            new_candidate = MatchCandidate(
                user_id=user_id,
                candidate_user_id=candidate_user_id,
                score=score,
                status=Status.PENDING
            )
            db.add(new_candidate)

    db.commit()
def get_all_candidates(db:Session,user_id:int):
    candidate = db.query(MatchCandidate).filter(MatchCandidate.user_id==user_id).all()
    return candidate
def update_candidate_status(db:Session,match_candidate_id:int,status:str):
    status_enum = Status(status.upper())
    match_candidate = db.query(MatchCandidate).filter(MatchCandidate.id==match_candidate_id).first()
    mutable_status = status_enum
    opposite_candidate = db.query(MatchCandidate).filter(and_(MatchCandidate.user_id==match_candidate.candidate_user_id,MatchCandidate.candidate_user_id==match_candidate.user_id)).first()
    if opposite_candidate and opposite_candidate.status==Status.REJECTED:
        mutable_status = Status.REJECTED
    elif opposite_candidate and opposite_candidate.status == Status.ACCEPTED and status_enum==Status.ACCEPTED:
        mutable_status = Status.ACCEPTED
        create_match(db, match_candidate.user_id, match_candidate.candidate_user_id)
    match_candidate.status = mutable_status
    db.commit()
    db.refresh(match_candidate)

def delete_pending_candidates_for_id(db:Session,user_id:int):
    candidates = db.query(MatchCandidate).filter(and_(MatchCandidate.user_id==user_id),(MatchCandidate.status=="PENDING")).all()
    if not candidates:
        raise HTTPException(status_code=404, detail="candidates not found")
    for can in candidates:
        db.delete(can)
    db.commit()
    
