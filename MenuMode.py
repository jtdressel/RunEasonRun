'''
Created on 2013-4-4

@author: Eason Chen

Menu mode class, it provides players with different options, players can choose
whichever gamemodes to play, or quit the game. 
'''
from modes import *
from EsAnimation import *
from EsSounds import *
from Eason import *
from Stupid import *

class MenuMode(GameMode):
    background = createBlankImage(size, False)
    IDLE, STARTING = range(2)
    attack_sounds = []
    modes = ['start_mode', 'speed_mode', 'speed_mode']
    def __init__(self):
        GameMode.__init__(self)
        images = loadSprites('options.png', -1, 258, 38)
        self.list_image_skip_line = loadSprites('skip_line.png', -1, 441, 42)
        self.list_image_menu = [[images[0], images[1]], [images[2], images[3]], \
                                [images[4], images[5]], [images[6], images[7]]]
        self.menu_choice = 0
        self.anim_skip_line = Animation(self.list_image_skip_line, 5, True)
        self.x_skip_line, self.y_skip_line = self.pos_skip_line = 100, 280
        self.rect_skip_line = self.list_image_skip_line[0].get_rect()
        self.rect_skip_line.topleft = self.pos_skip_line
        self.rect_menu = [0, 0, 0, 0]
        self.x_menu = [0, 0, 0, 0]
        self.y_menu = [0, 0, 0, 0]
        self.pos_menu = [0, 0, 0, 0]
        self.list_menu = [0, 0, 0, 0]
        for i in range(4):
            self.rect_menu[i] = images[0].get_rect()
            self.x_menu[i], self.y_menu[i] = self.pos_menu[i] = 20, i * 48 + 50
            self.list_menu[i] = self.list_image_menu[i][0]
            self.rect_menu[i].topleft = self.pos_menu[i]
        self.eason = SimpleEason((X + 160, Y))
        self.joe = SimpleStupid((width, Y), X + 160 + 40)
        self.status = MenuMode.IDLE
        for i in range(4):
            name = 'punch' + str(i) + '.wav'
            MenuMode.attack_sounds.append(load_sound(name))
            MenuMode.attack_sounds[i].set_volume(sound_volume)
    
    def enter(self):
        pygame.mouse.set_visible(False)
        MenuMode.background.convert()
        MenuMode.background.fill((255, 255, 255))
        self.menu_choice = 0
        self.eason.stand()
        self.so_far = 0
        self.eason.cnt = 0
        self.eason.setPos((X + 160, Y))
        self.status = MenuMode.IDLE
        self.joe.reset()
        self.skip = False
        self.anim_skip_line.reset()
    
    def exit(self):
        pygame.mouse.set_visible(False)
        self.menu_choice = 0
        self.eason.stand()
        self.so_far = 0
        self.eason.cnt = 0
        self.eason.setPos((X + 160, Y))
        self.status = MenuMode.IDLE
        self.joe.reset()
        self.skip = False
    
    def key_down(self, event):
        if event.key == K_ESCAPE:
            self.quit()
        keys = pygame.key.get_pressed()
        if keys[K_UP] or keys[K_w] or keys[K_a]:
            self.menu_choice = ((self.menu_choice - 1) % 4 + 4) % 4
        if keys[K_DOWN] or keys[K_s] or keys[K_d]:
            self.menu_choice = ((self.menu_choice + 1) % 4 + 4) % 4
        if keys[K_SPACE] or keys[K_RETURN]:
            if self.menu_choice == 3:
                self.quit()
            if self.status == MenuMode.STARTING:
                self.skip = True
            self.status = MenuMode.STARTING
            if self.skip:
                self.switch_to_mode(MenuMode.modes[self.menu_choice])
            self.joe.run()
            self.anim_skip_line.start()
    
    def update(self, clock):
        if self.status == MenuMode.IDLE:
            for i in range(4):
                self.list_menu[i] = self.list_image_menu[i][0]
            self.list_menu[self.menu_choice] = self.list_image_menu[self.menu_choice][1]
        else:
            self.img_skip_line = self.anim_skip_line.image
            self.anim_skip_line.update(pygame.time.get_ticks())
            if self.joe.arrived():
                self.joe.stand()
            if self.joe.anim_stand.done() and self.joe.punchCnt == 0:
                self.joe.punch()
                self.eason.beat()
                MenuMode.attack_sounds[randint(0, 3)].play()
            if self.joe.anim_punch.done() and self.joe.notFinish():
                self.joe.punch()
                self.eason.beat()
                MenuMode.attack_sounds[randint(0, 3)].play()
            if not self.joe.notFinish() and self.joe.notKicked():
                self.joe.kick()
                self.eason.fly()
                MenuMode.attack_sounds[randint(0, 3)].play()
            if self.joe.anim_kick.done() and (not self.joe.anim_esc.started()):
                self.joe.esc()
            
        self.eason.update()
        self.joe.update()
        
        if self.eason.status == SimpleEason.RUN:
            self.switch_to_mode(MenuMode.modes[self.menu_choice])
    
    def draw(self, screen):
        screen.blit(MenuMode.background, (0, 0))
        screen.blit(self.eason.image, self.eason.rect)
        if self.status == MenuMode.IDLE:
            for i in range(4):
                screen.blit(self.list_menu[i], self.rect_menu[i])
        else:
            screen.blit(self.joe.image, self.joe.rect)
            screen.blit(self.img_skip_line, self.rect_skip_line)
        pygame.display.flip()
        
        
        
        
        
        
        
        
        
        