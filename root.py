'''
Created on 2013-2-8

@author: Eason Chen

Initializations of global variables
'''
import os, pygame, math, time, json
from pygame.locals import *
from random import randint

## initialize global variables
kSrcDir = 'src'
kGlobals = 'globals.json'
dirSprites = 'sprites'
dirSounds = 'sounds'
dirBGM = 'bgm'
dirImg = 'img'
globals = json.load(open(os.path.join(kSrcDir, kGlobals)))
FPS = globals['fps']
size = width, height = globals['screen_size']
white = 255, 255, 255
pos = X, Y = globals['pos']
bgm_volume = globals['bgm_volume']
sound_volume = globals['sound_volume']
difficulty = globals['difficulty']
hitTime = globals['hit_time']
v_w = globals['v_walk']
v_r = globals['v_run']
