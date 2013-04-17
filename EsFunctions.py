'''
Created on 2013-4-14

@author: Eason Chen
'''
import math

class EsVector(object):
    '''
    vector class
    '''
    def __init__(self, x, y):
        self.x, self.y = x, y
    
    def add(self, x, y):
        self.x += x
        self.y += y
    
    def sub(self, x, y):
        self.x -= x
        self.y -= y
    
    def reset(self, x, y):
        self.x, self.y = x, y 

def dist((x1, y1), (x2, y2)):
    partA = (x1 - x2) ** 2
    partB = (y1 - y2) ** 2
    return math.sqrt(partA + partB)