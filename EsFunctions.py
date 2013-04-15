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

def dist(p1, p2):
    partA = (p1.x - p2.x) ** 2
    partB = (p1.y - p2.y) ** 2
    return math.sqrt(partA + partB)