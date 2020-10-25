from attendance_check import db
from attendance_check.models.models import run_query, t_daily_eat_log
from flask import Blueprint, jsonify, request, make_response
'''
t_daily_eat_log = db.Table(
    'daily_eat_log',
    db.Column('date_id', db.ForeignKey('date_mealtime_mapping.id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, info='날짜 인덱스'),
    db.Column('member_id', db.ForeignKey('group_member_info.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True, info='구성원 고유 번호 [ 예) 군번 / 순번 ]')
)
'''
def insert_eatlog(did, mid):
    insert_stmt = t_daily_eat_log.insert().values(date_id=did, member_id=mid)
    db.session.using_bind("master").execute(insert_stmt)
    db.session.commit()
    db.session.flush()

def check_already_logged(did, mid) -> bool:
    row = db.session.using_bind("slave").query(t_daily_eat_log).filter_by(date_id=did, member_id=mid).first()
    if row:
        if row.date_id and row.member_id:
            return True
        else:
            # TODO: raise exception this case
            return True
    return False

def get_full_log() ->  dict:
    full_log = {}
    rows = db.session.using_bind("slave").query(t_daily_eat_log).all()
    for row in rows:
        if not row.date_id in full_log:
            full_log[row.date_id] = []
        full_log[row.date_id].append(row.member_id)
    return full_log

eatlogger = Blueprint('eatlogger', __name__, url_prefix='/eatlogger')
@eatlogger.route('/write/', methods=['POST'])
def write_eatlog():
    content = request.get_json()
    already_logged = run_query(check_already_logged, (content['date_id'], content['member_id']), slave=True)
    if not already_logged:
        run_query(insert_eatlog, (content['date_id'], content['member_id']))
        res = make_response(jsonify({"message": "확인되었습니다."}), 200)
    else:
        res = make_response(jsonify({"message": "이미 기록되있습니다."}), 204)
    return res

@eatlogger.route('/load/', methods=['GET'])
def load_eatlog():
    full_log = run_query(get_full_log, slave=True)
    res = make_response(jsonify(full_log), 200)
    return res