'''
Created on 2013-4-4

@author: Eason Chen

One background class, you pass the background image file name as the parameter
and it will automatically load it and draw it onto the screen, make sure the 
height of your background image file is the same as the screen height, which, 
in this case, is 400. And also, the class has update() and draw() methods, 
so don't forget to update and then draw when you use this class to make your
background.
'''
from root import *
from EsImage import *

class Background():
    def __init__(self, name):
        self.images = [0, 0]
        self.images[0] = loadImage(name, None)
        self.images[1] = self.images[0]
        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()
        self.rects = [0, 0]
        self.x = [0, self.width + 1]
        self.y = [0, 0]
        for i in range(2):
            self.rects[i] = self.images[i].get_rect()
            
    
    def reset(self):
        self.x = [0, self.width + 1]
        self.y = [0, 0]
    
    def update(self, x):
        for i in range(2):
            self.x[i] += x
            if self.x[i] + self.width < 0:
                self.x[i] = self.x[(i+1)%2] + self.width + 1
            self.rects[i].topleft = (self.x[i], self.y[i])
    
    def draw(self, screen):
        for i in range(2):
            screen.blit(self.images[i], self.rects[i])