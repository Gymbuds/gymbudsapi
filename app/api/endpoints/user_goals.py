
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import get_current_user
from app.db.crud.user_goals_crud import (
    add_multiple_user_goals,
    get_user_goals
)
from app.schemas.user import UserGoalsUpdate
from app.db.models.user_goal import GymGoal
from app.db.models.user import User

router = APIRouter()

@router.post("/goals")
def add_goals(
    goals_update: UserGoalsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return add_multiple_user_goals(db=db, user_id=current_user.id, goals=goals_update.goals)

@router.get("/goals")
def get_goals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_goals(db=db, user_id=current_user.id)