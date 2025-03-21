from openai import OpenAI
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from app.schemas.advice import AIAdviceType
from app.db.crud.workout_log_crud import get_workout_logs_by_user_latest
from app.db.models.user import User
import json
load_dotenv()


def deepSeekChat(db:Session,workout_type:str,user:User,):
    client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
    user_workouts = get_workout_logs_by_user_latest(db=db,user_id=user.id,latest_amt_days=30)
    parsed_user_workouts = []
    for workout in user_workouts:
        workout_dict = workout.__dict__
        workout_dict.pop('_sa_instance_state', None) # notn eeded
        if 'exercise_details' in workout_dict:
            workout_dict['exercise_details'] = [
                exercise.__dict__ for exercise in workout_dict['exercise_details']
            ]
        parsed_user_workouts.append(workout_dict)
    
    user_preferences  = {
        "name": user.name,
        "preferred_workout_goals" :user.preferred_workout_goals,
        "age": user.age,
        "skill_level":user.skill_level
    }
    #health_data = some_func()
    if workout_type==AIAdviceType.WORKOUT_ADVICE:
        messages = [{"role":"system","content":"You are a fitness coach analyzing a user's workout logs and preferences."
                    "Based on the following information, provide personalized workout advice to help the user achieve their fitness goals."},
                    {"role": "user", "content": f"User Preferences: {user_preferences},User Workout Logs: {parsed_user_workouts}"},
        ]
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "please add 1+1"},
        ],
        stream=False
    )
    print(response.choices[0])
    # print("content",response.choices[0].message.content)
    


