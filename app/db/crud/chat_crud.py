from sqlalchemy.orm import Session
from app.db.models.chat import Chat
from app.db.models.user import User
from app.db.crud.user_crud import get_user_info_by_id
from fastapi import status,HTTPException
from sqlalchemy import and_

def create_chat(db:Session,user_id_1:int,user_id_2:int):
    user_1 = get_user_info_by_id(db=db,user_id=user_id_1)
    user_2 = get_user_info_by_id(db=db,user_id_2=user_id_2)
    if not user_1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not user_2:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    u1,u2 = sorted([user_id_1,user_id_2])
    new_chat = Chat(
        user_id1=u1,
        user_id2=u2,
    )
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
def get_chat(db:Session,user_id_1:int,user_id_2:int):
    u1,u2 = sorted([user_id_1,user_id_2])

    chat = db.query(Chat).filter(and_(Chat.user_id1 == u1,Chat.user_id2 == u2)).first()
    if not chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return chat



