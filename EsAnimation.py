'''
Created on 2013-2-8

@author: Eason Chen

animation class, creates animation objects using given list of images.
fps and whether or not repeat can be set
'''
from root import *
from EsImage import *

class Animation(pygame.sprite.Sprite):
    '''
        create an animation object for the given list of images
    '''
    def __init__(self, images, fps = 30, repeat = False):
        self._repeat = repeat
        self._images = images
        self._start = False
        self._done = False
        self._delay = 1000 / fps
        self._last_update = pygame.time.get_ticks()
        self.image = createBlankImage(self._images[0].get_size())
        
    def done(self):
        return self._done
    
    def started(self):
        return self._start
    
    def start(self):
        self._start = True
        self._last_update = pygame.time.get_ticks()
        self._done = False
        self._frame = 0
        
    def finish(self):
        self._done = True
        self._start = False
        
    def reset(self):
        self._start = False
        self._frame = 0
        self._done = False
        
    def update(self, t):
        if self._done:
            return 
        if not self._start:
            return 
        if t - self._last_update > self._delay:
            if not self._done:
                self._frame += 1
                
            if self._frame >= len(self._images):
                if self._repeat:
                    self._frame = 0
                else:
                    self._frame -= 1
                    self.finish()
                    
            self._last_update = t
        self.image = self._images[self._frame]
