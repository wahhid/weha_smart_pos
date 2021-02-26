from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class ResPartner(Base):
    __tablename__ = 'res_partner'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    email = Column(String(255))
    street = Column(String(255))
    city = Column(String(255))
    state_id = Column(Integer)
    country_id = Column(Integer)
    phone = Column(String(50))
    zip = Column(String(50))
    mobile = Column(String(50))
    email = Column(String(100))
    barcode = Column(String(50))
    property_account_position_id = Column(Integer)
    property_product_pricelist_id = Column(Integer)