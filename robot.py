from motor import Motor

class Robot:
    def __init__(self):
        self.motor_front_left = Motor(16, 12, 'front left')
        self.motor_front_right = Motor(10, 8, 'front right')
        self.motor_rear_left = Motor(18, 22, 'rear left')
        self.motor_rear_right = Motor(24, 26, 'rear right')
    
    def forward(self):
        print('*** Going forward!')

        pwr = .05
        self.motor_front_left.set_power(pwr)
        self.motor_front_right.set_power(pwr)
        
        self.motor_rear_left.set_power(pwr)
        self.motor_rear_right.set_power(pwr)
    
    def back(self):
        print('*** Going back!')

        self.motor_front_left.turn_anticlockwise()
        self.motor_front_right.turn_clockwise()
        
        self.motor_rear_left.turn_anticlockwise()
        self.motor_rear_right.turn_clockwise()
    
    def left(self):
        print('*** Turning left!')

        self.motor_front_left.turn_anticlockwise()
        self.motor_front_right.turn_anticlockwise()
        
        self.motor_rear_left.turn_anticlockwise()
        self.motor_rear_right.turn_anticlockwise()
    
    def right(self):
        print('*** Turning right!')

        self.motor_front_left.turn_clockwise()
        self.motor_front_right.turn_clockwise()
        
        self.motor_rear_left.turn_clockwise()
        self.motor_rear_right.turn_clockwise()
    
    def stop(self):
        print('*** Stopping!')

        self.motor_front_left.set_power(0)
        self.motor_front_right.set_power(0)
        
        self.motor_rear_left.set_power(0)
        self.motor_rear_right.set_power(0)
