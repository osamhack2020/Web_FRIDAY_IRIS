from flask import Blueprint
from attendance_check import db
from attendance_check.models.models import GroupList, SupplyList

plznaming = Blueprint('plznaming', __name__)

@plznaming.route('/group/<supply_name>', methods=['GET'])
def get_group_list(supply_name):
    supply_id = SupplyList.query.filter_by(name=supply_name).first()
    print(type(supply_id), supply_id)
    group_list = GroupList.query.filter_by(supply_id=supply_id)
    print(group_list)