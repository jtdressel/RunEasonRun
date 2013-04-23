"""
Dennis is a reskin of BadGuy

"""
from BadGuy import *
class Dennis(BadGuy):
    def __init__(self, pos, up, lo, level):
        #-----------------------INITIALIZATION---------------------------------
        print "stuff"
        pygame.sprite.Sprite.__init__(self)
        #filename = str((level-1) % 3) + '.png'
        self.images = loadSprites('dennis_0.png', -1, 80, 80)
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
        self.status = BadGuy.STAND
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
        animList = [self.images[6], self.images[7], self.images[8], \
                    self.images[9]]
        self.anim_stand = Animation(animList, 10, True)
        self.anim_attack = []
        animList = [self.images[19], self.images[18]]
        self.anim_attack.append(Animation(animList, 10, False))
        animList = [self.images[17], self.images[16]]
        self.anim_attack.append(Animation(animList, 10, False))
        animList = [self.images[3], self.images[4], self.images[5]]
        self.anim_walk = Animation(animList, 10, True)
        self.anim_beaten = []
        anim = [self.images[10], self.images[11]]
        self.anim_beaten.append(Animation(anim, 16, False))
        anim = [self.images[12], self.images[13], self.images[14]]
        self.anim_beaten.append(Animation(anim, 24, False))
        anim = [self.images[39], self.images[38], self.images[37], self.images[36], \
            self.images[35], self.images[34], self.images[35], self.images[35], \
            self.images[35], self.images[35], self.images[35], self.images[35]]
        self.anim_front_fucked = Animation(anim, 20, False)
        anim = [self.images[49], self.images[48], self.images[47], self.images[46], \
            self.images[45], self.images[44], self.images[45], self.images[45], \
            self.images[45], self.images[45], self.images[45], self.images[45]]
        self.anim_back_fucked = Animation(anim, 20, False)