import RPi.GPIO as GPIO

class Motor:
    PWM_MAX = 100
    
    def __init__(self, pwr_pin, dir_pin, name):
        self.pwr_pin = pwr_pin
        self.dir_pin = dir_pin
        self.name = name
        self.init()
        
        
    def init(self):
        # print('------ init motor {}, {}'.format(self.pwr_pin, self.dir_pin))
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.output(self.dir_pin, 0)
        
        GPIO.setup(self.pwr_pin, GPIO.OUT)
        self.PWM = GPIO.PWM(self.pwr_pin, 16000)
        self.PWM.start(0)
        self.set_power(0)
    
    
    def set_power(self, power_level):
        if power_level < 0:  
            # Reverse mode
            GPIO.output(self.dir_pin, False)  
        elif power_level > 0:  
            # Forward mode  
            GPIO.output(self.dir_pin, True)  
        else:  
            # Stop mode  
            GPIO.output(self.dir_pin, False)  
        self.power_level = int(Motor.PWM_MAX * abs(power_level))
        if self.power_level > Motor.PWM_MAX:  
            self.power_level = Motor.PWM_MAX  
        self.PWM.ChangeDutyCycle(self.power_level)
        print('------ set power for motor {} to {}'.format(self.name, self.power_level))

        
    def cleanup(self):
        GPIO.output(self.dir_pin, 0)
        GPIO.cleanup()
