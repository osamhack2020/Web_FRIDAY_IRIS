from models import get_session
from models import run_query
from models.models import t_daily_menu, MenuInfo
import sqlalchemy as db

def get_menu_id(menu):
    row = get_session("r").query(MenuInfo).filter_by(menu_name=menu).first()
    if row:
        return row.id
    else:
        return -1

def find_menu_id(menu):
    _id = run_query(get_menu_id, ([menu]))
    if _id != -1:
        return _id

def insert_daily_menu(date_id, menu_id):
    insert_stmt = t_daily_menu.insert().values(date_id=date_id, menu_id=menu_id)
    sess = get_session("w")
    sess.execute(insert_stmt)
    sess.commit()

def set_daily_menu(date_id, menu_name):
    mid = find_menu_id(menu_name)
    run_query(insert_daily_menu, (date_id, mid))
