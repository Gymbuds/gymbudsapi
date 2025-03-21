from sqlalchemy.orm import Session
from app.db.models.ai_advice import AIAdvice
from app.schemas.advice import AIAdviceBase
from app.core.deepseek import deepSeekChat
from app.db.models.user import User
def create_advice(db: Session, user: User, advice: AIAdviceBase) -> AIAdvice:

    deepSeekChat(db=db,workout_type=advice.advice_type,user=user)
    
    ai_response = "test"
    db_advice = AIAdvice(
        user_id=user.id,
        ai_feedback = ai_response,
        advice_type=advice.advice_type,
    )
    db.add(db_advice)
    db.commit()
    db.refresh(db_advice)
    return db_advice