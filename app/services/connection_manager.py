from fastapi import WebSocket
from typing import Dict
class ChatConnectionManager: # key is user_id
    def __init__(self):
        self.active_connections : Dict[str,WebSocket]= {}
    async def connect(self,websocket: WebSocket,key):
        await websocket.accept()
        self.active_connections[key] = websocket
    async def send_personal_message(self,message:str,websocket:WebSocket):
        await websocket.send_text(message)
    

        


