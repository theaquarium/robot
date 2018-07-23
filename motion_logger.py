from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.state import InstanceState

from command import Command

class MotionLogger:
    def __init__(self, name):
        self.name = name

        Base = declarative_base()
        engine = create_engine('sqlite:///' + self.name +'.db')
        Base.metadata.bind = engine
        self.DBSession = sessionmaker(bind=engine)

    def log(self, cmd):
        command = Command(cmd)
        print('-> Logged Command by {}: {}'.format(self.name, command))

        session = self.DBSession()
        session.add(command)
        session.commit()
        session.close()

    def get_commands(self):
        session = self.DBSession()
        last_start = session.query(Command).\
            filter(Command.type == 'start').\
            order_by(Command.timestamp.desc()).\
            first()

        commands = session.query(Command).filter(Command.id > last_start.id).all()

        session.close()
        return commands
