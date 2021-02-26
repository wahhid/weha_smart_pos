from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class PosPaymentMethod(Base):
    __tablename__ = 'pos_payment_method'

    id = Column(Integer, primary_key=True, autoincrement=True))
    name = Column(String(100))
    