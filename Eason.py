'''
Created on 2013-2-12

@author: Eason Chen

two classes:
Eason: the private class of Eason, including all the attributes and methods, 
        this is for gameplay
SimpleEason: simple version of Eason class, this is for the animations of the
        starting mode, attributes and methods for gameplay are not included
'''
from root import *
from EsAnimation import *
from EsSounds import *
from EsTimer import *

JMP_ACC = 0.3
DWN_ACC = 3

class Eason(pygame.sprite.Sprite):
    '''REMEMBER EVERY TIME ADD ONE STATUS, ADD ONE NUMBER'''
    RUN, JUMP, ATK, DEAD, DOWN = range(5)
    def __init__(self, pos):
        #--------------------------INITIALIZATION------------------------------
        pygame.sprite.Sprite.__init__(self)
        self.images = loadImage('eason1.png', -1, 80, 80)
        self.sound_jmp = load_sound('jump.wav')
        self.sound_atk = load_sound('attack.wav')
        self.sound_gameover = load_sound('gameover.wav')
        self.sound_levelup = load_sound('levelup.wav')
        self.sound_cd = load_sound('cd.wav')
        self.sound_jmp.set_volume(sound_volume)
        self.sound_atk.set_volume(sound_volume)
        self.sound_gameover.set_volume(sound_volume)
        self.sound_cd.set_volume(sound_volume)
        self.sound_levelup.set_volume(sound_volume)
        self.rect = self.images[0].get_rect()
        
        #-------------------- ATTRIBUTES --------------------------------------
        self.x, self.y = pos
        self.init_x, self.init_y = pos
        self.jmp_cnt = 0
        self.atk_range = 200
        self.v_x, self.v_y = 3, 0
        self.a_x, self.a_y = 0, 0
        self.cd_time = 1900
        self.cd = False
        self.exp = 0
        self.level = 1
        self.CDtimer = CDTimer(self.cd_time)
        
        #----------------------ANIMATIONS--------------------------------------
        animList = [self.images[20], self.images[21]]
        self.anim_run = Animation(animList, 10, True)
        animList = [self.images[60], self.images[61], self.images[62]]
        self.anim_jmp = Animation(animList, 20, False)
        animList = [self.images[60], self.images[61], self.images[63]]
        self.anim_jmp2 = Animation(animList, 20, False)
        animList = [self.images[58], self.images[59], self.images[69]]
        self.anim_down = Animation(animList, 10, True)
        animList = [self.images[0], self.images[1], self.images[2], \
                    self.images[3], self.images[4]]
        self.anim_punch = Animation(animList, 40, False)
        animList = [self.images[5], self.images[6], self.images[7], \
                    self.images[8], self.images[9]]
        self.anim_kick = Animation(animList, 40, False)
        animList = [self.images[31], self.images[32], self.images[33], \
                    self.images[34]]
        self.anim_dead = Animation(animList, 30, False)
        
        #-------------------------START----------------------------------------
        self.status = Eason.RUN
        self.atkDone = True
        
    
    def reset(self):
        self.setLevel(1)
        self.exp = 0
        self.setPos(pos)
        self.atkDone = True
        self.v_x, self.v_y = 3, 0
        self.a_x, self.a_y = 0, 0
    
    def setLevel(self, lv):
        self.level = lv
        self.setCDTime()
        self.setAtkRange()
    
    def levelUp(self):
        if self.level < 20:
            self.level += 1
            self.sound_levelup.play()
            self.setCDTime()
            self.setAtkRange()
    
    def expUp(self):
        self.exp += 1
        if self.exp >= int(self.level * difficulty):
            self.exp = 0
            self.levelUp()
    
    def setCDTime(self):
        self.cd_time = 2000 - 100 * self.level
        self.CDtimer.setTime(self.cd_time)
        self.CDtimer.reset()
    
    def setAtkRange(self):
        self.atk_range = 190 + 10 * self.level
        
    def run(self):
        self.status = Eason.RUN
        self.v_x = 2.63 + 0.37 * self.level
        if not self.anim_run._start:
            self.anim_run.reset()
            self.anim_run.start()
    
    def down(self):
        if self.status == Eason.DEAD:
            return 
        self.status = Eason.DOWN
        self.a_y = DWN_ACC
        if not self.anim_down._start:
            self.anim_down.reset()
            self.anim_down.start()
    
    def jump(self):
        if self.status == Eason.DEAD:
            return
        if self.jmp_cnt == 2:
            return 
        self.sound_jmp.play()
        self.status = Eason.JUMP
        self.v_y = -7
        self.a_y = JMP_ACC
        self.jmp_cnt += 1
        if self.jmp_cnt == 1:
            if not self.anim_jmp._start:
                self.anim_jmp.reset()
                self.anim_jmp.start()
        if self.jmp_cnt == 2:
            if not self.anim_jmp2._start:
                self.anim_jmp2.reset()
                self.anim_jmp2.start()
            
    def setPos(self, pos):
        self.x, self.y = pos
        
    def resetStatus(self):
        self.status = Eason.RUN
        self.v_y = 0
        self.a_y = JMP_ACC
            
    def resetJump(self):
        self.jmp_cnt = 0
        self.anim_jmp.reset()
        self.anim_jmp2.reset()
        
    def move(self):
        t = 1
        self.s_x = self.v_x * t + self.a_x * t * t / 2
        s_y = self.v_y * t + self.a_y * t * t / 2
        self.v_x = self.v_x + self.a_x * t
        self.v_y = self.v_y + self.a_y * t
        self.y += s_y
        if self.status == Eason.DEAD:
            return 
        if self.x <= self.init_x:
            self.x = self.init_x
        else:
            if self.atkDone:
                self.x -= self.v_x / 2
        
    def stepOn(self, floor):
        if self.v_y < 0:
            return False
        hitbox = pygame.Rect(self.x + 20, self.y + 41, 40, 40)
        return hitbox.colliderect(floor.rect)
    
    def stand(self):
        self.v_y = 0
        self.a_y = 0
        
    def fall(self):
        if not self.a_y == DWN_ACC:
            self.a_y = JMP_ACC
            if (not self.isDead()) and (not self.acting()):
                self.status = Eason.JUMP
        
    def stop(self):
        self.a_y = 0
        self.v_x, self.v_y = 0, 0
        
    def isDead(self):
        if self.status == Eason.DEAD:
            return True
        return self.y > height
    
    def gameOver(self):
        if self.status == Eason.DEAD:
            return 
        self.sound_gameover.play()
        self.stop()
        self.status = Eason.DEAD
        self.anim_dead.reset()
        self.anim_dead.start()
        
    def attack(self):
        if self.status == Eason.ATK or self.status == Eason.DEAD:
            return 
        if self.CDtimer.isStart() and (not self.CDtimer.timeUp()):
            return 
        if self.status == Eason.JUMP:
            self.anim_atk = self.anim_kick
            self.kick = True
        else:
            self.anim_atk = self.anim_punch
            self.kick = False
        self.anim_atk.reset()
        self.anim_atk.start()
        self.sound_atk.play()
        self.CDtimer.start()
        self.atkDone = False
        self.status = Eason.ATK
        
    def fixPos(self, y):
        self.y = y - 80
        
    def atkMove(self):
        if self.x - self.init_x < self.atk_range and not self.atkDone:
            self.x += 19 + self.level
        else:
            self.atkDone = True
            if self.kick:
                self.status = Eason.JUMP
            else:
                self.status = Eason.RUN
            
    def acting(self):
        if self.status == Eason.ATK:
            return True
        return False
    
    def hit(self, target):
        if self.status != Eason.ATK and self.status != Eason.DOWN:
            return False
        hitbox = self.rect.inflate(-30, -10)
        return hitbox.colliderect(target.rect.inflate(-20, -5))
    
    def update(self):
        if self.status == Eason.RUN:
            self.image = self.anim_run.image
            self.anim_run.update(pygame.time.get_ticks())
            
        if self.status == Eason.JUMP:
            if self.jmp_cnt == 1:
                self.image = self.anim_jmp.image
                self.anim_jmp.update(pygame.time.get_ticks())
            elif self.jmp_cnt == 2:
                self.image = self.anim_jmp2.image
                self.anim_jmp2.update(pygame.time.get_ticks())
        
        if self.status == Eason.DOWN:
            self.image = self.anim_down.image
            self.anim_down.update(pygame.time.get_ticks())
            
        if self.status == Eason.ATK:
            self.image = self.anim_atk.image
            self.anim_atk.update(pygame.time.get_ticks())
            self.atkMove()
            
        if self.status == Eason.DEAD:
            self.image = self.anim_dead.image
            self.anim_dead.update(pygame.time.get_ticks())
        
        if self.status != Eason.DEAD and self.CDtimer.timeUp():
            self.sound_cd.play()
        
        self.move()
        self.rect.topleft = self.x, self.y
        
class SimpleEason():
    STAND, BEAT, RUN, FLY = range(4)
    def __init__(self, p):
        self.images = loadImage('eason0.png', -1, 80, 80)
        
        animLst = [self.images[1], self.images[2], self.images[3], \
                   self.images[0]]
        self.anim_stand = Animation(animLst, 10, True)
        animLst = [self.images[20], self.images[21]]
        self.anim_run = Animation(animLst, 10, True)
        animLst = [self.images[46], self.images[47], self.images[48]]
        self.anim_beats =[]
        for i in range(3):
            self.anim_beats.append(Animation([self.images[46 + i]], 10, False))
        animLst = []
        for i in range(6):
            animLst.append(self.images[i+30])
        animLst.append(self.images[34])
        self.anim_fly = Animation(animLst, 10, False)
        
        self.setPos(p)
        self.rect = self.images[0].get_rect()
        self.cnt = 0
        
        self.v_x, self.v_y = 0, 0
    
    def setSpeed(self, x, y):
        self.v_x, self.v_y = x, y
        
    def setPos(self, p):
        self.x, self.y = p
    
    def stand(self):
        self.status = SimpleEason.STAND
        self.anim_stand.start()
    
    def run(self):
        self.status = SimpleEason.RUN
        self.anim_run.start()
    
    def beat(self):
        '''
        self.cnt += 1
        if self.cnt > 2:
            self.fly()
            return 
            '''
        self.status = SimpleEason.BEAT
        self.anim_beat = self.anim_beats[randint(0, 2)]
        self.anim_beat.start()
    
    def fly(self):
        self.status = SimpleEason.FLY
        self.anim_fly.start()
        self.setSpeed(-3, 0)
        self.flyPause = SimpleTimer(2000)
        self.stt = 0
    
    def move(self):
        self.x += self.v_x
        self.y += self.v_y
    
    def update(self):
        if self.status == SimpleEason.STAND:
            self.image = self.anim_stand.image
            self.anim_stand.update(pygame.time.get_ticks())
        
        if self.status == SimpleEason.RUN:
            self.image = self.anim_run.image
            self.anim_run.update(pygame.time.get_ticks())
        
        if self.status == SimpleEason.BEAT:
            self.image = self.anim_beat.image
            self.anim_beat.update(pygame.time.get_ticks())
            if self.anim_beat.done():
                self.stand()
        
        if self.status == SimpleEason.FLY:
            self.image = self.anim_fly.image
            self.anim_fly.update(pygame.time.get_ticks())
            if self.anim_fly.done():
                self.setSpeed(0, 0)
                self.setPos(pos)
                if self.flyPause.timeUp():
                    self.run()
        
        self.move()
        self.rect.topleft = self.x, self.y
