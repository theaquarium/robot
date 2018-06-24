from motor import Motor

class Robot:
    def __init__(self):
        self.motor_front_left = Motor(31, 33)
        self.motor_front_right = Motor(35, 37)
        self.motor_rear_left = Motor(32, 36)
        self.motor_rear_right = Motor(38, 40)
    
    def forward(self):
        print('*** Going forward!')

        self.motor_front_left.turn_clockwise()
        self.motor_front_right.turn_anticlockwise()
        
        self.motor_rear_left.turn_clockwise()
        self.motor_rear_right.turn_anticlockwise()
    
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

        self.motor_front_left.stop()
        self.motor_front_right.stop()
        
        self.motor_rear_left.stop()
        self.motor_rear_right.stop()
