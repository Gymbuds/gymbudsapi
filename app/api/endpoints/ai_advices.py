from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.advice import AIAdviceBase, AIAdviceResponse 
from app.db.crud.advice_crud import create_advice
from app.db.models.user import User
from app.core.security import get_current_user

router = APIRouter()

# Create AI Advice
@router.post("", response_model=AIAdviceResponse) 
async def create_ai_advice(advice: AIAdviceBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await create_advice(db, current_user, advice)