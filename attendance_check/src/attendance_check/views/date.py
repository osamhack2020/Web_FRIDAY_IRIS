from flask import Blueprint, jsonify, make_response
from attendance_check import db
from attendance_check.models.models import DateMealtimeMapping
'''
class DateMealtimeMapping(db.Model):
    __tablename__ = 'date_mealtime_mapping'

    id = db.Column(db.Integer, primary_key=True, info='인덱스')
    korean_date = db.Column(db.Date, nullable=False, unique=True, info='날짜(20200101)')
    meal_time = db.Column(db.Enum('breakfast', 'lunch', 'dinner'), nullable=False, info='식사시간 ( 1~3 : 아침, 점심, 저녁 )')

    members = db.relationship('Account', secondary='daily_eat_log', backref='date_mealtime_mappings')

'''
date = Blueprint('date', __name__, url_prefix='/date')

@date.route('/<date_text>', methods=['GET'])
def get_date_id(date_text):
    date, meal_time = date_text.split("_")
    row = DateMealtimeMapping.query.filter_by(korean_date=date, meal_time=meal_time).first()
    if not row:
        return jsonify(
            error_id = 1,
            msg = "식사 시간이 등록되지 않았습니다. 관리자에게 문의하세요"
        ), 404
    res = make_response(jsonify({"date_id": row.id}), 200)
    return res