from openai import OpenAI
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from app.schemas.advice import AIAdviceType
from app.db.crud.workout_log_crud import get_workout_logs_by_user_latest
from app.db.crud.health_data_crud import get_health_data_by_user_latest
from app.db.models.user import User
load_dotenv()


async def deepSeekChat(db: Session, workout_type: str, user: User, use_health_data: bool):
    client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
    user_workouts,workout_earliest,workout_latest= get_workout_logs_by_user_latest(db=db,user_id=user.id,latest_amt_days=30)
    parsed_user_workouts = []
    parsed_health_datas = []
    for workout in user_workouts:
        workout_dict = workout.__dict__
        workout_dict.pop('_sa_instance_state', None) # notn eeded
        if 'exercise_details' in workout_dict:
            workout_dict['exercise_details'] = [
                exercise.__dict__ for exercise in workout_dict['exercise_details']
            ]
        parsed_user_workouts.append(workout_dict)
    
    if (user.skill_level):
        skill_level = user.skill_level.value 
    else:
        skill_level = None
    user_preferences  = {
        "name": user.name,
        "preferred_workout_goals" : user.preferred_workout_goals if user.preferred_workout_goals else None,
        "age": user.age if user.age else  None,
        "skill_level":  skill_level,
        "weight": user.weight if user.weight else  None,
    }
    if use_health_data:
        health_datas = get_health_data_by_user_latest(db, user.id, 30)
        for health_data in health_datas:
            health_data_dict = health_data.__dict__
            health_data_dict.pop('_sa_instance_state', None)  
            health_data_dict = {key: value for key, value in health_data_dict.items() if value != 0}
            parsed_health_datas.append(health_data_dict)
    ai_preferences = """If there is a variable with the value 'None', ignore it. 
                    This will be a singular response don't say a message allowing the user to respond
                    This will go into a react native text box format the response to fit as text seperated by paragraphs or sections with headers
                    Do not mention the user's name, workout type, or any titles—just provide the analysis immediately.  
                    Do not include any introductions, summaries, or acknowledgments.  
                    Only output the core advice and insights with no extra context.
                    """
    stringed_parsed_health_datas = f", User Health Data {parsed_health_datas}" if use_health_data else ""
    user_info = f"User's Preferences and Details: {user_preferences}, User's Workout Logs: {parsed_user_workouts}{stringed_parsed_health_datas}"
    if workout_type==AIAdviceType.WORKOUT_ADVICE:
        messages = [{"role":"system","content":f"""You are a fitness coach analyzing a user's workout logs and preferences.
                    Based on the following information, provide personalized workout advice to help the user achieve their fitness goals. 
                    {ai_preferences}"""},
                    {"role": "user", "content": f"{user_info}"},
        ]
    if workout_type==AIAdviceType.WORKOUT_OPTIMIZATION:
        messages = [{"role":"system","content":f"""You are a fitness coach analyzing a user's workout logs and preferences.
                    "Based on the following information, provide personalized advice on how the user can optimize their workouts for better results.
                    {ai_preferences}"""},
                    {"role": "user", "content": f"{user_info}"},
        ]
    if workout_type==AIAdviceType.GOAL_ALIGNMENT:
        messages = [{"role":"system","content":f"""You are a fitness coach analyzing a user's workout logs and preferences."
                    "Based on the following information, analyze how well the user's workouts align with their goals and provide personalized advice."
                    {ai_preferences}"""},
                    {"role": "user", "content": f"{user_info}"},
        ]
    if workout_type==AIAdviceType.MUSCLE_BALANCE:
        messages = [{"role":"system","content":f"""You are a fitness coach analyzing a user's workout logs and preferences."
                    "Based on the following information, analyze how well the user's current workout routine balances their muscle groups in relation to their fitness goals, body type, and preferences. Provide personalized advice on how they can improve their muscle balance to achieve better overall fitness and alignment with their specific needs."
                    {ai_preferences}"""},
                    {"role": "user", "content": f"{user_info}"},
        ]
    if workout_type == AIAdviceType.RECOVERY_ANALYSIS:
        messages = [{"role":"system","content":f"""You are a fitness coach analyzing a user's workout logs and preferences."
                    "Based on the following information, evaluate the user's data  and provide personalized advice on how to optimize their rest, sleep, and recovery techniques to enhance performance and prevent overtraining. "
                    {ai_preferences}"""},
                    {"role": "user", "content": f"{user_info}"},
        ]
    if workout_type == AIAdviceType.PERFORMANCE_TRENDS:
        messages = [{"role":"system","content":f"""You are a fitness coach analyzing a user's workout logs and preferences."
                    "Based on the following information, Analyze the user's workout logs to identify performance trends over time, highlighting strengths, weaknesses, and areas for improvement."
                    {ai_preferences}"""},
                    {"role": "user", "content": f"{user_info}"},
        ]
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        stream=False
    )
    return response.choices[0].message.content,workout_earliest,workout_latest
    


