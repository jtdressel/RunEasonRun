'''
Created on 2013-3-2

@author: Eason Chen

The main structure and core logic of this game
'''
from root import *
from Eason import *
from Floor import *
from Stupid import *
from EsAnimation import *
from EsImage import *
from EsSounds import *
from modes import *
from StartingMode import *
from PlayMode import *

def loadIcon(name):
    fullname = os.path.join(kSrcDir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print "Image doesn't exist: ", fullname
        raise SystemExit, message
    return image

def main():
    ## initialize pygame
    pygame.init()
    pygame.display.set_icon(loadIcon('icon.png'))
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(globals['window_title'])
    clock = pygame.time.Clock()
    
    ## set up the modes
    modes = ModeManager()
    ## register the two modes
    modes.register_mode('start_mode', StartingMode())
    modes.register_mode('play_mode', PlayMode())
    ## program starts with startingmode
    modes.switch_to_mode('start_mode')
    ## main loop
    while not modes.quitting():
        clock.tick(FPS)
        ## check input events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                modes.current_mode.key_down(event)
        ## update and then draw
        modes.current_mode.update(clock)
        modes.current_mode.draw(screen)

main()