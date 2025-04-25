# from app.db.database
from sqlalchemy.orm import Session
from app.db.crud.range_crud import get_availability_ranges_user
from app.db.models.avalrange import AvailabilityRange,DayOfWeek
from sqlalchemy import and_
import json
def match_users(db:Session,user_id:int):
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
    for day in DayOfWeek: # get all the days avaliable + list of aval ranges
        day_ranges = db.query(AvailabilityRange).filter(and_(AvailabilityRange.user_id==user_id,AvailabilityRange.day_of_week==day.value)).all()
        if(len(day_ranges)>=1):
            user_aval_days.append(day.value)
            user_aval_ranges.append(day_ranges)
    for i in range(len(user_aval_ranges)): # sort each day avalranges for comparison later
        user_aval_ranges[i] = sorted(user_aval_ranges[i],key=lambda aval_range: aval_range.start_time)
    


        
    return {"Hello":"World"}
# def same_schedule(db:Session,day_of_week:string,)
