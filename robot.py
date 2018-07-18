from motor import Motor

class Robot:
    def __init__(self):
        self.motor_front_left = Motor(35, 37, 'front left')
        self.motor_front_right = Motor(29, 31, 'front right')
        self.motor_rear_left = Motor(38, 40, 'rear left')
        self.motor_rear_right = Motor(32, 36, 'rear right')
        self.pwr = 1
        self.pwr_turn = 1

    def __log_command__(self, cmd):
        print('*** ' + cmd)

    def forward(self):
        __log_command__('forward')

        self.motor_front_left.set_power(self.pwr)
        self.motor_front_right.set_power(self.pwr)

        self.motor_rear_left.set_power(self.pwr)
        self.motor_rear_right.set_power(self.pwr)

    def back(self):
        __log_command__('back')

        self.motor_front_left.set_power(-self.pwr)
        self.motor_front_right.set_power(-self.pwr)

        self.motor_rear_left.set_power(-self.pwr)
        self.motor_rear_right.set_power(-self.pwr)

    def left(self):
        __log_command__('left')

        self.motor_front_left.set_power(-self.pwr_turn)
        self.motor_front_right.set_power(self.pwr_turn)

        self.motor_rear_left.set_power(-self.pwr_turn)
        self.motor_rear_right.set_power(self.pwr_turn)

    def right(self):
        __log_command__('right')

        self.motor_front_left.set_power(self.pwr_turn)
        self.motor_front_right.set_power(-self.pwr_turn)

        self.motor_rear_left.set_power(self.pwr_turn)
        self.motor_rear_right.set_power(-self.pwr_turn)

    def stop(self):
        __log_command__('stop')

        self.motor_front_left.set_power(0)
        self.motor_front_right.set_power(0)

        self.motor_rear_left.set_power(0)
        self.motor_rear_right.set_power(0)
