
""" CRUD for Messages"""
from sqlalchemy.orm import Session

from fastapi import status,HTTPException
from app.db.models.message import Message
from app.db.crud.user_crud import get_user_info_by_id



def create_message(db:Session,chat_id:int,user_id:int,content:str,image_url:str):
    """
    Create a new message and add it to the database.

    Parameters:
    - db (Session): The database session.
    - chat_id (int): The ID of the chat.
    - user_id (int): The ID of the user.
    - content (str): The content of the message.

    Raises:
    - HTTPException: If the user with the given ID is not found.

    Returns:
    - None
    """
    user =  get_user_info_by_id(db=db,user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    new_message = Message(
        chat_id=chat_id,
        sender_id=user_id,
        content=content,
        image_url=image_url
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    print(new_message)
    return new_message
def get_messages_for_chat(db:Session,chat_id:int):
    """
    Gets all messages for a particular chat

    Parameters:
    - db (Session): The database session.
    - chat_id (int) :ID of chat
    """
    messages = db.query(Message).filter(Message.chat_id==chat_id).all()
    
    return messages
def get_message(db: Session, message_id: int):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    return message