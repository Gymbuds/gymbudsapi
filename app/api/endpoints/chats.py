from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import get_current_user
from app.db.crud.chat_crud import get_chat,create_chat
from app.db.models.user import User

router = APIRouter()

@router.get("/{user_id}")
def get_chat_for_two_users(user_id:int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user),):
    try:
        chat = get_chat(db=db,user_id_1=current_user.id,user_id_2=user_id)
    except:
        print("Chat not found..Creating chat")
        chat = create_chat(db=db,user_id_1=current_user.id,user_id_2=user_id)
        
    return chat