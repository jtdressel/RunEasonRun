'''
Created on 2013-4-16

@author: Eason Chen
'''
from root import *
from modes import *
from BrawlMode import *
from SpeedMode import *
from AboutMode import *

class StoryMode(GameMode):
    def __init__(self):
        self.ptr = 0
        self.lst_mode = [self, SpeedMode('city.png', False), BrawlMode('street.png', 224, 385, False), \
                         SpeedMode('industrial.png', False), BrawlMode('warehouse.png', 290, 380, False), \
                         SpeedMode('dark0.png', False), BrawlMode('finalboss0.png', 302, 400, False), \
                         AboutMode(0.5)]
        self.mode_name = ['menu_mode', 'city_run', 'street_fight', 'industrial_run', 'warehouse_fight', \
                          'lightning_run', 'lightning_fight', 'credit']
        self.modes = ModeManager()
        for i in range(8):
            self.modes.register_mode(self.mode_name[i], self.lst_mode[i])
        self.level = 1
    
    def enter(self):
        if not self.ptr:
            self.level = 1
        else:
            if self.lst_mode[self.ptr].gameover:
                self.ptr = 0
                self.level = 1
                self.switch_to_mode('menu_mode')
                return 
            if self.mode_name[self.ptr] != 'credit':
                self.level = self.lst_mode[self.ptr].eason.level
        self.ptr += 6
        if self.ptr > 7:
            self.switch_to_mode('menu_mode')
            self.ptr = 0
            self.level = 1
            return 
        if self.mode_name[self.ptr] != 'credit':
            self.lst_mode[self.ptr].setLevel(self.level)
        self.modes.switch_to_mode(self.mode_name[self.ptr])
    
    def exit(self):
        pygame.mixer.music.stop()
        
    def key_down(self, event):
        '''
        if event.key == K_ESCAPE:
            self.ptr = 0
            self.level = 1
            self.switch_to_mode('menu_mode')
            return 
        '''
        self.modes.current_mode.key_down(event)
            
    
    def key_up(self, event):
        self.modes.current_mode.key_up(event)
    
    def update(self, clock):
        self.modes.current_mode.update(clock)
    
    def draw(self, screen):
        self.modes.current_mode.draw(screen)
