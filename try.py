import pygame
from pygame.locals import *
from sys import exit
 
pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)
clock = pygame.time.Clock()
A = pygame.Surface((20, 20)).convert()
A.fill((255, 0, 0))
rect = A.get_rect()

x, y = 0, 0
move = {K_LEFT: 0, K_RIGHT: 0, K_UP: 0, K_DOWN: 0}
hh = {K_LEFT: 0, K_RIGHT: 0}
vv = {K_UP: 0, K_DOWN: 0}

class Vec():
    def __init__(self, x, y):
        self.x, self.y = x, y
    
    def add(self, v1):
        self.x += v1.x
        self.y += v1.y
    
    def subtract(self, v1):
        self.x -= v1.x
        self.y -= v1.y
    
    def st(self, x, y):
        self.x, self.y = x, y

vec = Vec(0, 0)
vh = Vec(1, 0)
vv = Vec(0, 1)
velocity = 1

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            keys = pygame.key.get_pressed()
            if event.key == K_a:
                vec.subtract(vh)
            if event.key == K_d:
                vec.add(vh)
            if event.key == K_w:
                vec.subtract(vv)
            if event.key == K_s:
                vec.add(vv)
            if keys[K_j]:
                velocity = 3
            
        elif event.type == KEYUP:
            if event.key == K_a:
                vec.add(vh)
            if event.key == K_d:
                vec.subtract(vh)
            if event.key == K_j:
                velocity = 1
            
            if event.key == K_w:
                vec.add(vv)
            if event.key == K_s:
                vec.subtract(vv)
    
    vx = vec.x * velocity
    vy = vec.y * velocity
    
    x += vx
    y += vy
    
    rect.topleft = x, y
    
    
    screen.fill((255,255,255))
    screen.blit(A, rect)
    pygame.display.update()