from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class PosOrderLine(Base):
    __tablename__ = 'pos_order_line'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer)
    name = Column(String(255))
    notice = Column(String(255))
    product_id = Column(Integer)
    price_unit = Column(Float)
    qty = Column(Float)
    price_subtotal = Column(Float)
    price_subtotal_incl = Column(Float)
    discount = Column(Float)
    order_id = Column(Integer)
    product_uom_id = Column(Integer)
    currency_id = Column(Integer)
    tax_id = Column(Integer)

    
