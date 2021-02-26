from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class ProductProduct(Base):
    __tablename__ = 'product_product'

    id = Column(Integer, primary_key=True)
    display_name = Column(String(255))
    lst_price = Column(Float)
    standard_price = Column(Float)
    categ_id = Column(Integer)
    pos_categ_id = Column(Integer)
    taxes_id = Column(Integer)
    barcode = Column(String(20))
    default_code = Column(String(20))
    to_weight = Column(Boolean)
    uom_id = Column(Integer)
    description_sale = Column(String(255))
    description = Column(String(255))
    product_tmpl_id = Column(Integer)
    tracking = Column(String(20))
    image_1920 = Column(String())

