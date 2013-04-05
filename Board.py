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
        self.image = pygame.Surface((width, 50))
        #self.image = createBlankImage((width, 50))
        self.rect = self.image.get_rect()
        self.dist = 0
        Board.digits = loadSprites('digits.png', -1, 26, 42)
        m = loadSprites('M.png', -1, 32, 42)
        c = loadSprites('C.png', -1, 30, 37)
        Board.M = m[0]
        Board.C = c[0]
        level = loadSprites('level.png', -1, 88, 42)
        Board.img_lv = level[0]
    
    def reset(self):
        self.dist = 0
    
    #Display the current level number
    def update_level(self, level):
        strLv = str(level)
        for i in range(len(strLv)):
            x = int(strLv[i])
            dgt = Board.digits[x]
            self.image.blit(dgt, (405 + 88 + 26 * i, 4))
        self.image.blit(Board.img_lv, (400, 4))

    # Display the distance ran
    def update_distance(self, distance):
        strDist = str(self.dist)
        for i in range(len(strDist)):
            x = int(strDist[i])
            dgt = Board.digits[x]
            self.image.blit(dgt, (51 + 26 * i, 4))
        self.image.blit(Board.M, (55 + len(strDist) * 26, 4))
        
    # Display the letter 'c' while cooldown is active
    def update_cooldown(self, cd):
        if(cd):
            self.image.blit(Board.C, (255, 4)) 

    def update(self, lv, dist, cd):
        self.dist += dist
        self.dist = int(self.dist)
        self.image.fill((66, 80, 102))
        self.update_distance(dist)
        self.update_level(lv)
        self.update_cooldown(cd)
