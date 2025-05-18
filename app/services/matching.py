# from app.db.database
from sqlalchemy.orm import Session
from app.db.crud.range_crud import get_availability_ranges_user
from app.db.models.avalrange import AvailabilityRange, DayOfWeek
from app.db.models.user import User
from app.db.crud.user_crud import get_user_info_by_id, get_multiple_users_info_by_ids
from app.db.crud.community_crud import get_user_preferred_gym, get_multiple_users_preferred_gym_ids
from app.db.crud.match_preferences_crud import get_match_preference
from app.db.crud.user_goals_crud import get_list_user_goals_as_set,get_multiple_users_goals_as_set
from app.db.crud.candidate_crud import create_candidate
from app.db.models.match_preferences import MatchPreference
from sqlalchemy import and_
from math import radians,cos,sin,asin,sqrt

import json

def get_similar_schedules_for_user(db: Session, user_id: int):
    # match schedules
    # interval manipulation 
    # monday [1,2] [2,5] vs [2,5] [5,6]

    # require schedule to be set up for matching -> ?   
    # filter only people that are available same day I am available, schedule set up 
    # say for example my Monday: [1,5][7,10] vs someone else's Monday [2,5][6,10]
    # https://leetcode.com/problems/merge-intervals/description/  o(nlogn)
    # sort both 

    user_aval_days = []    # list of days where user has availability
    user_aval_ranges:AvailabilityRange = []  # corresponding sorted list of user's time ranges per day
    potential_similar_schedule_users = set()  # store matched user ids

    for day in DayOfWeek:  # get all the days available + list of availability ranges
        day_ranges = db.query(AvailabilityRange).filter(
            and_(
                AvailabilityRange.user_id == user_id,
                AvailabilityRange.day_of_week == day.value
            )
        ).all()
        if day_ranges:
            user_aval_days.append(day.value)
            user_aval_ranges.append(sorted(day_ranges, key=lambda r: r.start_time))  # sort each day's ranges

    for i in range(len(user_aval_days)):  # for each available day
        other_user_ids = db.query(AvailabilityRange.user_id).filter(
            and_(
                AvailabilityRange.user_id != user_id,
                AvailabilityRange.day_of_week == user_aval_days[i]
            )
        ).distinct().all()  # get all other user IDs who have availability on this day

        for (other_user_id,) in other_user_ids:
            other_ranges = db.query(AvailabilityRange).filter(
                and_(
                    AvailabilityRange.user_id == other_user_id,
                    AvailabilityRange.day_of_week == user_aval_days[i]
                )
            ).order_by(AvailabilityRange.start_time).all()

            # Compare their time ranges to the current user's ranges
            for other_range in other_ranges:
                for user_range  in user_aval_ranges[i]:  # user ranges for current day
                    if (user_range.start_time <= other_range.start_time and user_range.end_time >= other_range.end_time) or (user_range.start_time>=other_range.start_time and user_range.end_time<=other_range.end_time):
                        potential_similar_schedule_users.add(other_user_id)
                        break  # one match is enough, move to next user
                else:
                    continue
                break

    return potential_similar_schedule_users

def distance_between_two_points(lat1:float,lat2:float,long1:float,long2:float): # Haversine formula
    R = 6371 
    delta_lat = radians(lat2 - lat1)
    delta_lon = radians(long2 - long1)
    a = sin(delta_lat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(delta_lon/2)**2
    c = 2 * asin(sqrt(a))
    return R*c * 0.621371 # kms -> miles
def compare_user_ids_distance(db:Session,user_id:int,user_ids:set,user_match_pref: MatchPreference):
    users_info = get_multiple_users_info_by_ids(db=db, user_ids=user_ids)
    main_user_info = get_user_info_by_id(db=db,user_id=user_id)
    res = set ()
    for user in users_info: 
        distance_miles = distance_between_two_points(main_user_info.latitude,user.latitude,main_user_info.longitude,user.longitude)
        if distance_miles<= user_match_pref.max_location_distance_miles:
            res.add(user.id)
    return res

def match_users(db: Session, user: User):
    intial_schedule_check = get_similar_schedules_for_user(db=db, user_id=user.id)  # set of user_ids of eligible users
    # distance_checked_user_ids = 
    user_match_preferences = get_match_preference(db=db,user_id=user.id)
    distance_checked_user_ids =  compare_user_ids_distance(db=db,user_id=user.id,user_ids=intial_schedule_check,user_match_pref=user_match_preferences)
    user_score_id = {}  #  user id ->
    if not intial_schedule_check:
        return []

    # point system more points = better fit 
    # goal alignment, gender [pref], weight [pref], gym tenure (beginner, intermediate, advanced) [pref], preferred gym 

    user_pref_gym = get_user_preferred_gym(db=db, user_id=user.id)

    # batch fetch potential users' info and preferred gyms
    user_ids = list(distance_checked_user_ids) # prevents different user_ids 
    potential_users_info = get_multiple_users_info_by_ids(db=db, user_ids=user_ids)
    potential_users_gym = get_multiple_users_preferred_gym_ids(db=db, user_ids=user_ids)
    potential_users_goals= get_multiple_users_goals_as_set(db=db,user_ids=user_ids)
    user_goals = get_list_user_goals_as_set(db=db,user_id=user.id)
    WEIGHTS = {
        "skill": 5,
        "gender": 3,
        "age": 3,
        "weight": 8,
        "goal": 4,
        "gym": 20,
    }

    for potential_user in potential_users_info:
        potential_user_id = potential_user.id
        score = 0

        if not potential_user:
            continue  # if user info is missing, skip
        
        # skill level matching
        if user.skill_level and potential_user.skill_level and user.skill_level == potential_user.skill_level:
            score += WEIGHTS["skill"]
        if user.age and potential_user.age and (user_match_preferences.start_age<=potential_user.age and user_match_preferences.end_age>=potential_user.age):
            score+= WEIGHTS["age"]
        # gender matching
        if user.gender and potential_user.gender and (user_match_preferences.gender == potential_user.gender or user_match_preferences.gender == "BOTH"):
            score += WEIGHTS["gender"]

        # weight proximity  needs to be within user pref  ppounds
        if user.weight and potential_user.weight and potential_user.weight <= user_match_preferences.end_weight and potential_user.weight >= user_match_preferences.start_weight:
            score += WEIGHTS["weight"]
        
        # Preferred gym matching
        if user_pref_gym and potential_user_id in potential_users_gym and user_pref_gym.id == potential_users_gym[potential_user_id]:
            score += WEIGHTS["gym"]

        # print(user_goals.intersection(potential_users_goals[potential_user_id]))
        if user_goals and potential_user_id in potential_users_goals:
            score+= WEIGHTS["goal"] * len(user_goals.intersection(potential_users_goals[potential_user_id]))
        if potential_user_id not in user_score_id:
            user_score_id[potential_user_id] = score
        
    
    create_candidate(db=db,user_id=user.id,candidate_scores=user_score_id)
    return user_score_id
