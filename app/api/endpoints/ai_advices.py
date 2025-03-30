from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.advice import AIAdviceBase, AIAdviceResponse 
from app.db.crud.advice_crud import create_advice,get_advices,get_advice_by_id
from app.db.models.user import User
from app.core.security import get_current_user
from typing import List
router = APIRouter()

# Create AI Advice
@router.post("", response_model=AIAdviceResponse) 
async def create_ai_advice(advice: AIAdviceBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await create_advice(db, current_user, advice)
@router.get("", response_model=List[AIAdviceResponse])
def get_ai_advices(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    res =  get_advices(db,current_user)
    return res
@router.get("/{advice_id}", response_model=AIAdviceResponse) 
def get_ai_advice_by_id(advice_id:int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return get_advice_by_id(db,advice_id)
