from fastapi import Depends,APIRouter, HTTPException,status
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.db.models.user import User
from app.db.crud.message_crud import get_messages_for_chat
from app.core.security import get_current_user
from app.db.crud.chat_crud import get_chat,create_chat
from typing import List
router=APIRouter()

@router.get("/{user_id}")
def get_messages(user_id:int,db:Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    chat = get_chat(db=db,user_id_1=current_user.id,user_id_2=user_id)
    if not chat:
        chat = create_chat(db=db,user_id_1=current_user.id,user_id_2=user_id)
    return get_messages_for_chat(db=db,chat_id=chat.id)
