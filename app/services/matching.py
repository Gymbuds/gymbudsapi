# from app.db.database
from sqlalchemy.orm import Session
def match_users(db:Session,user_id:int):
    # match schedules
    # interval manipulation 
    # require schedule to be set up for matching -> ? 
    # filter only people that are avaliable same day  i am avaliable, schedule set up 
    # say for example my Monday: [1,5][7,10] vs  someone elses monday [2,5][6,10]
    # https://leetcode.com/problems/merge-intervals/description/  o(nlogn)
    # sort both 
    # Schedule alignment , goal alignment, gender, 
