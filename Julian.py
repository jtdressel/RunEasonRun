"""
Julian class will include attributes and methods for enemies and AI control of them

Children of Julian class will have additional abilities not containted in Julian
"""
from BadGuy import *
class Julian(BadGuy):
    '''
Fight Script:

While at full health:
* Punch
* Uppercut

Whie betwen full health and half health:
* Energy Punch
* Energy Uppercut
* Punch
* Uppercut

After half health:
* Energy Beam
* Energy Punch
* Energy Uppercut
* Punch
* Uppercut


Animation List:
* Standing
* Walking
* Punch
* Uppercut
* Energy Chargeup
* Energy Punch
* Energy Uppercut
* Laser Beam Attack
* beaten
* front fucked
* back fucked
'''
    def __init__(self, pos, up, lo, level):
        #-----------------------INITIALIZATION---------------------------------
        pygame.sprite.Sprite.__init__(self)
        #filename = str((level-1) % 3) + '.png'
        self.images = loadSprites('julian_0.png', -1, 80, 100)
        
        self.imagesCol = loadSprites('julian_col.png', -1, 200, 405)
        self.images2 = loadSprites('julian_2.png', -1, 80, 100)
        print self.images2.__len__()      
        self.rect = self.images[0].get_rect()
        self.attack_sounds = []
        for i in range(4):
            name = 'punch' + str(i) + '.wav'
            self.attack_sounds.append(load_sound(name))
            self.attack_sounds[i].set_volume(sound_volume)
        self.sound_atk = []
        self.sound_atk.append(load_sound('attack0.wav'))
        self.sound_atk.append(load_sound('attack1.wav'))
        
        #-----------------------ATTRIBUTES-------------------------------------
        self.x, self.y = pos
        self.init_x, self.init_y = pos
        self.v_x, self.v_y = 0, 0
        self.a_x, self.a_y = 0, 0
        self.width, self.height = 80, 80
        self.status = None
        self.level = level
        self.direction = BadGuy.LEFT
        self.upperBound, self.lowerBound = up , lo
        self.damage = 0
        self.cd_atk = CDTimer(100)
        self.max_HP = 400 + 100 * (level - 1)
        self.HP = self.max_HP
        self.rect_body = pygame.Rect(0, 0, 27, 57)
        self.cd_hit = CDTimer(20)
        self.cd_action = CDTimer(200)
        self.cd_action.start()
        self.dmg_period = CDTimer(1000)
        self.dmg_taken = 0
        self.deadFlag = False
        self.vec = EsVector(0, 0)
        self.velocity = v_w
        
        #-----------------------ANIMATIONS-------------------------------------
        energy_charge_list = [self.images2[39],self.images2[38],self.images2[37],self.images2[46],self.images2[45],self.images2[44]]
        energy_uppercut_list=[self.images2[32],self.images2[31],self.images2[30]]
        energy_punch_list=[self.images2[29],self.images2[28],self.images2[27]]
        waling_list  = [self.images[3], self.images[4], self.images[5]]
        standing_list=[self.images[6],self.images[7],self.images[8]]
        uppercut_list = [self.images[28],self.images[27],self.images[26]]
        uppercut_punch = [self.images[19],self.images[18]]
        punch_list = [self.images[20],self.images[17], self.images[18], self.images[19]]

        self.images1 = loadSprites('julian_1-b.png', -1, 100, 100)
        self.images1_2 = loadSprites('julian_1-c.png', -1, 100, 100)
        self.images1_1 = loadSprites('julian_1-b.png', -1, 100, 100)
        self.images1_0 = loadSprites('julian_1.png', -1, 140, 118)# works for zero
        anim_front = [self.images1_0[0],self.images1_1[0],self.images1_2[0]]#inefecient, but dealing wiht a malformed sprite sheet
        #self.anim_stand = Animation(standing_list , 10, True)
        self.anim_front_fucked = Animation(anim_front, 20, False)
        self.anim_stand = Animation(standing_list, 10, True)
        self.anim_attack = []
        self.anim_attack.append(Animation(uppercut_punch, 10, False))
        
        self.anim_attack.append(Animation(punch_list, 10, False))

        
        self.anim_walk = Animation(waling_list, 10, True)

        self.anim_beaten = []
        anim = [self.images[10], self.images[11]]
        self.anim_beaten.append(Animation(anim, 16, False))
        anim = [self.images[12], self.images[13], self.images[14]]
        self.anim_beaten.append(Animation(anim, 24, False))
        
        
            


        #anim = [self.images1[6], self.images1[6], self.images1[6], self.images1[6], self.images1[6]]
        self.anim_back_fucked = Animation(energy_charge_list, 20, False)

    def aiMove(self, target):
        self.turnFace(target)
        if self.withinRange(48, target):
            self.setTarget(self.x, self.y)
            if self.cd_action.timeUp():
                P = 50
                if randint(1, 100) <= P:
                    pass#self.attack()
                self.cd_action.start()
        elif self.checkForTarget(target):
            self.setTarget(target.x, target.gnd_y)
        else:
            self.setTarget(self.x, self.y)
        self.moveToTarget()
        
    def attack(self):
        if self.isDead():
            return 
        if self.cd_atk.isStart() and not self.cd_atk.timeUp():
            return 
        if self.status == BadGuy.DEAD or self.status == BadGuy.ATK:
            return
        self.anim_atk = self.anim_attack[randint(0, 1)]
        self.anim_atk.reset()
        self.anim_atk.start()
        self.sound_atk[randint(0, 1)].play()
        self.status = BadGuy.ATK
        self.damage = 6 + randint(-2, 2) + self.level
        self.cd_atk.setTime(500)