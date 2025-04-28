from fastapi import Depends, APIRouter
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.schemas.match import MatchResultCreate,MatchResultResponse
from app.db.crud.match_crud import create_match,delete_match,get_matches
from app.core.security import get_current_user
from app.db.models.user import User
from app.services.matching import match_users
from typing import List
router=APIRouter()

@router.post("", response_model=MatchResultResponse)
def match_result(match_user:MatchResultCreate,db:Session=Depends(get_db), current_user:User=Depends(get_current_user)):
    return create_match(db, current_user.id,match_user.matched_user_id)

@router.delete("/{match_id}")
def remove_match(match_id:int, db:Session=Depends(get_db), current_user:User=Depends(get_current_user)):
    delete_match(db, current_user.id, match_id)
    return {"sucess": "Match deleted"}

@router.get("", response_model=List[MatchResultResponse])
def get_user_matches(db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    return get_matches(db, current_user.id)

@router.post("/find-match")
def test_match(db:Session = Depends(get_db),current_user :User = Depends(get_current_user)):
    return match_users(db=db,user= current_user)