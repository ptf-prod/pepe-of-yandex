#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import pygame
import pyganim

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"
ANIMATION_DELAY = 100
ANIMATION_LAVA = [('data\\framestiles\lava anim\lava anim0000.png'),
                   ('data\\framestiles\lava anim\lava anim0001.png'),
                   ('data\\framestiles\lava anim\lava anim0002.png'),
                   ('data\\framestiles\lava anim\lava anim0003.png'),
                   ('data\\framestiles\lava anim\lava anim0004.png'),
                   ('data\\framestiles\lava anim\lava anim0005.png'),
                   ('data\\framestiles\lava anim\lava anim0006.png')]
 
class Platform(sprite.Sprite):
    def __init__(self, x, y, filename):
        sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image.load(filename), (32, 32))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class Blank(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((32, 32))
        self.image.fill((50, 150, 255))
        self.image.set_alpha(0)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

class Lava(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((64, 64))
        self.image.set_colorkey(Color("White"))
        self.image.fill(Color("White"))
        self.rect = Rect(x, y, 64, 64)
        boltAnim = []
        for anim in ANIMATION_LAVA:
            boltAnim.append((pygame.transform.scale(image.load(anim), (32, 32)), ANIMATION_DELAY))
        self.boltAnimLava = pyganim.PygAnimation(boltAnim)
        self.boltAnimLava.play()
        self.boltAnimLava.blit(self.image, (x - 32, y - 32))  # По-умолчанию, стоим


class Spikes(Platform):
    def __init__(self, x, y, filename):
        super().__init__(x, y, filename)
        self.image.fill((0, 0, 0))


class Ice(Platform):
    def __init__(self, x, y, filename):
        super().__init__(x, y, filename)
        self.image.fill((0, 255, 0))


class Teleport(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.image = Surface((32, 32))
        self.image.fill((0, 0, 255))
