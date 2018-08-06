import threading
import pigpio
import time
from SonarI2C import SonarI2C

class VicinityMonitor(threading.Thread):
    def __init__(self):
        super(VicinityMonitor, self).__init__()
        self.stoprequest = threading.Event()
        self.pi = pigpio.pi()
        self.octosonar = SonarI2C(self.pi, int_gpio=17)

    def run(self):
        # As long as we weren't asked to stop, try to take new tasks from the
        # queue. The tasks are taken with a blocking 'get', so no CPU
        # cycles are wasted while waiting.
        # Also, 'get' is given a timeout, so stoprequest is always checked,
        # even if there's nothing in the queue.
        result_list = []
        while not self.stoprequest.isSet():
            try:
                for i in range(8):
                    sonar_result = self.octosonar.read_cm(i)
                    time.sleep(0.01)
                    if sonar_result is False:
                        result_list.append("Timed out")
                    else:
                        result_list.append(round(sonar_result, 1))
                print(result_list)
                result_list = []
            except Queue.Empty:
                continue

    def join(self, timeout=None):
        self.stoprequest.set()
        self.octosonar.cancel()
        self.pi.stop()
        super(VicinityMonitor, self).join(timeout)
