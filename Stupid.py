'''
Created on 2013-2-13

@author: Eason Chen

two classes included:
Stupid: primary class of Stupid, complete attribtes and methods included, this
        is for gameplay
SimpleStupid: this class is for animations in the starting mode, main gameplay
        functions are not included
'''
from root import *
from EsAnimation import *
from EsSounds import *
from EsTimer import *

class Stupid(pygame.sprite.Sprite):
    STAND, ATK, DEAD = range(3)
    def __init__(self, pos):
        #-----------------------INITIALIZATION---------------------------------
        pygame.sprite.Sprite.__init__(self)
        self.images = loadImage('0.png', -1, 80, 80)
        self.rect = self.images[0].get_rect()
        
        #-----------------------ATTRIBUTES-------------------------------------
        self.x, self.y = pos
        self.width, self.height = 80, 80
        self.status = Stupid.STAND
        
        #-----------------------ANIMATIONS-------------------------------------
        animList = [self.images[6], self.images[7], self.images[8], \
                    self.images[9]]
        self.anim_stand = Animation(animList, 10, True)
        animList = [self.images[19], self.images[18], self.images[17], \
                    self.images[16]]
        self.anim_attack = Animation(animList, 10, False)
        animList = [self.images[36], self.images[37], self.images[34], \
                    self.images[35]]
        self.anim_dead = Animation(animList, 10, False)
        
        self.stand()
        
    def outOfSight(self):
        return self.x + self.width < 0
    
    def stand(self):
        self.status = Stupid.STAND
        self.anim_stand.reset()
        self.anim_stand.start()
        
    def attack(self):
        self.status = Stupid.ATK
        self.anim_attack.reset()
        self.anim_attack.start()
        
    def die(self):
        self.status = Stupid.DEAD
        self.anim_dead.reset()
        self.anim_dead.start()
        
    def isDead(self):
        return self.status == Stupid.DEAD
        
    def hit(self, target):
        hitbox = self.rect.inflate(-35, -20)
        return hitbox.colliderect(target.rect.inflate(-35, -20))
        
    def update(self, x):
        if self.status == Stupid.STAND:
            self.image = self.anim_stand.image
            self.anim_stand.update(pygame.time.get_ticks())
            
        if self.status == Stupid.ATK:
            self.image = self.anim_attack.image
            self.anim_attack.update(pygame.time.get_ticks())
            if self.anim_attack._done:
                self.status = Stupid.STAND
        
        if self.status == Stupid.DEAD:
            self.image = self.anim_dead.image
            self.anim_dead.update(pygame.time.get_ticks())
        
        self.x += x
        self.rect.topleft = self.x, self.y

class SimpleStupid():
    IDLE, RUN, ESC, PUNCH, KICK, STAND = range(6)
    def __init__(self, p, x):
        self.setPos(p)
        self.initP = p
        self.images = loadImage('0.png', -1, 80, 80)
        self.rect = self.images[0].get_rect()
        
        animLst = [self.images[27], self.images[28], self.images[29], \
                   self.images[28]]
        self.anim_run = Animation(animLst, 10, True)
        animLst = [self.images[6], self.images[7], self.images[8], \
                   self.images[9]]
        self.anim_stand = Animation(animLst, 10, False)
        self.anim_atks = []
        animLst = [self.images[17], self.images[16]]
        self.anim_atks.append(Animation(animLst, 15, False))
        animLst = [self.images[19], self.images[18]]
        self.anim_atks.append(Animation(animLst, 15, False))
        animLst = [self.images[32], self.images[31], self.images[30]]
        self.anim_atks.append(Animation(animLst, 15, False))
        animLst = [self.images[15], self.images[14], self.images[14],\
                    self.images[15]]
        self.anim_kick = Animation(animLst, 10, False)
        self.anim_punch = self.anim_atks[0]
        animLst = [self.images[0], self.images[1], self.images[2], self.images[1]]
        self.anim_esc = Animation(animLst, 10, True)
        self.v_x, self.v_y = 0, 0
        self.dest = x
        self.status = SimpleStupid.IDLE
        self.punchCnt = 0
        self.kicked = False
    
    def reset(self):
        self.punchCnt = 0
        self.kicked = False
        self.anim_stand.reset()
        self.anim_run.reset()
        self.anim_kick.reset()
        self.anim_esc.reset()
        for i in self.anim_atks:
            i.reset()
        self.setPos(self.initP)
        self.setSpeed(0, 0)
    
    def run(self):
        self.status = SimpleStupid.RUN
        self.anim_run.start()
        self.setSpeed(-3, 0)
    
    def esc(self):
        self.status = SimpleStupid.ESC
        self.anim_esc.start()
        self.setSpeed(4, 0)
    
    def stand(self):
        self.setSpeed(0, 0)
        self.status = SimpleStupid.STAND
        self.anim_stand.start()
    
    def setPos(self, p):
        self.x, self.y = p
    
    def setSpeed(self, x, y):
        self.v_x, self.v_y = x, y
    
    def notFinish(self):
        if self.punchCnt < hitTime:
            return True
        return False
    
    def punch(self):
        self.punchCnt += 1
        self.status = SimpleStupid.PUNCH
        self.anim_punch = self.anim_atks[randint(0, 2)]
        self.anim_punch.start()
    
    def notKicked(self):
        return not self.kicked
    
    def kick(self):
        self.kicked = True
        self.status = SimpleStupid.KICK
        self.anim_kick.start()
    
    def move(self):
        self.x += self.v_x
        self.y += self.v_y
        if self.x > width:
            self.setSpeed(0, 0)
    
    def arrived(self):
        if self.status == SimpleStupid.RUN and \
        math.fabs(self.x - self.dest) < math.fabs(self.v_x):
            self.setPos((self.dest, self.y))
            return True
        return False
    
    def update(self):
        if self.status == SimpleStupid.RUN:
            self.image = self.anim_run.image
            self.anim_run.update(pygame.time.get_ticks())
        
        if self.status == SimpleStupid.STAND:
            self.image = self.anim_stand.image
            self.anim_stand.update(pygame.time.get_ticks())
        
        if self.status == SimpleStupid.PUNCH:
            self.image = self.anim_punch.image
            self.anim_punch.update(pygame.time.get_ticks())
        
        if self.status == SimpleStupid.KICK:
            self.image = self.anim_kick.image
            self.anim_kick.update(pygame.time.get_ticks())
        
        if self.status == SimpleStupid.ESC:
            self.image = self.anim_esc.image
            self.anim_esc.update(pygame.time.get_ticks())
            
        self.move()
        self.rect.topleft = self.x, self.y
