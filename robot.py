from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.state import InstanceState

from motor import Motor
from motion import Motion

Base = declarative_base()
engine = create_engine('sqlite:///robot.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

class Robot:
    def __init__(self):
        self.motor_front_left = Motor(35, 37, 'front left')
        self.motor_front_right = Motor(29, 31, 'front right')
        self.motor_rear_left = Motor(38, 40, 'rear left')
        self.motor_rear_right = Motor(32, 36, 'rear right')
        self.pwr = 1
        self.pwr_turn = 1

    def __log_command__(self, cmd):
        motion = Motion(cmd)
        print('- {}: {}'.format(self.__class__.__name__, motion))

        session = DBSession()
        session.add(motion)
        session.commit()

    def forward(self):
        self.__log_command__('forward')

        self.motor_front_left.set_power(self.pwr)
        self.motor_front_right.set_power(self.pwr)

        self.motor_rear_left.set_power(self.pwr)
        self.motor_rear_right.set_power(self.pwr)

    def back(self):
        self.__log_command__('back')

        self.motor_front_left.set_power(-self.pwr)
        self.motor_front_right.set_power(-self.pwr)

        self.motor_rear_left.set_power(-self.pwr)
        self.motor_rear_right.set_power(-self.pwr)

    def left(self):
        self.__log_command__('left')

        self.motor_front_left.set_power(-self.pwr_turn)
        self.motor_front_right.set_power(self.pwr_turn)

        self.motor_rear_left.set_power(-self.pwr_turn)
        self.motor_rear_right.set_power(self.pwr_turn)

    def right(self):
        self.__log_command__('right')

        self.motor_front_left.set_power(self.pwr_turn)
        self.motor_front_right.set_power(-self.pwr_turn)

        self.motor_rear_left.set_power(self.pwr_turn)
        self.motor_rear_right.set_power(-self.pwr_turn)

    def stop(self):
        self.__log_command__('stop')

        self.motor_front_left.set_power(0)
        self.motor_front_right.set_power(0)

        self.motor_rear_left.set_power(0)
        self.motor_rear_right.set_power(0)

    def get_motions(self):
        session = DBSession()
        motions = session.query(Motion).all()
        motions_serializeable = [{k: str(v) for k, v in m.__dict__.items() if k != '_sa_instance_state'} for m in motions]
        return motions_serializeable
