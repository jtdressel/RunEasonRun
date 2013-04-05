'''
Created on 2013-2-8

@author: Eason Chen

Functions for processing images
'''
from root import *

def createBlankImage((width, height), transprt = True):
    image = pygame.Surface((width, height))
    if transprt:
        image.set_colorkey(image.get_at((0, 0)), pygame.RLEACCEL)
    return image

def loadSprites(name, transprt, width, height):
    fullname = os.path.join(kSrcDir, dirSprites, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print "Image doesn't exist: ", fullname
        raise SystemExit, message
    image = image.convert_alpha()
    images = []
    image_width, image_height = image.get_size()
    for j in xrange(int(image_height / height)):
        for i in xrange(int(image_width / width)):
            tmp = image.subsurface(i * width, j * height, width, height)
            if transprt != None:
                if transprt == -1:
                    transprt = tmp.get_at((0, 0))
                tmp.set_colorkey(transprt, pygame.RLEACCEL)
            images.append(tmp)
    return images

def loadImage(name, transprt):
    try:
        image = pygame.image.load(name)
    except pygame.error, message:
        print "Image doesn't exist: ", name
        raise SystemExit, message
    image = image.convert_alpha()
    if transprt != None:
        if transprt == -1:
            transprt = image.get_at((0, 0))
        image.set_colorkey(transprt, pygame.RLEACCEL)
    return image