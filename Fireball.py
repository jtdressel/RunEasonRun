'''
Created on 2013-4-12

@author: Eason Chen
'''
from root import *
from EsAnimation import *
from EsSounds import *

class Fireball(pygame.sprite.Sprite):
    START, FLY, EXPLODE = range(3)
    LEFT, RIGHT = range(2)
    def __init__(self, pos, dir, dmg):
        self.x, self.y = self.pos = pos
        self.direction = dir
        self.images = loadSprites('fireball.png', -1, 80, 80)
        self.rect = self.images[0].get_rect()
        anim = [self.images[0]]
        self.anim_start = Animation(anim, 10, False)
        anim = [self.images[1], self.images[2], self.images[3], self.images[2]]
        self.anim_fly = Animation(anim, 15, True)
        anim = [self.images[4], self.images[5], self.images[6], self.images[7]]
        self.anim_explode = Animation(anim, 30, False)
        self.status = Fireball.START
        self.v = 7
        self.damage = dmg
        if self.direction == Fireball.LEFT:
            self.v = -self.v
        self.anim_start.start()
    
    def move(self):
        self.x += self.v
    
    def fly(self):
        if self.status == Fireball.FLY:
            return 
        self.status = Fireball.FLY
        self.anim_fly.reset()
        self.anim_fly.start()
    
    def outOfSight(self):
        if self.x > width:
            return True
        if self.x + 80 < 0:
            return True
        return False
    
    def exploded(self):
        return self.anim_explode.done()
    
    def explode(self):
        self.v = 0
        self.status = Fireball.EXPLODE
        self.anim_explode.reset()
        self.anim_explode.start()
    
    def update(self):
        if self.status == Fireball.START:
            if self.anim_start.done():
                self.fly()
            self.image = self.anim_start.image
            self.anim_start.update(pygame.time.get_ticks())
        
        if self.status == Fireball.FLY:
            self.image = self.anim_fly.image
            self.anim_fly.update(pygame.time.get_ticks())
        
        if self.status == Fireball.EXPLODE:
            self.image = self.anim_explode.image
            self.anim_explode.update(pygame.time.get_ticks())
        
        if self.direction == Fireball.LEFT:
            self.image = pygame.transform.flip(self.image, 1, 0)
        
        self.move()
        self.rect.topleft = self.x, self.y
        
        
            