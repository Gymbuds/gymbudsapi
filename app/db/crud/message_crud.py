
""" CRUD for Messages"""
from sqlalchemy.orm import Session

from fastapi import status,HTTPException
from app.db.models.message import Message
from app.db.crud.user_crud import get_user_info_by_id



def create_message(db:Session,chat_id:int,user_id:int,content:str):
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
        user_id=user_id,
        content=content
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
def get_messages_for_chat(db:Session,chat_id:int):
    """
    Gets all messages for a particular chat

    Parameters:
    - db (Session): The database session.
    - chat_id (int) :ID of chat
    """
    messages = db.query(Message).filter(Message.chat_id==chat_id).all()
    if not messages:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return messages