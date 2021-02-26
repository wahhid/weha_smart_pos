from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class SyncProcess(Base):
    __tablename__ = 'sync_process'

    model_name = Column(String(255), primary_key=True)
    last_sync = Column(DateTime)
