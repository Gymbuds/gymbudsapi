from sqlalchemy.orm import Session
from app.db.models.chat import Chat
from app.db.models.user import User
from app.db.models.message import Message
from app.db.crud.user_crud import get_user_info_by_id
from fastapi import status,HTTPException
from sqlalchemy import and_, or_, desc, select, func
from sqlalchemy.sql import nulls_last
from sqlalchemy.orm import aliased

def create_chat(db:Session,user_id_1:int,user_id_2:int):
    
    user_1 = get_user_info_by_id(db=db,user_id=user_id_1)
    user_2 = get_user_info_by_id(db=db,user_id=user_id_2)
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
    return new_chat
def get_chat(db:Session,user_id_1:int,user_id_2:int):
    u1,u2 = sorted([user_id_1,user_id_2])

    chat = db.query(Chat).filter(and_(Chat.user_id1 == u1,Chat.user_id2 == u2)).first()
    
    return chat

def get_user_chats_sorted_by_latest_message(db: Session, user_id: int):
    # Subquery: get latest message per chat
    latest_message_subq = (
        db.query(
            Message.chat_id,
            func.max(Message.timestamp).label("latest_time")
        )
        .group_by(Message.chat_id)
        .subquery()
    )

    # Alias to get full latest message info
    LatestMessage = aliased(Message)

    # Join chat → user → latest message
    results = (
        db.query(
            Chat,
            LatestMessage,
            User
        )
        .outerjoin(latest_message_subq, Chat.id == latest_message_subq.c.chat_id)
        .outerjoin(LatestMessage, and_(
            LatestMessage.chat_id == latest_message_subq.c.chat_id,
            LatestMessage.timestamp == latest_message_subq.c.latest_time
        ))
        .join(User, or_(
            (Chat.user_id1 == user_id) & (User.id == Chat.user_id2),
            (Chat.user_id2 == user_id) & (User.id == Chat.user_id1)
        ))
        .filter(or_(
            Chat.user_id1 == user_id,
            Chat.user_id2 == user_id
        ))
        .order_by(nulls_last(latest_message_subq.c.latest_time.desc()))
        .all()
    )

    response = []
    for chat, latest_message, other_user in results:
        response.append({
            "chat_id": chat.id,
            "last_message_time": latest_message.timestamp if latest_message else None,
            "last_message_id": latest_message.id if latest_message else None,
            "other_user": {
                "id": other_user.id,
                "name": other_user.name,
                "profile_picture": other_user.profile_picture,
            }
        })
    return response
