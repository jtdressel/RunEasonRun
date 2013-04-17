'''
Created on 2013-4-16

@author: Eason Chen
'''
from root import *
from modes import *
from BrawlMode import *
from SpeedMode import *

class StoryMode(GameMode):
    def __init__(self):
        self.ptr = 0
        self.lst_mode = [self, SpeedMode('city.png', False), BrawlMode('street.png', 224, 385, False), \
                         SpeedMode('industrial.png', False), BrawlMode('warehouse.png', 290, 380, False)]
        self.mode_name = ['menu_mode', 'city_run', 'street_fight', 'industrial_run', 'warehouse_fight']
        self.modes = ModeManager()
        for i in range(5):
            self.modes.register_mode(self.mode_name[i], self.lst_mode[i])
<<<<<<< HEAD
=======

>>>>>>> c51e79e43ee84a6de7b31d5816137009688553c1
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
            
            self.level = self.lst_mode[self.ptr].eason.level
        self.ptr += 1
        if self.ptr > 4:
            self.ptr = 1
        self.lst_mode[self.ptr].setLevel(self.level)
        self.modes.switch_to_mode(self.mode_name[self.ptr])
    
    def exit(self):
        pygame.mixer.music.stop()
        
    def key_down(self, event):
        if event.key == K_ESCAPE:
            self.ptr = 0
            self.level = 1
            self.switch_to_mode('menu_mode')
            return 
        
        self.modes.current_mode.key_down(event)
            
    
    def key_up(self, event):
        self.modes.current_mode.key_up(event)
    
    def update(self, clock):
        self.modes.current_mode.update(clock)
    
    def draw(self, screen):
        self.modes.current_mode.draw(screen)
