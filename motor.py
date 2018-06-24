import RPi.GPIO as GPIO

class Motor:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        
    def init(self):
        # print('------ init motor {}, {}'.format(self.a, self.b))
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.a, GPIO.OUT)
        GPIO.setup(self.b, GPIO.OUT)
        # GPIO.setwarnings(False)
    
    def turn_clockwise(self):
        self.init()
        GPIO.output(self.a, 1)
        GPIO.output(self.b, 0)
    
    def turn_anticlockwise(self):
        self.init()
        GPIO.output(self.a, 0)
        GPIO.output(self.b, 1)
    
    def stop(self):
        GPIO.cleanup()
