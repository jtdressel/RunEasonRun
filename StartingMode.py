'''
Created on 2013-3-3

@author: Eason Chen

Starting mode class, one of the gamemodes
'''
#from root import *
from modes import *
from EsAnimation import *
from EsSounds import *
from Eason import *
from Stupid import *

class StartingMode(GameMode):
    background = pygame.Surface(size)
    IDLE, STARTING = range(2)
    attack_sounds = []
    def __init__(self):
        GameMode.__init__(self)
        self.lines = loadImage('starting_line.png', -1, 441, 42)
        self.line_x, self.line_y = self.line_pos = 100, 280
        self.anim_line = Animation(self.lines, 5, True)
        self.rect_line = self.lines[0].get_rect()
        self.rect_line.topleft = self.line_pos
        self.eason = SimpleEason((X + 150, Y))
        self.joe = SimpleStupid((width, Y), X + 150 + 40)
        self.status = StartingMode.IDLE
        for i in range(4):
            name = 'punch' + str(i) + '.wav'
            StartingMode.attack_sounds.append(load_sound(name))
            StartingMode.attack_sounds[i].set_volume(sound_volume)
        
    def enter(self):
        pygame.mouse.set_visible(False)
        StartingMode.background.convert()
        StartingMode.background.fill((255, 255, 255))
        self.anim_line.start()
        self.eason.stand()
        self.so_far = 0
        self.eason.cnt = 0
        self.eason.setPos((X + 150, Y))
        self.status = StartingMode.IDLE
        self.joe.reset()
        #pygame.mixer.music.play(-1)
        
    def exit(self):
        pygame.mouse.set_visible(True)
    
    def key_down(self, event):
        if event.key == K_ESCAPE:
            self.quit()
        else:
            if self.status == StartingMode.STARTING:
                return 
            self.status = StartingMode.STARTING
            self.joe.run()
        
    def update(self, clock):
        self.img_line = self.anim_line.image
        self.anim_line.update(pygame.time.get_ticks()) 
        
        if self.joe.arrived():
            self.joe.stand()
        if self.joe.anim_stand.done() and self.joe.punchCnt == 0:
            self.joe.punch()
            self.eason.beat()
            StartingMode.attack_sounds[randint(0, 3)].play()
        if self.joe.anim_punch.done() and self.joe.notFinish():
            self.joe.punch()
            self.eason.beat()
            StartingMode.attack_sounds[randint(0, 3)].play()
        if not self.joe.notFinish() and self.joe.notKicked():
            self.joe.kick()
            self.eason.fly()
            StartingMode.attack_sounds[randint(0, 3)].play()
        if self.joe.anim_kick.done() and (not self.joe.anim_esc.started()):
            self.joe.esc()
            
        self.eason.update()
        self.joe.update()
        
        if self.eason.status == SimpleEason.RUN:
            self.switch_to_mode('play_mode')
        
        
    def draw(self, screen):
        screen.blit(StartingMode.background, (0, 0))
        screen.blit(self.eason.image, self.eason.rect)
        if self.status == StartingMode.IDLE:
            screen.blit(self.img_line, self.rect_line)
        if self.status == StartingMode.STARTING:
            screen.blit(self.joe.image, self.joe.rect)
        pygame.display.flip()
