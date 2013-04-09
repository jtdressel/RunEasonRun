import pygame
from pygame.locals import *
from sys import exit
 
pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)
background = pygame.Surface((20, 20)).convert()
background.fill((255, 0, 0))
 
x, y = 0, 0
move = {K_LEFT: 0, K_RIGHT: 0, K_UP: 0, K_DOWN: 0}
 
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key in move:
                move[event.key] = 1
        elif event.type == KEYUP:
            if event.key in move:
                move[event.key] = 0
            
    x -= move[K_LEFT]
    x += move[K_RIGHT]
    y -= move[K_UP]
    y += move[K_DOWN]
    screen.fill((255,255,255))
    screen.blit(background, (x,y))
    pygame.display.update()