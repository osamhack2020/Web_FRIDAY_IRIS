from models import get_session
from models import run_query
from models.models import DateMealtimeMapping

def select_date_id(datetime, mealtime):
    row = get_session("r").query(DateMealtimeMapping).filter_by(korean_date=datetime, meal_time=mealtime).first()
    if row:
        return row.id
    else:
        return -1
        
def get_date_id(datetime, mealtime):
    _id = run_query(select_date_id, (datetime, mealtime))
    if _id != -1:
        return _id
    else:
        return -1

def find_date_id(date_string):
    MEAL = ["breakfast", "lunch", "dinner"]
    datetime, mealtime = date_string.split("_")
    _id = get_date_id(datetime, MEAL[int(mealtime)-1])
    if _id != -1:
        return _id
    else:
        return -1

def insert_mealtime(datetime, mealtime):
    new_mealtime = DateMealtimeMapping(korean_date=datetime, meal_time=mealtime)
    sess = get_session("w")
    sess.add(new_mealtime)
    sess.commit()

def set_mealtime(datetime, mealtime):
    run_query(insert_mealtime, (datetime, mealtime))

def set_date_id(date_string):
    MEAL = ["breakfast", "lunch", "dinner"]
    datetime, mealtime = date_string.split("_")
    meal_time = MEAL[int(mealtime)-1]
    set_mealtime(datetime, meal_time)