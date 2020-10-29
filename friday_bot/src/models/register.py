from models import get_session
from models import run_query
from models.models import RegisterCode, CafeteriaList, Account, GroupList, GroupMemberInfo
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

def insert_user_info(chat_id, name, cafeteria, password):
    new_acc = Account(chat_id, name, cafeteria, password)
    sess = get_session("w")
    sess.add(new_acc)
    sess.commit()

def set_user_info(chat_id, user_dict):
    # password 준비하기
    params = (
        chat_id,
        user_dict['nickname'],
        user_dict['cafeteria'],
        user_dict['password']
    )
    run_query(insert_user_info, params)

def exist_password(chat_id, password):
    row = get_session("r").query(Account).filter_by(chat_id=chat_id, password=password).first()
    if row:
        return True
    else:
        return False

def available_password(chat_id, password):
    return run_query(exist_password, (chat_id, password))

def exist_group_name(cafeteria_id, group_name):
    row = get_session("r").query(GroupList).filter_by(cafeteria_id=cafeteria_id, name=group_name).first()
    if row:
        return True
    else:
        return False   

def available_group_name(cafeteria, group_name):
    return run_query(exist_group_name, (cafeteria, group_name))

def find_user_cafeteria_info(chat_id):
    row = get_session("r").query(Account).with_entities(Account.cafeteria).filter_by(chat_id=chat_id).first()
    if row:
        return row.cafeteria
    else:
        return ''

def get_cafeteria_id(name):
    row = get_session("r").query(CafeteriaList).filter_by(name=name).first()
    if row:
        return row.id
    else:
        return -1

def get_user_cafeteria_id(chat_id):
    name = run_query(find_user_cafeteria_info, ([chat_id]))
    if name:
        _id = run_query(get_cafeteria_id, ([name]))
        if _id != -1:
            return _id

def get_group_id(name):
    row = get_session("r").query(GroupList).filter_by(name=name).first()
    if row:
        return row.id
    else:
        return -1

def insert_group_user(mid, gid, name):
    new_user = GroupMemberInfo(member_id=mid, group_id=gid, name=name)
    sess = get_session("w")
    sess.add(new_user)
    sess.commit()

def insert_group(name, cid):
    new_group = GroupList(name=name, cafeteria_id = cid)
    sess = get_session("w")
    sess.add(new_group)
    sess.commit()
    
def insert_cafeteria(name):
    new_ct = CafeteriaList(name=name)
    sess = get_session("w")
    sess.add(new_ct)
    sess.commit()

def add_group_user(group_name, member_name, member_id):
    gid = run_query(get_group_id, ([group_name]))
    if gid != -1:
        run_query(insert_group_user, (member_id, gid, member_name))

def add_group(cafeteria_id, group_name):
    run_query(insert_group, (group_name, cafeteria_id))

def add_cafeteria(name):
    run_query(insert_cafeteria, ([name]))