# Timer
import time

class Timer:
    def __init__(self):
        self.start = 0
        self.stop = 0

    def startTimer(self):
        self.start = time.time()

    def stopTimer(self):
        self.stop = time.time()

    def getTime(self):
        return self.stop - self.start
