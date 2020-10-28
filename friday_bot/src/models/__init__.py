from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.config import get_alchemy_uri
from models.config import SQLALCHEMY_BINDS
import sqlalchemy.exc as SA


# Lost connection 문제를 해결하기 위해 exception시 자동으로 다시 시도 구현
# attempts 수치를 조절할 필요는 있다.
default_engine = create_engine(SQLALCHEMY_BINDS['master'], echo = True)

def run_query(f, params=(), attempts=4, slave=False):
    while attempts > 0:
        attempts -= 1
        try:
            # "break" if query was successful and return any results
            return f(*params) 
        except SA.DBAPIError as exc:
            if attempts > 0 and exc.connection_invalidated:
                if not slave:
                    get_session("w").rollback()
                else:
                    get_session("r").rollback()
            else:
                raise

def get_session(mode="r"):
    Session = sessionmaker()
    if mode == "w":
        db_engine = create_engine(SQLALCHEMY_BINDS['master'], echo = True)
    else:
        db_engine = create_engine(SQLALCHEMY_BINDS['slave'], echo = True)
    Session.configure(bind=db_engine)
    session = Session()
    return session

    # if __name__ == '__main__':
    
    #     #  Database를 없으면 생성 또는 사용의 의미 django에서  create_or_update() (table) 같은것
    #     Base.metadata.create_all(DATABASE_ENGINE)
        
    #     # 세션을 만들어서 연결시킨다.
    #     Session = sessionmaker()
    #     Session.configure(bind=DATABASES) # 이 부분을 조절하면 될듯..?
    #     session = Session()
        
    #     # 위의 클래스,인스턴스 변수를 지킨 다음에
    #     tada = Tada('ks','ks','1111')
        
    #     # 세션에 추가를 한다.
    #     session.add(tada)
    #     session.commit()
 