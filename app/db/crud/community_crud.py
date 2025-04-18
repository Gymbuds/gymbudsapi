from sqlalchemy.orm import Session
from app.db.models.community import Community
from app.db.models.user_community import UserCommunity
from sqlalchemy import and_
from fastapi import HTTPException, status
 
def create_community(db:Session,name:str,address:str,latitude:float,longitude:float,places_id:str):
    community = Community(name=name,address=address,latitude=latitude,longitude=longitude,places_id=places_id)
    db.add(community)
    db.commit()
    db.refresh(community)
    return community
def get_community_by_address(db:Session,address:str):
    return db.query(Community).filter(Community.address == address).first()

def user_join_community(db:Session,community_id:int,user_id:int):
    existing = db.query(UserCommunity).filter_by(user_id=user_id, community_id=community_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is already a member of this community."
        )
    user_community = UserCommunity(user_id=user_id,community_id=community_id)
    db.add(user_community)
    db.commit()
    db.refresh(user_community)
    return user_community

def user_leave_community(db:Session,community_id:int,user_id:int):
    user_community = db.query(UserCommunity).filter(and_(UserCommunity.community_id==community_id, UserCommunity.user_id==user_id)).first()
    db.delete(user_community)
    db.commit()

def get_community_users(db:Session,community_id:int):
    users = db.query(UserCommunity).filter(UserCommunity.community_id==community_id).all()
    return users
