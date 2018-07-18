import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.sqlite import DATETIME

Base = declarative_base()

class Motion(Base):
    __tablename__ = 'motion'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DATETIME, nullable=False)
    type = Column(String(250), nullable=False)

    def __init__(self, type):
        self.timestamp = datetime.datetime.now()
        self.type = type

    def __repr__(self):
        return '{}: {}'.format(self.timestamp, self.type)

engine = create_engine('sqlite:///robot.db')
Base.metadata.create_all(engine)
