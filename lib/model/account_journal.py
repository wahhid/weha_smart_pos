from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class AccountJournal(Base):
    __tablename__ = 'account_journal'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))