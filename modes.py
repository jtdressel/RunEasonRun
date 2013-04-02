import pygame
from pygame.locals import *

'''
    copied from class demos, for managing game modes
'''

class ModeManager( object ):
    '''
    A class that manages switching between modes.
    '''
    
    def __init__( self ):
        self.modes = { '__quitting__': kQuittingMode }
        self.current_mode = None
    
    def register_mode( self, mode_name, mode ):
        '''
        Register a new mode with the mode manager.
        '''
        
        assert mode_name not in self.modes
        self.modes[ mode_name ] = mode
        mode._registered_with_manager( self )
    
    def switch_to_mode( self, mode_name ):
        '''
        Switch to the mode named 'mode_name'.
        Calls exit() on the previous mode and enter() on the new mode.
        Passing None for 'mode_name' quits (terminates the game loop).
        
        NOTE: Switching from a mode to the same mode *does* call exit() and enter().
        '''
        ## Handle the special quitting case.
        if mode_name is None: mode_name = '__quitting__'
        
        assert mode_name in self.modes
        
        if self.current_mode is not None:
            self.current_mode.exit()
        
        self.current_mode = self.modes[ mode_name ]
        
        self.current_mode.enter()
    
    def quitting( self ):
        return self.current_mode is kQuittingMode

class GameMode( object ):
    def __init__( self ):
        '''
        A base class for game modes.
        '''
        self.manager = None
    
    def enter( self ):
        '''
        Called when this mode is entered, in case there is set-up to do.
        '''
        pass
    
    def exit( self ):
        '''
        Called when this mode is exited, in case there is tear-down to do
        like stopping music.
        '''
        pass
    
    def switch_to_mode( self, mode_name ):
        '''
        Switches to the specified 'mode_name'.
        
        NOTE: This is simply a convenience method for the current mode which could
              use self.manager.switch_to_mode().
        '''
        assert self.manager is not None
        self.manager.switch_to_mode( mode_name )
    
    def quit( self ):
        '''
        Quits.  This is a convenience method for self.switch_to_mode( None ).
        '''
        self.switch_to_mode( None )
    
    def _registered_with_manager( self, manager ):
        self.manager = manager
    
    def key_down( self, event ):
        pass
    
    def key_up( self, event ):
        pass
    
    def mouse_motion( self, event ):
        pass
    
    def mouse_button_up( self, event ):
        pass
    
    def mouse_button_down( self, event ):
        pass
    
    def update( self, clock ):
        '''
        Called once per frame to update the game state.
        Will be passed the pygame.time.Clock object used by the main loop;
        use the clock object for timing inside this method.
        
        NOTE: It is perfectly OK to ignore the key*() and mouse*() methods above
              and call pygame.mouse.* and pygame.key.* functions here inside update().
        '''
        pass
    
    def draw( self, screen ):
        '''
        Called every time a new frame is to be drawn.
        This method is responsible for clearing the screen and calling
        pygame.display.flip() afterwards.
        Passed the screen pygame.Surface.
        '''
        pass

class SimpleMode( GameMode ):
    '''
    A simple GameMode that fills the screen with green and quits when escape is pressed.
    '''
    
    def key_down( self, event ):
        ## By default, quit when the escape key is pressed.
        if event.key == K_ESCAPE:
            self.quit()
    
    def draw( self, screen ):
        '''
        Called every time a new frame is to be drawn.
        This method is responsible for clearing the screen and calling
        pygame.display.flip() afterwards.
        Use self.screen for access to the screen surface.
        '''
        screen.fill( ( 0, 255, 0 ) )
        pygame.display.flip()

kQuittingMode = GameMode()
