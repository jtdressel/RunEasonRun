"""
Julian class will include attributes and methods for enemies and AI control of them

Children of Julian class will have additional abilities not containted in Julian
"""
from BadGuy import *
class Julian(BadGuy):
    def __init__(self, pos, up, lo, level):
        #-----------------------INITIALIZATION---------------------------------
        pygame.sprite.Sprite.__init__(self)
        #filename = str((level-1) % 3) + '.png'
        self.images = loadSprites('julian_0.png', -1, 80, 100)
        self.images1 = loadSprites('julian_1.png', -1, 80, 100)
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
        animList = [self.images2[49],self.images2[48],self.images2[47],self.images2[45]]
        energy_charge_list = [self.images2[39],self.images2[38],self.images2[37],self.images2[46],self.images2[45],self.images2[44]]
        #animList = [self.images1[6], self.images1[6], self.images1[6], self.images1[6], self.images1[6]] 
        energy_uppercut_list=[self.images2[32],self.images2[31],self.images2[30]]
        energy_punch_list=[self.images2[29],self.images2[28],self.images2[27]]
        self.anim_stand = Animation(energy_uppercut_list, 10, True)

        self.anim_attack = []
        
        animList = [self.images[20],self.images[17], self.images[18], self.images[19]]
        self.anim_attack.append(Animation(animList, 10, False))
        
        animList = [self.images[20], self.images[20]]
        self.anim_attack.append(Animation(animList, 10, False))

        animList = [self.images[3], self.images[4], self.images[5]]
        self.anim_walk = Animation(animList, 10, True)

        self.anim_beaten = []
        anim = [self.images[10], self.images[11]]
        self.anim_beaten.append(Animation(anim, 16, False))
        anim = [self.images[12], self.images[13], self.images[14]]

        self.anim_beaten.append(Animation(anim, 24, False))
        
        
        #anim = [self.images[39], self.images[38], self.images[37], self.images[36], \
        #    self.images[35], self.images[34], self.images[35], self.images[35], \
        #    self.images[35], self.images[35], self.images[35], self.images[35]]
            
        anim = [self.images1[3], self.images1[2], self.images1[1], self.images1[1], self.images1[1]]    
            
            
        self.anim_front_fucked = Animation(anim, 20, False)
        #anim = [self.images[49], self.images[48], self.images[47], self.images[46], \
        #    self.images[45], self.images[44], self.images[45], self.images[45], \
        #    self.images[45], self.images[45], self.images[45], self.images[45]]
        anim = [self.images1[6], self.images1[6], self.images1[6], self.images1[6], self.images1[6]]
        self.anim_back_fucked = Animation(anim, 20, False)
