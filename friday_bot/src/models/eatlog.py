from models import get_session
from models import run_query
from models.models import t_daily_eat_log,GroupMemberInfo, MemberChatIdMapping, GroupList, Account, CafeteriaList
from sqlalchemy import and_
def check_uneater(cid, did):
    # 계정 정보를 /conn_group 으로 동기화해서 미 식사자에게 메시지 보낼 수 있게 
    subquery2 = get_session("r").query(GroupList).filter_by(cafeteria_id=cid).with_entities(GroupList.id)
    subquery = get_session("r").query(t_daily_eat_log).filter_by(date_id=did).with_entities(t_daily_eat_log.c.member_id)
    # 계정 주의 그룹 멤버만으로 필터 걸어야 하는데 .. 
    row = get_session("r").query(GroupMemberInfo).filter(and_(GroupMemberInfo.id.notin_(subquery), GroupMemberInfo.group_id.in_(subquery2))).all()
    if row:
        return [r.name for r in row]
    return []

def get_member_id(name):
    row = get_session("r").query(GroupMemberInfo).filter_by(name=name).first()
    if row:
        return row.id
    else:
        return -1

def get_cafeteria_name(chat_id):
    row = get_session("r").query(Account).filter_by(chat_id=chat_id).first()
    if row:
        return row.cafeteria
    else:
        return ''

def get_cafeteria_id(c_name):
    row = get_session("r").query(CafeteriaList).filter_by(name=c_name).first()
    if row:
        return row.id
    else:
        return -1   

def get_member_name(member_id):
    row = get_session("r").query(GroupMemberInfo).filter_by(member_id=member_id).first()
    if row:
        return row.name
    else:
        return ''

def get_member_mapped_id(chat_id):
    row = get_session("r").query(MemberChatIdMapping).filter_by(chat_id=chat_id).first()
    if row:
        return row.id
    else:
        return -1

def get_chat_id(mid):
    row = get_session("r").query(MemberChatIdMapping).filter_by(member_id=mid).first()
    if row:
        return row.chat_id
    else:
        return -1

def find_chat_id(name):
    mid = run_query(get_member_id, ([name]))
    cid = run_query(get_chat_id, ([mid]))
    if cid != -1:
        return cid

def find_member_id(name):
    _id = run_query(get_member_id, ([name]))
    if _id != -1:
        return _id

def find_mid_at_map(chat_id):
    _id = run_query(get_member_mapped_id, ([chat_id]))
    if _id != -1:
        return _id

def find_member_name(member_id):
    name = run_query(get_member_name, ([member_id]))
    if name:
        return name

def insert_user_chat_id_map(chat_id, member_id):
    new_map = MemberChatIdMapping(member_id=member_id, chat_id = chat_id)
    sess = get_session("w")
    sess.add(new_map)
    sess.commit()

def set_chat_id(chat_id, member_id):
    run_query(insert_user_chat_id_map, (chat_id, member_id))

def find_cafeteria_id(chat_id):
    c_name = run_query(get_cafeteria_name, ([chat_id]))
    if c_name:
        c_id = run_query(get_cafeteria_id, ([c_name]))
    return c_id

