from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class PosSync(Base):
    __tablename__ = 'pos_sync'

    id = Column('id', Integer, primary_key=True)
    modelName = Column('model_name', String, unique=True)
    lastSync = Column('last_sync', DateTime)

#class PosConfig(Base):
#    __tablename__ = 'pos_config'

#    id = Column()


engine = create_engine('sqlite:///pos.db', echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

possyncs = session.query(PosSync).all()
for possync in possyncs:
    print(possync.lastSync)
# possync = PosSync()
# possync.id = 2
# possync.modelName = 'res.partner'
# possync.lastSync = datetime.now()

# session.add(possync)
# session.commit()
# session.close()