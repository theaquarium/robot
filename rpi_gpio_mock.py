class RPi_GPIO_mock:

    BOARD = 0
    OUT = 0

    def __init__(self):
        pass

    def setmode(self, *args):
        pass

    def setwarnings(self, *args):
        pass

    def setup(self, *args):
        pass

    class PWM:
        def __init__(self, *argc):
            pass

        def start(self, *args):
            pass

        def ChangeDutyCycle(self, *args):
            pass
