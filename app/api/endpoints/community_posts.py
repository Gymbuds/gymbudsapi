from fastapi import Depends,APIRouter
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.schemas.post import CommunityPostCreate,CommunityPostUpdate,CommunityPostResponse
from app.db.crud.com_post_crud import create_post,update_post,delete_post
from app.core.security import get_current_user 
from app.db.models.user import User
router=APIRouter()

@router.post("", response_model=CommunityPostResponse)
def create_community_post(
    post: CommunityPostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_post(db, current_user.id, post)

@router.patch("/{post_id}", response_model=CommunityPostResponse)
def update_community_post(
    post_id: int,
    post_update: CommunityPostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_post(db, current_user.id, post_id, post_update)

@router.delete("/{post_id}")
def delete_community_post(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return delete_post(db, current_user.id, post_id)