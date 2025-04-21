from sqlalchemy.orm import Session
from app.db.models.community import Community

def create_community(db:Session,name:str,address:str,latitude:float,longitude:float):
    community = Community(name=name,address=address,latitude=latitude,longitude=longitude)
    db.add(community)
    db.commit()
    db.refresh(community)
    return community
def get_community_by_address(db:Session,address:str):
    return db.query(Community).filter(Community.address == address).first()
    