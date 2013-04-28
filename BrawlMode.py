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
    FIGHT, VICTORY = range(2)
    def __init__(self, name, upper, lower, infinite = False):
        GameMode.__init__(self)
        self.infinite = infinite
        if self.infinite == True:
            self.background = Background('arena.png')
            self.spriteFile = BrawlEnemies['arena.png']
        elif name == 'finalboss0.png':
            self.background = AnimatedBackground('finalboss0.png', 'finalboss1.png')
            self.spriteFile = 'julian'
        else:
            self.background = Background(name)
            self.spriteFile = BrawlEnemies[name]
        self.upper_bound, self.lower_bound = upper, lower
        self.eason = BrawlEason(pos, upper, lower)
        self.eason.stand()
        self.fireball = []
        self.bar = BrawlBar(infinite)
        self.so_far = 0
        self.status = BrawlMode.FIGHT

        
        #badguy1
    def spawn_enemy(self, numEnemy, maxLv):
        self.baddy = []
        if self.spriteFile != 'julian':
            for i in range(numEnemy):
                j = randint(0,len(self.spriteFile)-1)
                x = (i % 2) * width - 40
                y = randint(self.upper_bound-80, self.lower_bound-80)
                lv = randint(1, maxLv)
                self.baddy.append(BadGuy((x, y), self.upper_bound, self.lower_bound, lv, self.spriteFile[j]))
                #self.baddy.append(Julian((x, y), self.upper_bound, self.lower_bound, lv ))
                self.baddy[i].stand()
        else:
            x = width - 40
            y = randint(self.upper_bound-80, self.lower_bound-80)
            lv = randint(1, maxLv)
            self.baddy.append(Julian((x, y), self.upper_bound, self.lower_bound, lv ))
            self.baddy[0].stand()

    def newBound(self, nu, nl):
        self.eason.newBound(nu, nl)
    
    def setLevel(self, lv):
        self.eason.setLevel(lv)
    
    def enter(self):
        self.trans = False
        self.mask = createBlankImage(size, False, (0, 0, 0))
        self.alpha_value = 0
        self.status = BrawlMode.FIGHT
        if self.infinite:
            self.eason.reset()
        self.eason.update()
        self.spawn_enemy(2 + self.eason.level, self.eason.level)
        for i in self.baddy:
            i.update()
        
        hp = self.eason.HP / self.eason.max_HP
        mana = self.eason.mana / self.eason.max_mana
        exp = self.eason.exp / (self.eason.level * difficulty)
        self.bar.update(self.eason.level, hp, mana, exp, self.eason.kill_cnt)
        
        #self.baddy.update()
        pygame.mixer.music.load(os.path.join(kSrcDir, dirBGM, "battle_bgm.ogg"))
        pygame.mixer.music.set_volume(bgm_volume)
        if self.infinite:
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.play(-1, 3.5)
        pygame.mouse.set_visible(False)
        self.so_far = 0
        self.gameover = False
    
    def exit(self):
        pygame.mixer.music.stop()
        pygame.key.set_repeat()
    
    def key_down(self, event):
        if event.key == K_ESCAPE:
            self.trans = True
            self.gameover = True

        keys = pygame.key.get_pressed()
        vh = EsVector(1, 0)
        vv = EsVector(0, 1)
        ## ---------------control of Eason------------------
        if event.key == K_a:
            self.eason.moveLeft()
        if event.key == K_d:
            self.eason.moveRight()
        if event.key == K_w:
            self.eason.moveUp()
        if event.key == K_s:
            self.eason.moveDown()
        if keys[K_LSHIFT]:
            self.eason.speedUp()
        if keys[K_j] and keys[K_k]:
            if not self.infinite and self.status == BrawlMode.VICTORY:
                self.trans = True
            else:
                f = self.eason.fireball()
                if f != None:
                    self.fireball.append(f)
        elif keys[K_j]:
            if not self.infinite and self.status == BrawlMode.VICTORY:
                self.trans = True
            else:
                self.eason.light_attack()
        elif keys[K_k]:
            if not self.infinite and self.status == BrawlMode.VICTORY:
                self.trans = True
            else:
                self.eason.heavy_attack()
        if keys[K_SPACE]:
            if not self.infinite and self.status == BrawlMode.VICTORY:
                self.trans = True
            else:
                self.eason.jump()
        
        if keys[K_i]:
            self.eason.setLevel(1)
        if keys[K_o]:
            self.eason.levelUp()
        if keys[K_v]:
            for i in self.baddy:
                i.HP = 0
    
    def key_up(self, event):
        vh = EsVector(1, 0)
        vv = EsVector(0, 1)
        if event.key == K_a:
            self.eason.moveRight()
        if event.key == K_d:
            self.eason.moveLeft()
        if event.key == K_w:
            self.eason.moveDown()
        if event.key == K_s:
            self.eason.moveUp()
        if event.key == K_LSHIFT:
            self.eason.slowDown()
        
    
    def battle(self, a, b):
        r = a.getHitBox()
        dmg = a.damage
        hit = False
        if r != None:
            hit = b.hit(r, dmg, a.x)
        return hit
    
    def checkVictory(self, clock):
        vic = True
        for i in self.baddy:
            if not i.isDead():
                vic = False
                break
        if vic:
            self.so_far += clock.get_time()
            if self.status != BrawlMode.VICTORY and not self.infinite:
                pygame.mixer.music.load(os.path.join(kSrcDir, dirBGM, "fightwin.ogg"))
                pygame.mixer.music.play(-1)
                self.status = BrawlMode.VICTORY
            if self.so_far > 2000:
                if self.infinite:
                    self.spawn_enemy(2 + self.eason.level, self.eason.level)
                    self.so_far = 0
    
    def checkDeath(self, clock):
        if self.eason.isDead():
            pygame.mixer.music.stop()
            self.gameover = True
            self.trans = True
    
    def update(self, clock):
        self.checkDeath(clock)
        self.checkVictory(clock)
        for i in self.baddy:
            i.aiMove(self.eason)
        self.eason.update()
        
        for i in self.baddy:
            self.battle(self.eason, i)
        
        hp = self.eason.HP / self.eason.max_HP
        mana = self.eason.mana / self.eason.max_mana
        exp = self.eason.exp / (self.eason.level * difficulty)
        self.bar.update(self.eason.level, hp, mana, exp, self.eason.kill_cnt)
        for i in self.fireball:
            i.update()
            for j in self.baddy:
                hit = self.battle(i, j)
                if hit:
                    i.explode()
        for i in self.fireball:
            if i.outOfSight() or i.exploded():
                self.fireball.pop(self.fireball.index(i))
                
        for i in self.baddy:
            i.update()
            self.battle(i, self.eason)
            if i.isDead() and not i.deadFlag:
                i.deadFlag = True
                self.eason.expUp()
        self.background.update(0)
        if self.trans:
            self.alpha_value += 3
            if self.alpha_value > 255:
                self.alpha_value = 255
                self.switch_to_mode('menu_mode')

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
        for i in self.baddy:
            lst.append(i)
        for i in self.fireball:
            lst.append(i)
        lst.sort(key = cmp)
        for i in lst:
            i.draw(screen)
        self.bar.draw(screen)
        self.mask.set_alpha(self.alpha_value)
        screen.blit(self.mask, (0, 0))
        pygame.display.flip()

def cmp(obj):
    return obj.y
