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
        c = loadSprites('C.png', -1, 30, 37)
        Bar.M = m[0]
        Bar.C = c[0]
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
    def update(self, lv, dist, cd):
        self.dist += dist
        self.dist = int(self.dist)
        self.strLv = str(lv)
        self.update_cooldown(cd)
    # Display the letter 'c' while cooldown is active
    def update_cooldown(self, cd):
        if(cd):
            self.image.blit(Bar.C, (255, 4)) 
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

class statusBar():
    def __init__(self, name, pos):
        self.case = loadImage('bar.png', -1)
        self.bar = loadImage(name, None)
        self.rect_bar = Rect(0, 0, 200, 15)
        self.width = 200
        self.x, self.y = self.pos = pos
    
    def update(self, frac):
        self.width = 2.5 + 200 * frac
        self.rect_bar.width = self.width
        
    def draw(self, screen):
        screen.blit(self.case, self.pos)
        screen.blit(self.bar, self.pos, self.rect_bar)

class BrawlBar():
    digits = []
    def __init__(self):
        BrawlBar.digits = loadSprites('digits.png', -1, 26, 42)
        level = loadSprites('level.png', -1, 88, 42)
        kill = loadSprites('kill.png', -1, 88, 42)
        self.img_lv = level[0]
        self.img_kill = kill[0]
        self.HP = statusBar('hp.png', (10, 20))
        self.mana = statusBar('mana.png', (10, 40))
        self.exp = statusBar('exp.png', (10, 60))
        self.strKill = None
    
    def update(self, lv, hp_frac, mana_frac, exp_frac, kills = None):
        self.strLv = str(lv)
        if kills != None:
            self.strKill = str(kills)
        self.mana.update(mana_frac)
        self.HP.update(hp_frac)
        self.exp.update(exp_frac)
    
    def draw(self, screen):
        for i in range(len(self.strLv)):
            x = int(self.strLv[i])
            dgt = BrawlBar.digits[x]
            screen.blit(dgt, (405 + 88 + 26 * i, 4))
        if self.strKill != None:
            for i in range(len(self.strKill)):
                x = int(self.strKill[i])
                dgt = BrawlBar.digits[x]
                screen.blit(dgt, (405 + 88 + 26 * i, 45))
        screen.blit(self.img_lv, (400, 4))
        screen.blit(self.img_kill, (400, 45))
        self.HP.draw(screen)
        self.mana.draw(screen)
        self.exp.draw(screen)

