# coding: utf-8
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Date, Enum, Boolean, SmallInteger, Float, Text
from sqlalchemy.orm import relationship
import sqlalchemy.exc as SA
from sqlalchemy.ext.declarative import declarative_base
from models import default_engine 
Base = declarative_base()

def init_db():
    db_engine = default_engine
    Base.metadata.create_all(db_engine)

class MemberChatIdMapping(Base):

    __tablename__ = 'member_chat_id_map'

    id = Column(Integer, primary_key=True)
    member_id = Column(ForeignKey('group_member_info.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True, info='멤버 인덱스')
    chat_id = Column(Integer, nullable=False, info='채팅방 고유번호')

    def __init__(self, member_id, chat_id):
        self.member_id = member_id
        self.chat_id = chat_id

class RealHeadcount(Base):
    __tablename__ = 'real_headcount'
    id = Column(Integer, primary_key=True, info='데이터 인덱스')
    date_id = Column(ForeignKey('date_mealtime_mapping.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, info='날짜 인덱스')
    n = Column(Integer, nullable=False, info="실 식수인원 수")

    def __init__(self, date_id, n):
        self.date_id = date_id
        self.n = n

class RegisterCode(Base):
 
    __tablename__ = 'register_code'
 
    id       = Column(Integer, primary_key=True)
    code     = Column(String(20), nullable=False, info='등록 코드')
    # 추후에 기간 항목을 수정해도 좋을 것 같음.
    
    def __init__(self, code):
        self.code     = code

class CafeteriaList(Base):
    __tablename__ = 'cafeteria_list'

    id = Column(Integer, primary_key=True, info='인덱스')
    name = Column(String(45), nullable=False, info='구내식당 이름 [ (군) 급양대 이름 ]')

    def __init__(self, name):
        self.name     = name

class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, info='인덱스')
    chat_id = Column(Integer, unique=True, info='ID역할을 할 chat_id')
    name = Column(String(45), nullable=False, info='멤버 이름')
    cafeteria = Column(String(45), nullable=False, info='구내식당 이름 [ (군) 급양대 이름 ]')
    password = Column(String(128), nullable=False, info='비밀 번호 (sha3-512 해싱 예정 )')
    def __init__(self, chat_id, name, cafeteria, password):
        self.chat_id = chat_id
        self.name     = name
        self.cafeteria = cafeteria
        self.password = password

t_daily_eat_log = Table(
    'daily_eat_log',
    Base.metadata,
    Column('date_id', ForeignKey('date_mealtime_mapping.id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, info='날짜 인덱스'),
    Column('member_id', ForeignKey('group_member_info.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True, info='멤버 인덱스')
)

t_daily_menu = Table(
    'daily_menu',
    Base.metadata,
    Column('date_id', ForeignKey('date_mealtime_mapping.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True, info='날짜 인덱스'),
    Column('cafeteria_id', ForeignKey('cafeteria_list.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, info='식당 인덱스'),
    Column('menu_id', ForeignKey('menu_info.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, info='메뉴 인덱스')
)

class FitData(Base):
    __tablename__ = 'fit_data'
    id = Column(Integer, primary_key=True, info='데이터 인덱스')
    serial = Column(Text, nullable=False)
    token_len = Column(Integer, nullable=False)

    def __init__(self, serial, token_len):
        self.serial = serial
        self.token_len = token_len

class MenuInfo(Base):
    __tablename__ = 'menu_info'

    id = Column(Integer, primary_key=True, info='메뉴 인덱스')
    menu_name = Column(String(45), nullable=False, info='메뉴 이름')
    info_serial = Column(Text, nullable=False, info='예) "구이류,튀김류" 이런 방식으로 데이터 저장')
    
    def __init__(self, menu_name, info_serial):
        self.menu_name = menu_name
        self.info_serial = info_serial

class DateMealtimeMapping(Base):
    __tablename__ = 'date_mealtime_mapping'

    id = Column(Integer, primary_key=True, info='인덱스')
    korean_date = Column(Date, nullable=False, info='날짜(20200101)')
    meal_time = Column(Enum('breakfast', 'lunch', 'dinner'), nullable=False, info='식사시간 ( 1~3 : 아침, 점심, 저녁 )')


class DailyHeadcount(DateMealtimeMapping):
    __tablename__ = 'daily_headcount'

    date_id = Column(ForeignKey('date_mealtime_mapping.id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, info='날짜 인덱스')
    official_count = Column(SmallInteger, nullable=False, info='식사 가능 인원 수')
    real_count = Column(SmallInteger, info='실제 식사 인원 수')


class DailyHolidayCheck(DateMealtimeMapping):
    __tablename__ = 'daily_holiday_check'

    date_id = Column(ForeignKey('date_mealtime_mapping.id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, info='날짜 인덱스')
    is_weekend = Column(Boolean, nullable=False, info='휴일 여부')
    before_weekend = Column(Boolean, nullable=False, info='휴일 전날 여부')
    after_weekend = Column(Boolean, nullable=False, info='휴일 다음날 여부')
    before_long_weekend = Column(Boolean, nullable=False, info='연휴 ( 3일 이상 ) 전날 여부')
    after_long_weekend = Column(Boolean, nullable=False, info='연휴 ( 3일 이상 ) 다음날 여부')
    in_end_year = Column(Boolean, nullable=False, info='연말 ( 12 /  21~31 ) 여부')

class DailyWeather(Base):

    __tablename__ = 'daily_weather'
    id = Column(Integer, primary_key=True, info='데이터 인덱스')
    date = Column(Date, nullable=False, info='날짜(20200101)')
    h = Column(Integer, nullable=False)
    t = Column(Float, nullable=False)
    hm = Column(Integer, nullable=False)
    ws = Column(Float, nullable=False)
    rain = Column(Boolean, nullable=False, info='비')
    snow = Column(Boolean, nullable=False, info='눈')

    def __init__(self, date, h, t, hm, ws, rain, snow):
        self.date = date
        self.h = h
        self.t = t
        self.hm = hm
        self.ws = ws
        self.rain = rain
        self.snow = snow

class GroupList(Base):
    __tablename__ = 'group_list'

    id = Column(Integer, primary_key=True, info='인덱스')
    name = Column(String(45), nullable=False, unique=True, info='집단 이름')
    cafeteria_id = Column(ForeignKey('cafeteria_list.id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True, info='배식소 인덱스')

    supply = relationship('CafeteriaList', primaryjoin='GroupList.cafeteria_id == CafeteriaList.id', backref='group_lists')

class GroupMemberInfo(Base):
    __tablename__ = 'group_member_info'

    id = Column(Integer, primary_key=True, info='인덱스')
    member_id = Column(String(45), nullable=False, info='구성원 고유 번호 [ 예) 군번 / 순번 ]')
    group_id = Column(ForeignKey('group_list.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True, info='집단 인덱스')
    name = Column(String(15), nullable=False, info='이름')

    group = relationship('GroupList', primaryjoin='GroupMemberInfo.group_id == GroupList.id', backref='group_member_infos')
