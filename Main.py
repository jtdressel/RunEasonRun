'''
Created on 2013-3-2

@author: Eason Chen

The main structure and core logic of this game
'''
from root import *
#from Eason import *
#from Floor import *
#from Stupid import *
#from EsAnimation import *
#from EsImage import *
from EsSounds import *
from modes import *
from StartingMode import *
from SpeedMode import *
from MenuMode import *
from BrawlMode import *
from StoryMode import *

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
    modes.register_mode('story_mode', StoryMode())
    modes.register_mode('speed_mode', SpeedMode('pipe.png', infinite = True))
    modes.register_mode('menu_mode', MenuMode())
    modes.register_mode('brawl_mode', BrawlMode('arena.png', 107, 400, True))
    ## program starts with shell menu
    modes.switch_to_mode('menu_mode')
    pygame.mixer.music.set_volume(bgm_volume)
    ## main loop
    while not modes.quitting():
        clock.tick(FPS)
        ## check input events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                modes.current_mode.key_down(event)
            elif event.type == KEYUP:
                modes.current_mode.key_up(event)
        ## update and then draw
        modes.current_mode.update(clock)
        modes.current_mode.draw(screen)

main()