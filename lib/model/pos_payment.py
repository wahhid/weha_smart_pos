from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class PosPayment(Base):
    __tablename__ = 'pos_payment'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    amount = Column(Float)
    pos_order_id = Column(Integer)
    payment_method_id = Column(Integer)
    session_id = Column(Integer)
    