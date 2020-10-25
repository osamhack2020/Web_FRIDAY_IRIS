from flask import Blueprint, jsonify
from attendance_check import db
from attendance_check.models.models import run_query, GroupList, GroupMemberInfo

def find_member_info(mid) -> (int, int, str):
    row = db.session.using_bind("slave").query(GroupMemberInfo).filter_by(member_id=mid).first()
    if row:
        return (row.id, row.group_id, row.name)
    else:
        return (-1, -1, '')

def find_group_name(gid) -> str:
    row = db.session.using_bind("slave").query(GroupList).filter_by(id=gid).first()
    if row:
        return row.name
    else:
        return ''

members = Blueprint('members', __name__, url_prefix='/members')

@members.route('/<member_id>', methods=['GET'])
def get_member_info(member_id):
    mid, gid, mname = run_query(find_member_info, ([member_id]), slave=True)
    if mid == -1:
        return jsonify(
            error_id = 1,
            msg = "멤버 정보를 조회할 수 없습니다."
        ), 404
    gname = run_query(find_group_name, ([gid]), slave=True)
    if not gname:
        return jsonify(
            error_id = 2,
            msg = "그룹 정보가 등록되어 있지 않은 사용자입니다."
        ), 404
    return jsonify(
        idx = mid,
        id = member_id,
        name = mname,
        group = gname
    ), 200