try:
    import RPi.GPIO as GPIO
except ImportError:
    # Fall back to the emulator
    from rpi_gpio_emulator import RPi_GPIO_emulator as GPIO
    
class Motor:
    PWM_MAX = 100
    PWM_FREQ = 16000
    
    def __init__(self, pin1, pin2, name):
        self.pin1 = pin1
        self.pin2 = pin2
        self.name = name
        self.init()
        
        
    def init(self):
        # print('------ init motor {}, {}'.format(self.pwr_pin, self.dir_pin))
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        
        GPIO.setup(self.pin1, GPIO.OUT)
        self.pin1pwm = GPIO.PWM(self.pin1, Motor.PWM_FREQ)
        self.pin1pwm.start(0)
        
        GPIO.setup(self.pin2, GPIO.OUT)
        self.pin2pwm = GPIO.PWM(self.pin2, Motor.PWM_FREQ)
        self.pin2pwm.start(0)
        
        self.set_power(0)
    
    
    def set_power(self, power_level):
        speed = min(int(Motor.PWM_MAX * abs(power_level)), Motor.PWM_MAX)
        if power_level < 0:
            # Reverse mode
            self.pin2pwm.ChangeDutyCycle(0)
            self.pin1pwm.ChangeDutyCycle(speed)
        elif power_level > 0:
            # Forward mode
            self.pin1pwm.ChangeDutyCycle(0)
            self.pin2pwm.ChangeDutyCycle(speed)
        else:
            # Stop mode
            self.pin2pwm.ChangeDutyCycle(0)
            self.pin1pwm.ChangeDutyCycle(0)

        print('------ set power for motor {} to {}'.format(self.name, power_level))

        
    def cleanup(self):
        self.pin1pwm.ChangeDutyCycle(0)
        self.pin2pwm.ChangeDutyCycle(0)
        GPIO.cleanup()
