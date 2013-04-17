'''
Created on 2013-2-10

@author: Eason Chen

creating floor objects
'''
from root import *
from EsAnimation import *

def createColoredImage((width, height), color):
    image = pygame.Surface((width, height))
    image = image.convert_alpha()
    image.fill(color)
    return image

class Floor(pygame.sprite.Sprite):
    def __init__(self, pos, size, color = (255,255,255)):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y = pos
        self.width, self.height = size
        self.image = createColoredImage(size, color)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x, self.y
        
    def out_of_sight(self):
        if self.x + self.width < 0:
            return True
        return False
    
    def update(self, x):
        self.x += x
        self.rect.topleft = self.x, self.y
        