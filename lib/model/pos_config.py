from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class PosConfig(Base):
    __tablename__ = 'pos_config'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer)
    name = Column(String(255))
    currency_id = Column(Integer)
    pricelist_id = Column(Integer)
    

    