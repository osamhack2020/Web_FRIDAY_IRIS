from models import get_session
from models import run_query
from models.models import RegisterCode, CafeteriaList, Account
import sqlalchemy as db

def exist_register_code(usr_input):
    row = get_session("r").query(RegisterCode).filter_by(code=usr_input).first()
    if row:
        return True
    else:
        return False

def exist_cafeteria_name(name):
    row = get_session("r").query(CafeteriaList).filter_by(name=name).first()
    if row:
        return True
    else:
        return False

def available_register_code(usr_input):
    return run_query(exist_register_code, ([usr_input]))

def available_cafeteria(name):
    return run_query(exist_cafeteria_name, ([name]))

def insert_user_info(name, cafeteria, password):
    new_acc = Account(name, cafeteria, password)
    sess = get_session("w")
    sess.add(new_acc)
    sess.commit()

def set_user_info(user_dict):
    params = (
        user_dict['nickname'],
        user_dict['cafeteria'],
        user_dict['password']
    )
    run_query(insert_user_info, params)