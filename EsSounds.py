'''
Created on 2013-2-8

@author: Lemon

functions for processing sounds
'''
from root import *

def load_sound(file):
    class NoneSound:
        def play(self): pass
    
    '''
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    '''
    fullname = os.path.join(kSrcDir, dirSounds, file)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print "Sound file doesn't exist: ", fullname
        raise SystemExit, message
    return sound