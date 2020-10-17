from flask import Blueprint, jsonify
from attendance_check import db
from attendance_check.models.models import GroupList, SupplyList

plznaming = Blueprint('plznaming', __name__)

@plznaming.route('/group/<supply_name>', methods=['GET'])
def get_group_list(supply_name):
    row = SupplyList.query.filter_by(name=supply_name).first()
    group_list = GroupList.query.filter_by(supply_id=row.id)
    return jsonify(
        group_list=[row.name for row in group_list]
    )