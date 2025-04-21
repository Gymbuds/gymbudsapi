from fastapi import Depends,APIRouter
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.schemas.community import CommunityCreate
from app.db.models.user import User
from app.db.crud.community_crud import get_community_by_address,create_community,user_join_community,user_leave_community,get_community_users
from app.core.security import get_current_user

router = APIRouter()

@router.post("")
def handle_community_request(community_body:CommunityCreate,db: Session = Depends(get_db)):
    community = get_community_by_address(db,community_body.address)
    if community is  None:
        create_community(db,community_body.name,community_body.address,community_body.latitude,community_body.longitude,community_body.places_id)
        community =get_community_by_address(db,community_body.address)
    return community
@router.post("/{community_id}")
def join_community(community_id,db:Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return user_join_community(community_id=community_id,user_id=current_user.id,db=db)

@router.delete("/{community_id}")
def leave_community(community_id,db:Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return user_leave_community(community_id=community_id,user_id=current_user.id,db=db)

@router.get("/{community_id}")
def get_community_members(community_id,db:Session = Depends(get_db)):
    return get_community_users(db=db, community_id=community_id)

@router.patch("/{community_id}/prefer")
def set_preferred_community(community_id:int, db:Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return set_preferred_community_by_id(db,community_id,current_user.id)