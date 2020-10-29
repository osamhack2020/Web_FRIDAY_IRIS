from models import get_session
from models import run_query
from models.models import t_daily_eat_log,GroupMemberInfo

def check_uneater(did):
    # 계정 정보를 /conn_group 으로 동기화해서 미 식사자에게 메시지 보낼 수 있게 
    subquery = get_session("r").query(t_daily_eat_log).filter_by(date_id=did).with_entities(t_daily_eat_log.c.member_id)
    # 계정 주의 그룹 멤버만으로 필터 걸어야 하는데 .. 
    row = get_session("r").query(GroupMemberInfo).filter(GroupMemberInfo.id.notin_(subquery)).all()
    if row:
        return [r.name for r in row]
    return []



