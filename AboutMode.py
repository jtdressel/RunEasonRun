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
        self.lst = []
    
    def enter(self):
        self.x, self.y = 0, 0
        self.gameover = False
        pygame.mixer.music.load(os.path.join(kSrcDir, dirBGM, 'victory.ogg'))
        pygame.mixer.music.play()
        self.mask = createBlankImage(size, False, (255, 255, 255))
        self.alpha_value = 0
        spriteFile = BrawlEnemies['arena.png']
        pos = [(255, 2700), (460, 1188), (373, 2343), (495, 890), (26, 1477)]
        lst = []
        num = randint(0, 4)
        for i in pos:
            lst.append(BadGuy(i, -3200, 3200, 1, spriteFile[num]))
            num = (num + 1) % 5
        
        lst_eason = [BrawlEason((436, 603), -3200, 3200), BrawlEason((409, 1663), -3200, 3200), \
                    BrawlEason((215, 2700), -3200, 3200), SimpleEason((211, 258))]
        self.lst = lst + lst_eason
        self.lst[len(self.lst) - 1].run()
        for i in self.lst:
            if self.lst.index(i) == len(self.lst) - 1:
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
            if self.lst.index(i) == len(self.lst) - 1:
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
        
        n = len(self.lst) - 1
        if randint(0, 1) == 0:
            self.lst[n-2].heavy_attack()
            self.lst[n-1].heavy_attack()
        else:
            self.lst[n-2].light_attack()
            self.lst[n-1].light_attack()
        for i in range(1, n - 3):
            self.lst[i].attack()
        self.lst[0].beaten()
        
        
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