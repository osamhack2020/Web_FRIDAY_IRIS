# coding: utf-8
from sqlalchemy import Column, Integer, String
import sqlalchemy.exc as SA
from sqlalchemy.ext.declarative import declarative_base
from models import default_engine 
Base = declarative_base()

def init_db():
    db_engine = default_engine
    Base.metadata.create_all(db_engine)

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
    name = Column(String(45), nullable=False, info='멤버 이름')
    cafeteria = Column(String(45), nullable=False, info='구내식당 이름 [ (군) 급양대 이름 ]')
    password = Column(String(128), nullable=False, info='비밀 번호 (sha3-512 해싱 예정 )')
    def __init__(self, name, cafeteria, password):
        self.name     = name
        self.cafeteria = cafeteria
        self.password = password