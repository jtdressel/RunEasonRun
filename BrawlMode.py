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
        self.baddy = BadGuy(pos, upper, lower, 5)
        self.baddy.stand()
    
    def spawn_enemy(self):
        pass
    
    def newBound(self, nu, nl):
        self.eason.newBound(nu, nl)
    
    def enter(self):
        self.eason.update()
        self.baddy.update()
        #self.baddy.update()
        pygame.mixer.music.load(os.path.join(kSrcDir, dirBGM, "battle_bgm.ogg"))
        pygame.mixer.music.set_volume(bgm_volume)
        #pygame.mixer.music.play(-1)
        pygame.mouse.set_visible(False)
    
    def exit(self):
        pygame.mixer.music.stop()
        pygame.key.set_repeat()
    
    def key_down(self, event):
        if event.key == K_ESCAPE:
            self.switch_to_mode('menu_mode')

        keys = pygame.key.get_pressed()
        vh = EsVector(1, 0)
        vv = EsVector(0, 1)
        if event.key == K_a:
            self.baddy.moveLeft()
        if event.key == K_d:
            self.baddy.moveRight()
        if event.key == K_w:
            self.baddy.moveUp()
        if event.key == K_s:
            self.baddy.moveDown()
        
        if keys[K_l]:
            self.baddy.attack()
        
        if keys[K_j] and keys[K_k]:
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
            self.baddy.resurge()
        if keys[K_i]:
            self.eason.setLevel(1)
        if keys[K_o]:
            self.eason.levelUp()
    
    def key_up(self, event):
        vh = EsVector(1, 0)
        vv = EsVector(0, 1)
        if event.key == K_a:
            self.baddy.moveRight()
        if event.key == K_d:
            self.baddy.moveLeft()
        if event.key == K_w:
            self.baddy.moveDown()
        if event.key == K_s:
            self.baddy.moveUp()
        if event.key == K_l:
            self.eason.slowDown()
        
    
    def battle(self, a, b):
        r = a.getHitBox()
        dmg = a.damage
        hit = False
        if r != None:
            hit = b.hit(r, dmg, a.x)
        return hit
    
    def update(self, clock):
        #self.baddy.aiMove((self.eason))
        self.eason.update()
        
        self.battle(self.eason, self.baddy)
        
        hp = self.eason.HP / self.eason.max_HP
        mana = self.eason.mana / self.eason.max_mana
        exp = self.eason.exp / (self.eason.level * difficulty)
        self.bar.update(self.eason.level, hp, mana, exp, self.eason.kill_cnt)
        for i in self.fireball:
            i.update()
            hit = self.battle(i, self.baddy)
            if hit:
                i.explode()
        for i in self.fireball:
            if i.outOfSight() or i.exploded():
                self.fireball.pop(self.fireball.index(i))
        self.baddy.update()
        self.battle(self.baddy, self.eason)
        if self.baddy.isDead() and not self.baddy.deadFlag:
            self.baddy.deadFlag = True
            self.eason.expUp()
        self.background.update(0)

    def draw(self, screen):
        self.background.draw(screen)
        #screen.blit(self.baddy.image, self.baddy.rect)
        '''
        screen.blit(self.eason.image, self.eason.rect)
        screen.blit(self.tmp.image, self.tmp.rect)
        self.bar.draw(screen)
        for i in self.fireball:
            i.draw(screen)
        '''
            
        lst = []
        lst.append(self.eason)
        lst.append(self.baddy)
        for i in self.fireball:
            lst.append(i)
        lst.sort(key = cmp)
        for i in lst:
            i.draw(screen)
        self.bar.draw(screen)
        pygame.display.flip()

def cmp(obj):
    return obj.y