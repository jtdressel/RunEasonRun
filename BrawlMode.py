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
from Background import *

class BrawlMode(GameMode):
    def __init__(self, name, upper, lower):
        self.background = Background(name)
        self.upper_bound, self.lower_bound = upper, lower
        self.eason = BrawlEason(pos, upper, lower)
        self.eason.stand()
        
    def newBound(self, nu, nl):
        self.eason.newBound(nu, nl)
    
    def enter(self):
        self.eason.update()
    
    def key_down(self, event):
        if event.key == K_ESCAPE:
            self.switch_to_mode('menu_mode')
        horizontal = {K_a: -v_w, K_d: v_w}
        vertical = {K_w: -0.8, K_s: 0.8}
        if event.key in horizontal:
            self.eason.setVelocity(horizontal[event.key], None)
        if event.key in vertical:
            self.eason.setVelocity(None, vertical[event.key])
        keys = pygame.key.get_pressed()
        if keys[K_j] and keys[K_k]:
            self.eason.fireball()
        elif keys[K_j]:
            self.eason.light_attack()
        elif keys[K_k]:
            self.eason.heavy_attack()
        if keys[K_SPACE]:
            self.eason.jump()

    def key_up(self, event):
        horizontal = {K_a: v_w, K_d: -v_w}
        vertical = {K_w: 0.8, K_s: -0.8}
        if event.key in horizontal:
            self.eason.setVelocity(horizontal[event.key], None)
        if event.key in vertical:
            self.eason.setVelocity(None, vertical[event.key])
    
    def update(self, clock):
        self.eason.update()
        self.background.update(0)
    
    def draw(self, screen):
        self.background.draw(screen)
        screen.blit(self.eason.image, self.eason.rect)
        pygame.display.flip()