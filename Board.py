'''
Created on 2013-3-5

@author: Eason Chen

One class included.
Board() is for displaying the current distance and level when in playmode
'''
from root import *
from EsImage import *

class Board():
    digits = []
    def __init__(self):
        self.image = pygame.Surface((width, 100))
        self.rect = self.image.get_rect()
        self.dist = 0
        Board.digits = loadImage('digits.png', -1, 26, 42)
        m = loadImage('M.png', -1, 32, 42)
        Board.M = m[0]
        level = loadImage('level.png', -1, 88, 42)
        Board.img_lv = level[0]
    
    def reset(self):
        self.dist = 0
    
    def update(self, lv, dist):
        blk = (0, 0, 0)
        self.dist += dist
        self.dist = int(self.dist)
        self.image.fill((255, 255, 255))
        
        strLv = str(lv)
        for i in range(len(strLv)):
            x = int(strLv[i])
            dgt = Board.digits[x]
            self.image.blit(dgt, (405 + 88 + 26 * i, 16))
        self.image.blit(Board.img_lv, (400, 16))
        
        strDist = str(self.dist)
        for i in range(len(strDist)):
            x = int(strDist[i])
            dgt = Board.digits[x]
            self.image.blit(dgt, (51 + 26 * i, 16))
        self.image.blit(Board.M, (55 + len(strDist) * 26, 16))
        