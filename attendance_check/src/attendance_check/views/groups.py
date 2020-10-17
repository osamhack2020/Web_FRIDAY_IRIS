from flask import Blueprint, jsonify
from attendance_check import db
from attendance_check.models.models import GroupList, SupplyList

groups = Blueprint('groups', __name__)

@groups.route('/groups/<supply_name>', methods=['GET'])
def get_group_list(supply_name):
    row = SupplyList.query.filter_by(name=supply_name).first()
    if not row:
        return jsonify(
            Error_Code = '404_1',
            msg = "등록되지 않은 배식장소 입니다."
        )
    group_list = GroupList.query.filter_by(supply_id=row.id)
    if not group_list:
        return jsonify(
            Error_Code = '404_2',
            msg = "해당 배식장소를 이용하는 그룹이 없습니다."
        )
        
    return jsonify(
        group_list=[row.name for row in group_list]
    )