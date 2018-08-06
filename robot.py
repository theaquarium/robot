import math

from motor import Motor
from command import Command
from vicinity_monitor import VicinityMonitor
from motion_logger import MotionLogger

class Robot:
    def __init__(self, name):
        self.name = name

        self.motor_front_left = Motor(35, 37, 'front left')
        self.motor_front_right = Motor(29, 31, 'front right')
        self.motor_rear_left = Motor(38, 40, 'rear left')
        self.motor_rear_right = Motor(32, 36, 'rear right')
        self.pwr = 1
        self.pwr_turn = 1

        self.vicinity_monitor = VicinityMonitor()
        self.vicinity_monitor.start()

        self.logger = MotionLogger(self.name)

        self.logger.log('start')

    def forward(self):
        self.logger.log('forward')

        self.motor_front_left.set_power(self.pwr)
        self.motor_front_right.set_power(self.pwr)

        self.motor_rear_left.set_power(self.pwr)
        self.motor_rear_right.set_power(self.pwr)

    def back(self):
        self.logger.log('back')

        self.motor_front_left.set_power(-self.pwr)
        self.motor_front_right.set_power(-self.pwr)

        self.motor_rear_left.set_power(-self.pwr)
        self.motor_rear_right.set_power(-self.pwr)

    def left(self):
        self.logger.log('left')

        self.motor_front_left.set_power(-self.pwr_turn)
        self.motor_front_right.set_power(self.pwr_turn)

        self.motor_rear_left.set_power(-self.pwr_turn)
        self.motor_rear_right.set_power(self.pwr_turn)

    def right(self):
        self.logger.log('right')

        self.motor_front_left.set_power(self.pwr_turn)
        self.motor_front_right.set_power(-self.pwr_turn)

        self.motor_rear_left.set_power(self.pwr_turn)
        self.motor_rear_right.set_power(-self.pwr_turn)

    def stop(self):
        self.logger.log('stop')

        self.motor_front_left.set_power(0)
        self.motor_front_right.set_power(0)

        self.motor_rear_left.set_power(0)
        self.motor_rear_right.set_power(0)

    def get_trajectory(self):
        _max_duration = 10  # 10 sec
        _max_duration = 0   # ignore
        _speed_right = 90   # deg/sec
        _speed_left = 30    # deg/sec
        _speed_forward = 30 * 2.54 / 100;  # m/sec
        _speed_backward = 30 * 2.54 / 100; # m/sec

        pos = (0, 0)
        angle = 0
        path = [pos]

        motions = self.logger.get_commands()

        for i in range(len(motions)):
            m = motions[i]
            duration = (motions[i + 1].timestamp - m.timestamp).total_seconds() if i < (len(motions) - 1) else _max_duration

            if m.type == 'stop':
                continue
            if m.type == 'left':
                angle = angle - _speed_left * duration
            if m.type == 'right':
                angle = angle + _speed_right * duration
            if m.type == 'forward':
                distance = _speed_forward * duration
                pos_x = pos[0] + distance * math.cos(math.radians(angle))
                pos_y = pos[1] + distance * math.sin(math.radians(angle))
                pos = (pos_x, pos_y)
                path.append(pos)
            if m.type == 'back':
                distance = _speed_backward * duration
                pos_x = pos[0] - distance * math.cos(math.radians(angle))
                pos_y = pos[1] - distance * math.sin(math.radians(angle))
                pos = (pos_x, pos_y)
                path.append(pos)

        return {
            'path': path,
            'direction': angle
        }
