# coding: utf-8
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Date, Enum, Boolean, SmallInteger
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
    Column('menu_id', ForeignKey('menu_info.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, info='메뉴 인덱스')
)

class MenuInfo(Base):
    __tablename__ = 'menu_info'

    id = Column(Integer, primary_key=True, info='메뉴 인덱스')
    menu_name = Column(String(45), nullable=False, info='메뉴 이름')
    meal_type = Column(String(45), nullable=False, info='메뉴 종류 ( 주식 / 밑 반찬 / 후식 )')
    cooking_method = Column(String(45), nullable=False, info='조리 방법 ( 대 분류 )')
    ingredient = Column(String(66), nullable=True, info='조리 재료 ( 중분류 )') # sum(all) * 3(hangul) / 2 (not all) , 대분류에서 끝나는 경우가 있어서 null가능 처리 

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


class DailyWeatherInfo(DateMealtimeMapping):
    __tablename__ = 'daily_weather_info'

    date_id = Column(ForeignKey('date_mealtime_mapping.id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, info='날짜 인덱스')
    is_abnormal_temperature = Column(Boolean, nullable=False, info='이상 기온 여부')
    is_heat_wave = Column(Boolean, nullable=False, info='폭염 여부')
    snow = Column(Boolean, nullable=False, info='눈 (  진눈깨비 비포함 )')
    rain = Column(Boolean, nullable=False, info='비 ( 진눈깨비 포함 )')
    discomfort_index = Column(Enum('low', 'normal', 'high', 'very high'), nullable=False, info='불퀘지수')
    cloudy = Column(Enum('clear', 'little cloudy', 'cloudy', 'grey'), nullable=False, info='흐림 여부')
    wind_chill_temperature = Column(Integer, nullable=False, info='체감 온도')


class PredictLog(DateMealtimeMapping):
    __tablename__ = 'predict_log'

    date_id = Column(ForeignKey('date_mealtime_mapping.id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, info='날짜 인덱스')
    predict_real_count = Column(SmallInteger, nullable=False, info='예측한 실 식수 인원')


class SpecialEvent(DateMealtimeMapping):
    __tablename__ = 'special_event'

    date_id = Column(ForeignKey('date_mealtime_mapping.id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, info='날짜 인덱스')
    is_positive = Column(Boolean, nullable=False, info='긍정 이벤트 ( 특식, 복날, 훈련 등 식수 증가 )')
    is_negative = Column(Boolean, nullable=False, info='부정 이벤트 ( 외부기관 훈련 )')

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
