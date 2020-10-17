from flask import Blueprint, jsonify
from attendance_check import db
from attendance_check.models.models import GroupList, SupplyList

groups = Blueprint('groups', __name__, url_prefix='/groups')

@groups.route('/<supply_name>', methods=['GET'])
def get_group_list(supply_name):
    row = SupplyList.query.filter_by(name=supply_name).first()
    if not row:
        return jsonify(
            error_id = 1,
            msg = "등록되지 않은 배식소 입니다."
        ), 404
    group_list = GroupList.query.filter_by(supply_id=row.id)
    if not group_list:
        return jsonify(
            error_id = 2,
            msg = "해당 배식소를 이용하는 그룹이 없습니다."
        ), 404
        
    return jsonify(
        group_list=[row.name for row in group_list]
    ), 200