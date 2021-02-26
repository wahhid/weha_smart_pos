from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class PosOrder(Base):
    __tablename__ = 'pos_order'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    amount_paid = Column(Float)
    amount_total = Column(Float)
    amount_tax = Column(Float)
    amount_return = Column(Float)
    pos_session_id = Column(Integer)
    pricelist_id = Column(Integer)
    partner_id = Column(Integer)
    user_id = Column(Integer)
    employee_id = Column(Integer)
    uid = Column(Integer)
    sequence_number = Column(Integer)
    creation_date = Column(DateTime)
    fiscal_position_id = Column(Integer)
    server_id = Column(Integer)
    to_invoice = Column(Boolean)
    state = Column(String(50))


