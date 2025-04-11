from fastapi import Depends,APIRouter
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.schemas.community import CommunityCreate
from app.db.crud.community_crud import get_community_by_address,create_community
router = APIRouter()

@router.post("")
def handle_community_request(community_body:CommunityCreate,db: Session = Depends(get_db)):
    community = get_community_by_address(db,community_body.address)
    if community is  None:
        create_community(db,community_body.name,community_body.address,community_body.latitude,community_body.longitude)
        community =get_community_by_address(db,community_body.address)
    return community