import time
import random

class Point:
    def __init__(self, width, height):
        self.x = random.randrange(0, width)
        self.y = random.randrange(0, height)

class Timer:
    def __init__(self):
        self.startTime = time.time()
        self.currentTime = time.time()
        self.lastTime = self.currentTime
        self.counter = 0 # The time has passed after reset
    
    def Tick(self):
        self.currentTime = time.time()
        self.counter = self.currentTime - self.lastTime
    
    def Reset(self):
        self.lastTime = self.currentTime
        self.counter = 0

    def TotalTime(self):
        return time.time() - self.startTime