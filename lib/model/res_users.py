from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class ResUsers(Base):
    __tablename__ = 'res_users'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    login = Column(String(255))

    