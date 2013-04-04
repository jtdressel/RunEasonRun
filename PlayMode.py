'''
Created on 2013-3-3

@author: Eason Chen

PlayMode class
'''
from root import *
from modes import *
from EsAnimation import *
from Eason import *
from Floor import *
from Stupid import *
from Board import *

class PlayMode(GameMode):
    background = pygame.Surface(size)
    attack_sounds = []
    
    def __init__(self):
        GameMode.__init__(self)
        self.eason = Eason(pos)
        PlayMode.background.convert()
        for i in range(4):
            name = 'punch' + str(i) + '.wav'
            PlayMode.attack_sounds.append(load_sound(name))
            PlayMode.attack_sounds[i].set_volume(sound_volume)
        self.so_far = 0
        self.board = Board()
        self.eason.run()
        
    def enter(self):
        ## initializations when entering this mode
        pygame.mixer.music.load(os.path.join(kSrcDir, dirBGM, "beethoven_virus.ogg"))
        pygame.mixer.music.set_volume(bgm_volume)
        pygame.mixer.music.play(-1)
        pygame.mouse.set_visible(False)
        PlayMode.background.fill((255, 255, 255))
        self.eason.reset()
        floor = Floor((0, Y + 80), (700, 2))
        self.floors = [floor]
        self.joes = []
        self.eason.run()
        self.so_far = 0
        self.board.reset()
        self.eason.update()
        
    def exit(self):
        ## clean-ups when exiting
        pygame.mixer.music.stop()
        self.floors = []
        self.joes = []
        pygame.mouse.set_visible(True)
    
    def key_down(self, event):
        ## check input events
        if event.key == K_ESCAPE:
            self.switch_to_mode('start_mode')
        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            self.eason.jump()
        if keys[K_a]:
            self.eason.attack()
        if keys[K_k]:
            self.eason.drop()
    
    def add_new_floor(self):
        last_floor = self.floors[len(self.floors) - 1]
        dist = width - last_floor.x - last_floor.width
        ## set probabilities of the appearance of floors and joes
        P = 0
        Q = 3 * self.eason.level + 20
        if dist > 320:
            P = 100
        elif dist > 200:
            P = 50
        elif dist > 100:
            P = 15
        elif dist > 50:
            P = 5
        if randint(1, 100) <= P:
            new_floor = Floor((width + 1, Y + 80 + randint(-60, 60)), \
                              (randint(50, 1500), 2))
            self.floors.append(new_floor)
            if new_floor.width > 640:
                Q = 100
            if randint(1, 100) <= Q and new_floor.width > 80:
                self.joes.append(Stupid((new_floor.x + \
                                        randint(0, new_floor.width - 80), \
                                        new_floor.y - 80)))
    
    ## supporting method
    def out_of_sight(self):
        if self.floors[0].out_of_sight():
            tmp = self.floors.pop(0)
            del tmp
        if self.joes:
            if self.joes[0].outOfSight():
                tmp = self.joes.pop(0)
                del tmp
    
    ## set the accelerate if Eason is not stepping on any floors
    def fall(self):
        found = False
        for i in self.floors:
            if self.eason.stepOn(i):
                self.eason.stand()
                self.eason.fixPos(i.y)
                if (not self.eason.acting()) and (not self.eason.isDead()):
                    self.eason.run()
                self.eason.resetJump()
                found = True
                break
        if not found:
            self.eason.fall()
    
    ## Eason beats Joe or be beaten
    def battle(self):
        for i in self.joes:
            if (not i.isDead()) and self.eason.hit(i):
                PlayMode.attack_sounds[randint(0, 3)].play()
                i.die()
                self.eason.expUp()
            if (not i.isDead()) and i.hit(self.eason):
                if not self.eason.isDead():
                    i.attack()
                    PlayMode.attack_sounds[randint(0, 3)].play()
                    self.eason.gameOver()
    
    ## switch to startmode if Eason dies
    def check_death(self, clock):
        if self.eason.isDead():
            pygame.mixer.music.stop()
            self.eason.gameOver()
            self.so_far += clock.get_time()
            if self.so_far > 3000:
                self.switch_to_mode('start_mode')
    
    ## update all the elements of this mode
    def update(self, clock):
        self.add_new_floor()
        self.out_of_sight()
        self.fall()
        self.battle()
        self.check_death(clock)
        self.eason.update()
        for i in self.floors:
            i.update(-self.eason.s_x)
        for i in self.joes:
            i.update(-self.eason.s_x)
        self.board.update(self.eason.level, self.eason.v_x / 3 )
    
    ## draw elements onto the given screen
    def draw(self, screen):
        screen.blit(PlayMode.background, (0, 0))
        screen.blit(self.board.image, self.board.rect)
        for i in self.floors:
            screen.blit(i.image, i.rect)
        for i in self.joes:
            screen.blit(i.image, i.rect)
        screen.blit(self.eason.image, self.eason.rect)
        pygame.display.flip()
        
        
