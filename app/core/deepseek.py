from openai import OpenAI
import os
from dotenv import load_dotenv
from app.schemas.advice import AIAdviceType
from app.db.crud.workout_log_crud import get_workout_logs_by_user_latest
load_dotenv()


def deepSeekChat(workout_type:str):
    client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
    print()
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
    


