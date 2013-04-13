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
from Fireball import *

JMP_ACC = 0.3
DRP_ACC = 3

class Eason(pygame.sprite.Sprite):
    '''REMEMBER EVERY TIME ADD ONE STATUS, ADD ONE NUMBER'''
    RUN, JUMP, ATK, DEAD, DROP = range(5)
    def __init__(self, pos):
        #--------------------------INITIALIZATION------------------------------
        pygame.sprite.Sprite.__init__(self)
        self.images = loadSprites('eason0.png', -1, 80, 80)
        self.sound_jmp = load_sound('jump.wav')
        self.sound_atk = []
        self.sound_atk.append(load_sound('attack0.wav'))
        self.sound_atk.append(load_sound('attack1.wav'))
        self.sound_gameover = load_sound('gameover.wav')
        self.sound_levelup = load_sound('levelup.wav')
        self.sound_cd = load_sound('cd.wav')
        self.sound_jmp.set_volume(sound_volume)
        for i in self.sound_atk:
            i.set_volume(sound_volume)
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
        self.anim_DROP = Animation(animList, 10, True)
        animList = [self.images[0], self.images[1], self.images[2], \
                    self.images[3], self.images[4]]
        self.anim_punch = Animation(animList, 40, False)
        animList = [self.images[5], self.images[6], self.images[7], \
                    self.images[8], self.images[9]]
        self.anim_kick = Animation(animList, 25, False)
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
    
    def drop(self):
        if self.status == Eason.DEAD:
            return 
        self.status = Eason.DROP
        self.a_y = DRP_ACC
        if not self.anim_DROP._start:
            self.anim_DROP.reset()
            self.anim_DROP.start()
        if not self.atkDone:
            self.atkDone = True
    
    def jump(self):
        if self.status == Eason.DEAD:
            return
        if self.jmp_cnt == 2:
            return 
        if not self.atkDone:
            self.atkDone = True
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
        if not self.a_y == DRP_ACC:
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
        self.sound_atk[randint(0, 1)].play()
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
        if self.status != Eason.ATK and self.status != Eason.DROP:
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
        
        if self.status == Eason.DROP:
            self.image = self.anim_DROP.image
            self.anim_DROP.update(pygame.time.get_ticks())
            
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
        
class BrawlEason(Eason):
    WALK, JUMP, ATK, DEAD, HIT, STAND = range(6)
    RIGHT, LEFT = range(2)
    def __init__(self, pos, up, lo):
        Eason.__init__(self, pos)
        self.images1 = loadSprites('eason1.png', -1, 80, 80)
        animList = [self.images[23], self.images[24], self.images[25], self.images[26], \
                    self.images[25], self.images[24]]
        self.anim_walk = Animation(animList, 10, True)
        animList = [self.images[36], self.images[37], self.images[38], \
                   self.images[18]]
        self.anim_stand = Animation(animList, 10, True)
        self.anim_punch = []
        animList = [self.images[14], self.images[15], self.images[16]]
        self.anim_punch.append(Animation(animList, 20, False))
        animList = [self.images[10], self.images[11], self.images[12]]
        self.anim_punch.append(Animation(animList, 20, False))
        animList = [self.images1[13], self.images1[14], self.images1[15], self.images1[16], \
                    self.images1[17], self.images1[18], self.images1[19], self.images1[29], \
                    self.images1[28], self.images1[27], self.images1[26], self.images1[25], self.images1[24]]
        self.anim_heavy_attack = Animation(animList, 35, False)
        animList = [self.images1[20], self.images1[21], self.images1[21], self.images1[21], self.images1[21],\
                     self.images1[22], self.images1[22], self.images1[22], self.images1[23]]
        self.anim_jump_punch = Animation(animList, 50, False)
        self.anim_fireball = []
        animList = [self.images1[0], self.images1[1], self.images1[2], self.images1[3], \
                    self.images1[4], self.images1[0]]
        self.anim_fireball.append(Animation(animList, 25, False))
        animList = [self.images1[5], self.images1[6], self.images1[7], self.images1[8], \
                    self.images1[9], self.images1[0]]
        self.anim_fireball.append(Animation(animList, 25, False))
        
        self.direction = BrawlEason.RIGHT
        self.v_x = 0
        self.upperBound, self.lowerBound = up, lo
        self.damage = 0
        self.cd_atk = CDTimer(100)
        self.acc = 0
        self.v = 0
        self.gnd_y = self.y
        self.kill_cnt = 0
        self.max_HP = 100
        self.max_mana = 100
        self.HP = 100
        self.mana = 100
    
    def isLeft(self):
        return self.direction == BrawlEason.LEFT
    
    def newBound(self, nu, nl):
        self.upperBound, self.lowerBound = nu, nl
    
    def setVelocity(self, vx = None, vy = None):
        if vx != None:
            self.v_x += vx
        if vy != None:
            self.v_y += vy
    
    def killUp(self):
        self.kill_cnt += 1
    
    def expUp(self):
        Eason.expUp(self)
        self.killUp()
    
    def levelUp(self):
        self.level += 1
        self.sound_levelup.play()
        self.max_HP += 50
        self.max_mana += 20
        self.HP = self.max_HP
        self.mana = self.max_mana
    
    def setLevel(self, lv):
        self.level = lv
        self.max_HP = 100 + 50 * (lv - 1)
        self.max_mana = 100 + 20 * (lv - 1)
        self.HP = self.max_HP
        self.mana = self.max_mana
        self.exp = 0
    
    def jump(self):
        if self.jmp_cnt > 1:
            return 
        self.jmp_cnt += 1
        self.status = BrawlEason.JUMP
        self.acc = JMP_ACC
        self.v = -6
        if self.jmp_cnt == 1:
            self.anim_jmp.reset()
            self.anim_jmp.start()
            self.gnd_y = self.y
        else:
            self.anim_jmp2.reset()
            self.anim_jmp2.start()
    
    def walk(self):
        if self.status == BrawlEason.ATK:
            return
        self.status = BrawlEason.WALK
        if not self.anim_walk.started():
            self.anim_walk.start()
        if self.v_x > 0:
            self.direction = BrawlEason.RIGHT
        elif self.v_x < 0:
            self.direction = BrawlEason.LEFT

    def light_attack(self):
        if self.cd_atk.isStart() and not self.cd_atk.timeUp():
            return 
        if self.status == BrawlEason.DEAD or self.status == BrawlEason.ATK:
            return 
        else:
            if self.isFalling():
                self.anim_atk = self.anim_jump_punch
            else:
                self.anim_atk = self.anim_punch[randint(0, 1)]
        self.anim_atk.reset()
        self.anim_atk.start()
        self.sound_atk[randint(0, 1)].play()
        self.atkDone = False
        self.status = BrawlEason.ATK
        self.damage = 10 + randint(-4, 4) + self.level
        self.cd_atk.setTime(1)
        
    def heavy_attack(self):
        if self.cd_atk.isStart() and not self.cd_atk.timeUp():
            return 
        if self.status == BrawlEason.DEAD or self.status == BrawlEason.ATK:
            return
        else:
            if self.isFalling():
                self.anim_atk = self.anim_kick
            else:
                self.anim_atk = self.anim_heavy_attack
            
        self.anim_atk.reset()
        self.anim_atk.start()
        self.sound_atk[randint(0, 1)].play()
        self.status = BrawlEason.ATK
        self.damage = (10 + randint(-4, 4) + self.level) * 2
        self.cd_atk.setTime(100)
    
    def fireball(self):
        fb = None
        if self.cd_atk.isStart() and not self.cd_atk.timeUp():
            return fb
        if self.status == BrawlEason.ATK or self.isFalling():
            return fb
        if self.mana < 20:
            return fb
        self.status = BrawlEason.ATK
        self.anim_atk = self.anim_fireball[randint(0, 1)]
        self.anim_atk.reset()
        self.anim_atk.start()
        self.damage = 0
        self.cd_atk.setTime(0)
        self.mana -= 20
        if self.isLeft():
            fb = Fireball((self.x - 35, self.y + 5), \
                         Fireball.LEFT, self.fireballDamage())
        else:
            fb = Fireball((self.x + 35, self.y + 5), \
                         Fireball.RIGHT, self.fireballDamage())
        return fb
    
    def fireballDamage(self):
        return 50 + randint(-10, 10) + self.level * 2

    def stand(self):
        if self.status == BrawlEason.STAND:
            return 
        self.status = BrawlEason.STAND
        self.anim_stand.reset()
        self.anim_stand.start()
        self.damage = 0
    
    def isJumping(self):
        if self.status == BrawlEason.JUMP:
            return True
        return False
    
    def isMoving(self):
        if self.v_x == 0 and self.v_y == 0:
            return False
        return True

    def isAttack(self):
        if self.status != BrawlEason.ATK:
            return False
        return True
    
    def stepOn(self):
        if self.gnd_y < self.y:
            self.y = self.gnd_y
            self.acc = 0
            self.v = 0
            self.jmp_cnt = 0
    
    def isFalling(self):
        if not self.acc:
            return False
        return True
    
    def getHitBox(self):
        if self.status != BrawlEason.ATK:
            return None
        hitBox = None
        ## -------------hitBox of light attacks-----------------
        if self.anim_atk.image == self.images[11] or \
        self.anim_atk.image == self.images[12] or \
        self.anim_atk.image == self.images[15] or \
        self.anim_atk.image == self.images[16]:
            x = 50
            y = self.y + 40
            if self.direction == BrawlEason.LEFT:
                x = 80 - x - 30
            x += self.x
            hitBox = pygame.Rect(x, y, 30, 15)
        
        ## ------------hitBox of kicks------------------
        if self.anim_atk.image == self.images[8] or\
        self.anim_atk.image == self.images[9]:
            x = 40
            y = self.y + 40
            if self.direction == BrawlEason.LEFT:
                x = 80 - x - 30
            x += self.x
            hitBox = pygame.Rect(x, y, 30, 16)
            
        ## -------------hitBox of heavy attacks-------------
        if self.anim_atk.image == self.images1[14] or \
        self.anim_atk.image == self.images1[16] or self.anim_atk.image == self.images1[17] or \
        self.anim_atk.image == self.images1[19] or self.anim_atk.image == self.images1[27] or\
        self.anim_atk.image == self.images1[26]:
            x = 40
            y = self.y + 40
            if self.direction == BrawlEason.LEFT:
                x = 80 - x - 36
            x += self.x
            hitBox = pygame.Rect(x, y, 36, 16)
        
        ## -------------hitBox of jump attacks--------------
        if self.anim_atk.image == self.images1[22] or self.anim_atk.image == self.images1[23]:
            x = 30
            y = self.y + 50
            if self.direction == BrawlEason.LEFT:
                x = 80 - x - 25
            x += self.x
            hitBox = pygame.Rect(x, y, 25, 20)
        
        return hitBox
            
    
    def move(self):
        t = 1
        ver_dist = self.v * t + self.acc * t * t / 2
        self.v = self.v + self.acc * t
        s_x = self.v_x * t + self.a_x * t * t / 2
        s_y = self.v_y * t + self.a_y * t * t / 2
        self.v_x = self.v_x + self.a_x * t
        self.v_y = self.v_y + self.a_y * t
        self.y += s_y
        self.x += s_x
        self.gnd_y += s_y
        self.y += ver_dist
        if self.x < -40:
            self.x = -40
        if self.x > width - 40:
            self.x = width - 40
        if self.y > self.lowerBound - 80:
            self.y = self.lowerBound - 80
            self.gnd_y = self.lowerBound - 81
        if self.y < self.upperBound - 80 and not self.isFalling():
            self.y = self.upperBound - 79
            self.gnd_y = self.upperBound - 79
    
    def restore(self):
        if self.HP < self.max_HP:
            self.HP += 0.01
        if self.mana < self.max_mana:
            self.mana += 0.05
    
    def update(self):
        # Eason.update(self)
        ## ----------------------update animations------------------------
        if self.status == BrawlEason.JUMP:
            if self.jmp_cnt == 1:
                self.image = self.anim_jmp.image
                self.anim_jmp.update(pygame.time.get_ticks())
            elif self.jmp_cnt == 2:
                self.image = self.anim_jmp2.image
                self.anim_jmp2.update(pygame.time.get_ticks())
            if self.direction == BrawlEason.LEFT:
                self.image = pygame.transform.flip(self.image, 1, 0)
            
        
        if self.status == BrawlEason.WALK:
            self.image = self.anim_walk.image
            if self.direction == BrawlEason.LEFT:
                self.image = pygame.transform.flip(self.image, 1, 0)
            self.anim_walk.update(pygame.time.get_ticks())
            
        if self.status == BrawlEason.STAND:
            self.image = self.anim_stand.image
            if self.direction == BrawlEason.LEFT:
                self.image = pygame.transform.flip(self.image, 1, 0)
            self.anim_stand.update(pygame.time.get_ticks())

        if self.status == BrawlEason.ATK:
            self.image = self.anim_atk.image
            if self.direction == BrawlEason.LEFT:
                self.image = pygame.transform.flip(self.image, 1, 0)
            self.anim_atk.update( pygame.time.get_ticks())
            
        ## ---------------------------------------------------------------
        
        if not self.isFalling() and not self.isAttack():
            self.stand()
        if self.isMoving() and not self.isAttack():
            if not self.isFalling():
                self.walk()
        if self.isAttack() and self.anim_atk.done():
            if not self.isFalling():
                self.stand()
            self.cd_atk.start()
            
        self.stepOn()
        self.move()
        self.restore()
        self.rect.topleft = self.x, self.y

class SimpleEason():
    STAND, BEAT, RUN, FLY = range(4)
    def __init__(self, p):
        self.images = loadSprites('eason0.png', -1, 80, 80)
        
        animLst = [self.images[36], self.images[37], self.images[38], \
                   self.images[18]]
        self.anim_stand = Animation(animLst, 8, True)
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
        self.setSpeed(0, 0)
    
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
        self.setSpeed(-3.5, 0)
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
