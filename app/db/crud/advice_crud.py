from sqlalchemy.orm import Session
from app.db.models.ai_advice import AIAdvice
from app.schemas.advice import AIAdviceBase

def create_advice(db: Session, user_id: int, advice: AIAdviceBase) -> AIAdvice:
    db_advice = AIAdvice(
        user_id=user_id,
        ai_feedback=advice.ai_feedback,
        advice_type=advice.advice_type,
    )
    db.add(db_advice)
    db.commit()
    db.refresh(db_advice)
    return db_advice