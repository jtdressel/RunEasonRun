'''
Created on 2013-3-5

@author: Eason Chen

One class included.
Board() is for displaying the current distance and level when in playmode
'''
from root import *
from EsImage import *

class Bar():
    digits = []
    themes = {'city': (66, 80, 102)}
    def __init__(self, theme):
        #self.image = pygame.Surface((width, 50))
        self.image = createBlankImage((width, 50), True, Bar.themes[theme])
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.dist = 0
        Bar.digits = loadSprites('digits.png', -1, 26, 42)
        m = loadSprites('M.png', -1, 32, 42)
        Bar.M = m[0]
        level = loadSprites('level.png', -1, 88, 42)
        Bar.img_lv = level[0]
        self.setTheme(theme)
    
    def reset(self):
        self.dist = 0
        
    def setTheme(self, newTheme):
        self.theme = newTheme
    
    def update(self, lv, dist):
        self.dist += dist
        self.dist = int(self.dist)
        self.strLv = str(lv)
    
    def draw(self, screen):
        for i in range(len(self.strLv)):
            x = int(self.strLv[i])
            dgt = Bar.digits[x]
            screen.blit(dgt, (405 + 88 + 26 * i, 4))
        screen.blit(Bar.img_lv, (400, 4))
        
        strDist = str(self.dist)
        for i in range(len(strDist)):
            x = int(strDist[i])
            dgt = Bar.digits[x]
            screen.blit(dgt, (51 + 26 * i, 4))
        screen.blit(Bar.M, (55 + len(strDist) * 26, 4))