from sqlalchemy.orm import Session
from app.db.models.ai_advice import AIAdvice
from app.schemas.advice import AIAdviceBase,AIAdviceResponse
from app.core.deepseek import deepSeekChat
from app.db.models.user import User
async def create_advice(db: Session, user: User, advice: AIAdviceBase) -> AIAdvice:
    ai_response = await deepSeekChat(db=db,workout_type=advice.advice_type,user=user,use_health_data=advice.health_data)
    print(ai_response)
    db_advice = AIAdvice(
        user_id=user.id,
        ai_feedback = ai_response,
        advice_type=advice.advice_type,
    )
    db.add(db_advice)
    db.commit()
    db.refresh(db_advice)
    return db_advice
def get_advices(db:Session,user:User):
    ai_advices = db.query(AIAdvice).filter(AIAdvice.user_id == user.id).all()
    print(ai_advices)
    return [AIAdviceResponse(
        id=advice.id,
        advice_type=advice.advice_type,
        ai_feedback=advice.ai_feedback,
        user_id = advice.user_id,
        created_at = advice.created_at,
    ) for advice in ai_advices]

def get_advice_by_id(db:Session,advice_id: int):
    ai_advice = db.query(AIAdvice).filter(AIAdvice.id==advice_id).first()
    return AIAdviceResponse(
        id=ai_advice.id,
        advice_type=ai_advice.advice_type,
        ai_feedback=ai_advice.ai_feedback,
        user_id = ai_advice.user_id,
        created_at = ai_advice.created_at,
    )
