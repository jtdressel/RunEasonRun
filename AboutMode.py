'''
Created on 2013-4-21

@author: Eason Chen
'''
from root import *
from EsAnimation import *
from EsSounds import *
from modes import *
from Eason import *
from Stupid import *
from BadGuy import *

class AboutMode(GameMode):
    def __init__(self, v):
        self.x, self.y = 0, 0
        self.v = -v
        self.image = loadImage('about.png', None)
        self.alpha_value = 0
        self.lst = [BrawlEason((436, 603), -3200, 3200), BrawlEason((409, 1663), -3200, 3200), \
                    BadGuy((460, 1088), -3200, 3200, 1), BadGuy((373, 2343), -3200, 3200, 1), \
                    BrawlEason((215, 2700), -3200, 3200), BadGuy((255, 2700), -3200, 3200, 1), \
                    SimpleEason((211, 258))]
    
    def enter(self):
        self.x, self.y = 0, 0
        self.gameover = False
        pygame.mixer.music.load(os.path.join(kSrcDir, dirBGM, 'victory.ogg'))
        pygame.mixer.music.play()
        self.mask = createBlankImage(size, False, (255, 255, 255))
        self.alpha_value = 0
        self.lst = [BrawlEason((436, 603), -3200, 3200), BrawlEason((409, 1663), -3200, 3200), \
                    BadGuy((460, 1088), -3200, 3200, 1), BadGuy((373, 2343), -3200, 3200, 1), \
                    BadGuy((255, 2700), -3200, 3200, 1), BrawlEason((215, 2700), -3200, 3200), \
                    SimpleEason((211, 258))]
        self.lst[6].run()
        self.lst[5].direction = BrawlEason.RIGHT
        self.lst[4].direction = BadGuy.LEFT
        for i in self.lst:
            if self.lst.index(i) == 6:
                continue
            for j in i.sound_atk:
                j.set_volume(0)
            for j in i.attack_sounds:
                j.set_volume(0)
        for i in self.lst:
            i.update()
    
    def exit(self):
        pygame.mixer.music.stop()
        for i in self.lst:
            if self.lst.index(i) == 6:
                continue
            for j in i.sound_atk:
                j.set_volume(sound_volume)
            for j in i.attack_sounds:
                j.set_volume(sound_volume)
        del self.lst
    
    def key_down(self, event):
        self.gameover = True
        pygame.mixer.music.fadeout(2000)
    
    def update(self, clock):
        if self.y >= -2800:
            self.y += self.v
            for i in self.lst:
                i.y += self.v
        
        if randint(0, 1) == 0:
            self.lst[1].heavy_attack()
            self.lst[5].heavy_attack()
        else:
            self.lst[1].light_attack()
            self.lst[5].light_attack()
        self.lst[3].attack()
        self.lst[4].beaten()
        
        
        for i in self.lst:
            i.update()
        
        if self.gameover:
            self.alpha_value += 2
            if self.alpha_value > 255:
                self.alpha_value = 255
                self.switch_to_mode('menu_mode')
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        if self.lst:
            for i in self.lst:
                i.draw(screen)
        self.mask.set_alpha(self.alpha_value)
        screen.blit(self.mask, (0, 0))
        pygame.display.flip()