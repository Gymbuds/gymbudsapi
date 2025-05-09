from sqlalchemy.orm import Session
from app.db.models.message import Message
from app.db.models.user import User
from app.db.crud.user_crud import get_user_info_by_id

def create_message(db:Session,chat_id:int,user_id:int,content:str):