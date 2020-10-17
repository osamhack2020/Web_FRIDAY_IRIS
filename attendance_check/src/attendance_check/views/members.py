from flask import Blueprint, jsonify
from attendance_check import db
from attendance_check.models.models import GroupList, GroupMemberInfo

members = Blueprint('members', __name__, url_prefix='/members')

@members.route('/<member_id>', methods=['GET'])
def get_member_info(member_id):
    row = GroupMemberInfo.query.filter_by(member_id=member_id).first()
    if not row:
        return jsonify(
            error_id = 1,
            msg = "멤버 정보를 조회할 수 없습니다."
        ), 404
    row2 = GroupList.query.filter_by(id=row.group_id).first()
    if not row2:
        return jsonify(
            error_id = 2,
            msg = "그룹 정보가 등록되어 있지 않은 사용자입니다."
        ), 404
    return jsonify(
        ID = row.member_id,
        NAME = row.name,
        Group = row2.name
    ), 200