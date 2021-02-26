from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class PosCategory(Base):
    __tablename__ = 'pos_category'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))