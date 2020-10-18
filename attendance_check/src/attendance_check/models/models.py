# coding: utf-8
from attendance_check import db

def init_scheme():
    db.create_all()

t_daily_eat_log = db.Table(
    'daily_eat_log',
    db.Column('date_id', db.ForeignKey('date_mealtime_mapping.id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, info='날짜 인덱스'),
    db.Column('member_id', db.ForeignKey('group_member_info.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True, info='구성원 고유 번호 [ 예) 군번 / 순번 ]')
)

class DailyMenu(db.Model):
    __tablename__ = 'daily_menu'

    id = db.Column(db.Integer, primary_key=True, info='인덱스')
    date_id = db.Column(db.ForeignKey('date_mealtime_mapping.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True, info='날짜 인덱스')
    menu = db.Column(db.String(45), nullable=False, info='메뉴')

    date = db.relationship('DateMealtimeMapping', primaryjoin='DailyMenu.date_id == DateMealtimeMapping.id', backref='daily_menus')


class MenuInfo(DailyMenu):
    __tablename__ = 'menu_info'

    menu_id = db.Column(db.ForeignKey('daily_menu.id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, info='메뉴 인덱스')
    meal_type = db.Column(db.String(45), nullable=False, info='메뉴 종류 ( 주식 / 밑 반찬 / 후식 )')
    cooking_method = db.Column(db.String(45), nullable=False, info='조리 방법 ( 대 분류 )')
    ingredient = db.Column(db.String(45), nullable=False, info='조리 재료 ( 중분류 )')



class DateMealtimeMapping(db.Model):
    __tablename__ = 'date_mealtime_mapping'

    id = db.Column(db.Integer, primary_key=True, info='인덱스')
    korean_date = db.Column(db.Date, nullable=False, info='날짜(20200101)')
    meal_time = db.Column(db.Enum('breakfast', 'lunch', 'dinner'), nullable=False, info='식사시간 ( 1~3 : 아침, 점심, 저녁 )')
    members = db.relationship('Account', secondary='daily_eat_log', backref='date_mealtime_mappings')


class DailyHeadcount(DateMealtimeMapping):
    __tablename__ = 'daily_headcount'

    date_id = db.Column(db.ForeignKey('date_mealtime_mapping.id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, info='날짜 인덱스')
    official_count = db.Column(db.SmallInteger, nullable=False, info='식사 가능 인원 수')
    real_count = db.Column(db.SmallInteger, info='실제 식사 인원 수')


class DailyHolidayCheck(DateMealtimeMapping):
    __tablename__ = 'daily_holiday_check'

    date_id = db.Column(db.ForeignKey('date_mealtime_mapping.id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, info='날짜 인덱스')
    is_weekend = db.Column(db.Boolean, nullable=False, info='휴일 여부')
    before_weekend = db.Column(db.Boolean, nullable=False, info='휴일 전날 여부')
    after_weekend = db.Column(db.Boolean, nullable=False, info='휴일 다음날 여부')
    before_long_weekend = db.Column(db.Boolean, nullable=False, info='연휴 ( 3일 이상 ) 전날 여부')
    after_long_weekend = db.Column(db.Boolean, nullable=False, info='연휴 ( 3일 이상 ) 다음날 여부')
    in_end_year = db.Column(db.Boolean, nullable=False, info='연말 ( 12 /  21~31 ) 여부')


class DailyWeatherInfo(DateMealtimeMapping):
    __tablename__ = 'daily_weather_info'

    date_id = db.Column(db.ForeignKey('date_mealtime_mapping.id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, info='날짜 인덱스')
    is_abnormal_temperature = db.Column(db.Boolean, nullable=False, info='이상 기온 여부')
    is_heat_wave = db.Column(db.Boolean, nullable=False, info='폭염 여부')
    snow = db.Column(db.Boolean, nullable=False, info='눈 (  진눈깨비 비포함 )')
    rain = db.Column(db.Boolean, nullable=False, info='비 ( 진눈깨비 포함 )')
    discomfort_index = db.Column(db.Enum('low', 'normal', 'high', 'very high'), nullable=False, info='불퀘지수')
    cloudy = db.Column(db.Enum('clear', 'little cloudy', 'cloudy', 'grey'), nullable=False, info='흐림 여부')
    wind_chill_temperature = db.Column(db.Integer, nullable=False, info='체감 온도')


class PredictLog(DateMealtimeMapping):
    __tablename__ = 'predict_log'

    date_id = db.Column(db.ForeignKey('date_mealtime_mapping.id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, info='날짜 인덱스')
    predict_real_count = db.Column(db.SmallInteger, nullable=False, info='예측한 실 식수 인원')


class SpecialEvent(DateMealtimeMapping):
    __tablename__ = 'special_event'

    date_id = db.Column(db.ForeignKey('date_mealtime_mapping.id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, info='날짜 인덱스')
    is_positive = db.Column(db.Boolean, nullable=False, info='긍정 이벤트 ( 특식, 복날, 훈련 등 식수 증가 )')
    is_negative = db.Column(db.Boolean, nullable=False, info='부정 이벤트 ( 외부기관 훈련 )')



class GroupList(db.Model):
    __tablename__ = 'group_list'

    id = db.Column(db.Integer, primary_key=True, info='인덱스')
    name = db.Column(db.String(45), nullable=False, unique=True, info='집단 이름')
    supply_id = db.Column(db.ForeignKey('supply_list.id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True, info='배식소 인덱스')

    supply = db.relationship('SupplyList', primaryjoin='GroupList.supply_id == SupplyList.id', backref='group_lists')



class GroupMemberInfo(db.Model):
    __tablename__ = 'group_member_info'

    id = db.Column(db.Integer, primary_key=True, info='인덱스')
    member_id = db.Column(db.String(45), nullable=False, info='구성원 고유 번호 [ 예) 군번 / 순번 ]')
    group_id = db.Column(db.ForeignKey('group_list.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True, info='집단 인덱스')
    name = db.Column(db.String(15), nullable=False, info='이름')

    group = db.relationship('GroupList', primaryjoin='GroupMemberInfo.group_id == GroupList.id', backref='group_member_infos')


class Account(GroupMemberInfo):
    __tablename__ = 'accounts'

    member_id = db.Column(db.ForeignKey('group_member_info.id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, info='구성원 인덱스')
    group_id = db.Column(db.ForeignKey('group_list.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True, info='집단 인덱스')
    password = db.Column(db.String(128), nullable=False, info='비밀 번호 (sha3-512 해싱 )')

    group = db.relationship('GroupList', primaryjoin='Account.group_id == GroupList.id', backref='accounts')



class SupplyList(db.Model):
    __tablename__ = 'supply_list'

    id = db.Column(db.Integer, primary_key=True, info='인덱스')
    name = db.Column(db.String(45), nullable=False, info='배식소 이름 [ (군) 급양대 이름 ]')
