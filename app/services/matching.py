# from app.db.database
from sqlalchemy.orm import Session
from app.db.crud.range_crud import get_availability_ranges_user
from app.db.models.avalrange import AvailabilityRange,DayOfWeek
from sqlalchemy import and_
import json
def get_similar_schedules_for_user(db:Session,user_id:int):
    # match schedules
    # interval manipulation 
   # monday  [1,2] [2,5]  vs [2,5] [ 5,6]

    # require schedule to be set up for matching -> ?   
    # filter only people that are avaliable same day  i am avaliable, schedule set up 
    # say for example my Monday: [1,5][7,10] vs  someone elses monday [2,5][6,10]
    # https://leetcode.com/problems/merge-intervals/description/  o(nlogn)
    # sort both 
    # goal alignment, gender [pref], weight [ pref], gy mtenure (begin,inter,advance) [pref],preferred gym 
    # point system  (100 ) more points = more compat
    user_aval_days = []
    user_aval_ranges = []
    potential_similar_schedule_users = set()
    for day in DayOfWeek: # get all the days avaliable + list of aval ranges
        day_ranges = db.query(AvailabilityRange).filter(and_(AvailabilityRange.user_id==user_id,AvailabilityRange.day_of_week==day.value)).all()
        if(len(day_ranges)>=1):
            user_aval_days.append(day.value)
            user_aval_ranges.append(day_ranges)
    for i in range(len(user_aval_ranges)): # sort each day avalranges for comparison later
        user_aval_ranges[i] = sorted(user_aval_ranges[i],key=lambda aval_range: aval_range.start_time)
    for i in range(len(user_aval_days)): # get all other user IDs who have availability on this day
        other_user_ids = db.query(AvailabilityRange.user_id).filter(
            and_(
                AvailabilityRange.user_id != user_id,
                AvailabilityRange.day_of_week == user_aval_days[i]
            )
        ).distinct().all()
        for (other_user_id,) in other_user_ids:
 
            other_ranges = db.query(AvailabilityRange).filter(
                and_(
                    AvailabilityRange.user_id == other_user_id,
                    AvailabilityRange.day_of_week == user_aval_days[i]
                )
            ).order_by(AvailabilityRange.start_time).all()
            # Compare their time ranges to the current user's ranges
            for other_range in other_ranges:
                for user_range in user_aval_ranges[i]:  #  user ranges for curr day
                    if user_range.start_time <= other_range.start_time and user_range.end_time >= other_range.end_time:
                        potential_similar_schedule_users.add(other_user_id)
                        break  # one match is enough, move to next user
                else:
                    continue
                break

        
        
    return potential_similar_schedule_users
def match_users(db:Session,user_id:int):
    valid_users = get_similar_schedules_for_user(db=db,user_id=user_id) # set of user_ids of eligible users
