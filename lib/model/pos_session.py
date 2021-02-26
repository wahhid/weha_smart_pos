from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class PosSession(Base):
    __tablename__ = 'pos_session'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    config_id = Column(Integer)
    company_id = Column(Integer)
    currency_id = Column(Integer)
    user_id = Column(Integer)
    


    