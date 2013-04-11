'''
Created on 2013-4-5

@author: Eason Chen
'''
from root import *
from modes import *
from EsAnimation import *
from EsSounds import *
from Eason import *
from Stupid import *
from BadGuy import *
from Background import *

class BrawlMode(GameMode):
    def __init__(self, name, upper, lower):
        self.background = Background(name)
        self.upper_bound, self.lower_bound = upper, lower
        self.eason = BrawlEason(pos, upper, lower)
        self.eason.stand()

        #badguy1
        self.baddy = BadGuy(pos, upper-10, lower-10)
        self.baddy.stand()
        
    def newBound(self, nu, nl):
        self.eason.newBound(nu, nl)
    
    def enter(self):
        self.eason.update()
        self.baddy.update()
    
    def key_down(self, event):
        if event.key == K_ESCAPE:
            self.switch_to_mode('menu_mode')
        horizontal = {K_a: -v_w, K_d: v_w}
        vertical = {K_w: -0.8, K_s: 0.8}
        if event.key in horizontal:
            self.eason.setVelocity(horizontal[event.key], None)
        if event.key in vertical:
            self.eason.setVelocity(None, vertical[event.key])
        if event.key == K_j:
        	self.eason.attack()
    
    def key_up(self, event):
        horizontal = {K_a: v_w, K_d: -v_w}
        vertical = {K_w: 0.8, K_s: -0.8}
        if event.key in horizontal:
            self.eason.setVelocity(horizontal[event.key], None)
        if event.key in vertical:
            self.eason.setVelocity(None, vertical[event.key])
    
    def update(self, clock):
    	self.baddy.aiMove((self.eason))
        self.eason.update()
        self.baddy.update()
        self.background.update(0)

    def draw(self, screen):
        self.background.draw(screen)
        screen.blit(self.baddy.image, self.baddy.rect)
        screen.blit(self.eason.image, self.eason.rect)
        pygame.display.flip()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
            