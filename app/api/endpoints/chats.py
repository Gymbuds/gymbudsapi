from fastapi import APIRouter,Depends,WebSocket,WebSocketDisconnect,HTTPException,status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import get_current_user,decode_access_token
from app.db.crud.chat_crud import get_chat,create_chat
from app.schemas.chat import MessageOut
from app.db.models.user import User
from app.db.crud.user_crud import get_user_info_by_id
from fastapi.encoders import jsonable_encoder

from app.db.crud.message_crud import create_message,get_messages_for_chat
from app.services.connection_manager import ChatConnectionManager
from typing import Dict
from sqlalchemy.orm import sessionmaker
from app.db.database import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

router = APIRouter()
active_connections: Dict[str, WebSocket] = {}

@router.get("/{user_id}")
def get_chat_for_two_users(user_id:int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user),):
    try:
        chat = get_chat(db=db,user_id_1=current_user.id,user_id_2=user_id)
    except:
        print("Chat not found..Creating chat")
        chat = create_chat(db=db,user_id_1=current_user.id,user_id_2=user_id)
        
    return chat
@router.websocket("/ws")
async def websocket_endpoint(websocket :WebSocket):
    await websocket.accept()
    db: Session = SessionLocal() 
    user_email = None
    try:
        initial_data = await websocket.receive_json()
        if "type" in initial_data and initial_data["type"]=="user_setup":
            auth_token = initial_data["auth_token"]
            payload = decode_access_token(auth_token)
            curr_user = db.query(User).filter(User.email==payload["sub"]).first()
            user_email = payload["sub"]
            active_connections[user_email] = websocket
        while True:
            data = await websocket.receive_json()
            if data["type"] == "new_message":
                other_user_id = int(data["other_user_id"])
                chat = get_chat(db=db, user_id_1=curr_user.id, user_id_2=other_user_id)

                new_message = create_message(
                    db=db,
                    chat_id=chat.id,
                    user_id=curr_user.id,
                    content=data["content"]
                )
                message_dict = {
                    "type":"new_message",
                    "chat_id": new_message.chat_id,
                    "sender_id": new_message.sender_id,
                    "content": new_message.content,
                    "timestamp": new_message.timestamp
                }
                message_out = MessageOut.model_validate(message_dict)
                message_json = jsonable_encoder(message_out)

                if user_email in active_connections:
                    await active_connections[user_email].send_json({
                        "type": "new_message",
                        "message": message_json
                    })

                await websocket.send_json({
                    "type": "new_message",
                    "message": message_json
                })
                print(active_connections)
    except WebSocketDisconnect:
        print(f"User {user_email} disconnected.")
        if user_email in active_connections:
            del active_connections[user_email]
