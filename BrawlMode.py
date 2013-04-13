'''
Created on 2013-4-5

@author: Eason Chen
'''
from root import *
from modes import *
from EsAnimation import *
from EsSounds import *
from Eason import *
from Stupid import *
from BadGuy import *
from Background import *
from Fireball import *
from Bar import *

class BrawlMode(GameMode):
    def __init__(self, name, upper, lower):
        self.background = Background(name)
        self.upper_bound, self.lower_bound = upper, lower
        self.eason = BrawlEason(pos, upper, lower)
        self.eason.stand()
        self.fireball = []
        self.bar = BrawlBar()

        #badguy1
        #self.baddy = BadGuy(pos, upper-10, lower-10)
        #self.baddy.stand()
        
    def newBound(self, nu, nl):
        self.eason.newBound(nu, nl)
    
    def enter(self):
        self.eason.update()
        #self.baddy.update()
        pygame.mixer.music.load(os.path.join(kSrcDir, dirBGM, "battle_bgm.ogg"))
        pygame.mixer.music.set_volume(bgm_volume)
        pygame.mixer.music.play(-1)
    
    def exit(self):
        pygame.mixer.music.stop()
    
    def key_down(self, event):
        if event.key == K_ESCAPE:
            self.switch_to_mode('menu_mode')
        horizontal = {K_a: -v_w, K_d: v_w}
        vertical = {K_w: -0.8, K_s: 0.8}
        if event.key in horizontal:
            self.eason.setVelocity(horizontal[event.key], None)
        if event.key in vertical:
            self.eason.setVelocity(None, vertical[event.key])

        keys = pygame.key.get_pressed()
        if keys[K_l]:
            f = self.eason.fireball()
            if f != None:
                self.fireball.append(f)
        elif keys[K_j]:
            self.eason.light_attack()
        elif keys[K_k]:
            self.eason.heavy_attack()
        if keys[K_SPACE]:
            self.eason.jump()
        if keys[K_u]:
            self.eason.levelUp()
        if keys[K_i]:
            self.eason.setLevel(1)
        if keys[K_o]:
            self.eason.expUp()

    def key_up(self, event):
        horizontal = {K_a: v_w, K_d: -v_w}
        vertical = {K_w: 0.8, K_s: -0.8}
        if event.key in horizontal:
            self.eason.setVelocity(horizontal[event.key], None)
        if event.key in vertical:
            self.eason.setVelocity(None, vertical[event.key])
    
    def update(self, clock):
        #self.baddy.aiMove((self.eason))
        self.eason.update()
        #self.baddy.update()
        hp = self.eason.HP / self.eason.max_HP
        mana = self.eason.mana / self.eason.max_mana
        exp = self.eason.exp / (self.eason.level * difficulty)
        self.bar.update(self.eason.level, hp, mana, exp, self.eason.kill_cnt)
        for i in self.fireball:
            i.update()
            if i.outOfSight() or i.exploded():
                self.fireball.pop(self.fireball.index(i))
        self.background.update(0)
        

    def draw(self, screen):
        self.background.draw(screen)
        #screen.blit(self.baddy.image, self.baddy.rect)
        screen.blit(self.eason.image, self.eason.rect)
        self.bar.draw(screen)
        for i in self.fireball:
            screen.blit(i.image, i.rect)
        pygame.display.flip()
