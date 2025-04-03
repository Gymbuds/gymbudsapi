from sqlalchemy.orm import Session
from app.db.models.ai_advice import AIAdvice
from app.schemas.advice import AIAdviceBase,AIAdviceResponse
from app.core.deepseek import deepSeekChat
from app.db.models.user import User
from fastapi import HTTPException,status

async def create_advice(db: Session, user: User, advice: AIAdviceBase) -> AIAdvice:
    ai_response,workout_earliest,workout_latest= await deepSeekChat(db=db,workout_type=advice.advice_type,user=user,use_health_data=advice.health_data)
    print(ai_response)
    db_advice = AIAdvice(
        user_id=user.id,
        ai_feedback = ai_response,
        advice_type=advice.advice_type,
        workout_earliest_date = workout_earliest,
        workout_latest_date= workout_latest,
        contains_health_data=advice.health_data
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
        workout_earliest_date = advice.workout_earliest_date,
        workout_latest_date= advice.workout_latest_date,
        contains_health_data=advice.contains_health_data,
    ) for advice in ai_advices]

def get_advice_by_id(db:Session,advice_id: int):
    ai_advice = db.query(AIAdvice).filter(AIAdvice.id==advice_id).first()
    return AIAdviceResponse(
        id=ai_advice.id,
        advice_type=ai_advice.advice_type,
        ai_feedback=ai_advice.ai_feedback,
        user_id = ai_advice.user_id,
        created_at = ai_advice.created_at,
        workout_earliest_date = ai_advice.workout_earliest_date,
        workout_latest_date= ai_advice.workout_latest_date,
        contains_health_data=ai_advice.contains_health_data
    )
def delete_advice_by_id(db:Session,advice_id:int):
    ai_advice = db.query(AIAdvice).filter(AIAdvice.id==advice_id).first()
    if not ai_advice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    db.delete(ai_advice)
    db.commit()
    return {"message":"AI Advice successfully deleted"},ai_advice