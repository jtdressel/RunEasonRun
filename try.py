import pygame
from pygame.locals import *
from sys import exit
 
pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)
A = pygame.Surface((20, 20)).convert()
A.fill((255, 0, 0))
rect = A.get_rect()
 
x, y = 0, 0
move = {K_LEFT: 0, K_RIGHT: 0, K_UP: 0, K_DOWN: 0}

hitbox = None

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key in move:
                move[event.key] = .3
            else:
                keys = pygame.key.get_pressed()
                if keys[K_j]:
                    A.fill((4, 4, 100))
            
        elif event.type == KEYUP:
            if event.key in move:
                move[event.key] = 0
        
            
    x -= move[K_LEFT]
    x += move[K_RIGHT]
    y -= move[K_UP]
    y += move[K_DOWN]
    
    
    rect.topleft = x, y
    
    screen.fill((255,255,255))
    screen.blit(A, rect)
    pygame.display.update()