from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class PosPromotion(Base):
    __tablename__ = 'pos_promotion'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
