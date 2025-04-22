from sqlalchemy.orm import Session
from app.db.models.community import Community
from app.db.models.user_community import UserCommunity
from app.db.crud.user_crud import get_user_info_by_id
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
    user_community = UserCommunity(user_id=user_id,community_id=community_id,is_preferred_gym=False)
    db.add(user_community)
    db.commit()
    db.refresh(user_community)
    return user_community

def user_leave_community(db:Session,community_id:int,user_id:int):
    user_community = db.query(UserCommunity).filter(and_(UserCommunity.community_id==community_id, UserCommunity.user_id==user_id)).first()
    db.delete(user_community)
    db.commit()

def get_community_users(db:Session,community_id:int):
    users_communities = db.query(UserCommunity).filter(UserCommunity.community_id==community_id).all()
    users = []
    for user_community in users_communities:
        users.append(get_user_info_by_id(db,user_community.user_id))
    return users

def set_preferred_community_by_id(db:Session,community_id:int,user_id:int):
    user_community = db.query(UserCommunity).filter(and_(UserCommunity.user_id==user_id,UserCommunity.community_id==community_id)).first()
    curr_preferred_gym = db.query(UserCommunity).filter(and_(UserCommunity.user_id==user_id,UserCommunity.is_preferred_gym==True)).first()
    if not user_community:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="connection DNE"
        )
    if not curr_preferred_gym:
        user_community.is_preferred_gym = True
    else:
        curr_preferred_gym.is_preferred_gym = False
        user_community.is_preferred_gym= True
    db.commit()
    if(curr_preferred_gym):
        db.refresh(curr_preferred_gym)
    db.refresh(user_community)
    return user_community
    
def get_user_preferred_gym(db:Session,user_id:int):
    user_community =  db.query(UserCommunity).filter(and_(UserCommunity.user_id==user_id,UserCommunity.is_preferred_gym==True)).first() 

    pref_gym = db.query(Community).filter(Community.id==user_community.community_id).first()

    return pref_gym