from flask import Blueprint, jsonify, make_response
from attendance_check import db
from attendance_check.models.models import run_query, DateMealtimeMapping
'''
class DateMealtimeMapping(db.Model):
    __tablename__ = 'date_mealtime_mapping'

    id = db.Column(db.Integer, primary_key=True, info='인덱스')
    korean_date = db.Column(db.Date, nullable=False, info='날짜(20200101)')
    meal_time = db.Column(db.Enum('breakfast', 'lunch', 'dinner'), nullable=False, info='식사시간 ( 1~3 : 아침, 점심, 저녁 )')
    members = db.relationship('Account', secondary='daily_eat_log', backref='date_mealtime_mappings')

'''
date = Blueprint('date', __name__, url_prefix='/date')

def check_date_exist(date, meal_time):
    row = db.session.using_bind("slave").query(DateMealtimeMapping).filter_by(korean_date=date, meal_time=meal_time).first()
    if row:
        return row.id
    else:
        return -1

@date.route('/<date_text>', methods=['GET'])
def get_date_id(date_text):
    date, meal_time = date_text.split("_")
    mid = run_query(check_date_exist, (date, meal_time), slave=True)
    if mid == -1:
        return jsonify(
            error_id = 1,
            msg = "식사 시간이 등록되지 않았습니다. 관리자에게 문의하세요"
        ), 404
    res = make_response(jsonify({"date_id": mid}), 200)
    return res