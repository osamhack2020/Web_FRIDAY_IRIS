from flask import Blueprint, jsonify, request, make_response
from attendance_check import db
import json
from attendance_check.models.models import GroupMemberInfo, t_daily_eat_log, DateMealtimeMapping, GroupMemberInfo
'''
t_daily_eat_log = db.Table(
    'daily_eat_log',
    db.Column('date_id', db.ForeignKey('date_mealtime_mapping.id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, info='날짜 인덱스'),
    db.Column('member_id', db.ForeignKey('group_member_info.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True, info='구성원 고유 번호 [ 예) 군번 / 순번 ]')
)
'''
eatlogs = Blueprint('eatlogs', __name__, url_prefix='/eatlogs')
@eatlogs.route('/', methods=['POST'])
def write_eatlog():
    content = request.get_json()
    row = GroupMemberInfo.query.with_entities(GroupMemberInfo.name).filter_by(id=content['member_id']).first()
    if not row:
        return make_response(jsonify({"message": "인식 오류, 다시 인식해주세요"}), 404)
    already_exist = db.session.query(t_daily_eat_log).filter_by(date_id=content['date_id'], member_id=content['member_id']).count() > 0
    if not already_exist:
        insert_stmt = t_daily_eat_log.insert().values(date_id=content['date_id'], member_id=content['member_id'])
        db.session.execute(insert_stmt)
        db.session.commit()
        res = make_response(jsonify({"message": row.name + "님 확인되었습니다."}), 200)
    else:
        res = make_response(jsonify({"message": row.name + "님은 이미 기록되있습니다."}), 204)
    return res

@eatlogs.route('/', methods=['GET'])
def load_eatlog():
    rows = db.session.query(t_daily_eat_log).all()
    if not rows:
        return "No Log exists"
    dates = DateMealtimeMapping.query.all()
    dates = {d.id: d.korean_date + " " + d.mealtime for d in dates}
    members = GroupMemberInfo.query.all()
    members = {m.id: m.name for m in members}
    logs = []
    for row in rows:
        logs.append({dates[row.date_id]:members[row.member_id]})
    res = make_response(jsonify(logs), 200)
    return res