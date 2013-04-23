'''
Created on 2013-2-15

@author: Eason Chen

Two simple timer classes for specific needs
NON-UNIVERSAL CLASSES!!!!
'''
from root import *

class CDTimer():
    def __init__(self, time):
        self.time = time
        self._start = False
    
    def setTime(self, time):
        self.time = time
    
    def start(self):
        self.startTime = pygame.time.get_ticks()
        self._start = True
    
    def isStart(self):
        return self._start
    
    def reset(self):
        self._start = False
    
    def getPercentage(self):
        if self.isStart():
            return (pygame.time.get_ticks() - self.startTime + 0.0) / (self.time + 0.0)
        return 1
    
    def timeUp(self):
        if not self._start:
            return False
        if pygame.time.get_ticks() - self.startTime >= self.time:
            self._start = False
            return True
        return False

class SimpleTimer():
    def __init__(self, duration):
        self.time = duration
        self._start = pygame.time.get_ticks()    
    
    def timeUp(self):
        if pygame.time.get_ticks() - self._start >= self.time:
            return True
        return False