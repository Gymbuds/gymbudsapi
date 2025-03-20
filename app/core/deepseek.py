from openai import OpenAI
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from app.schemas.advice import AIAdviceType
from app.db.crud.workout_log_crud import get_workout_logs_by_user_latest
from app.db.models.user import User
from app.db.database import db

load_dotenv()


def deepSeekChat(workout_type:str,user:User,db:Session):
    client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
    user_workouts = get_workout_logs_by_user_latest(db=db,user_id=user.id,latest_amt_days=30)
    # user_preferences = 
    # if workout_type==AIAdviceType.WORKOUT_ADVICE:
    #     messages = [{"role":"system","content":"You are a fitness coach analyzing a user's workout logs and preferences."
    #                 "Based on the following information, provide personalized workout advice to help the user achieve their fitness goals."},
    #                 {"role": "user", "content": "User Preferences: {user_preferences}"},
    #     ]
    # response = client.chat.completions.create(
    #     model="deepseek-chat",
    #     messages=[
    #         {"role": "system", "content": "You are a helpful assistant"},
    #         {"role": "user", "content": "please add 1+1"},
    #     ],
    #     stream=False
    # )
    # print(response.choices[0])
    # print("content",response.choices[0].message.content)
    


