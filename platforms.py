#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import pygame
import pyganim

from animation import *
from constants import *


PLAT_COLOR = "#FF6262"
ANIMATION_DELAY = 100
ANIMATION_LAVA = ['data/framestiles/lava anim/lava anim0000.png',
                  'data/framestiles/lava anim/lava anim0001.png',
                  'data/framestiles/lava anim/lava anim0002.png',
                  'data/framestiles/lava anim/lava anim0003.png',
                  'data/framestiles/lava anim/lava anim0004.png']

ANIMATION_TELEPORT = ['data/framestiles/portal anim/finish-portal anim0000.png',
                      'data/framestiles/portal anim/finish-portal anim0001.png',
                      'data/framestiles/portal anim/finish-portal anim0002.png',
                      'data/framestiles/portal anim/finish-portal anim0003.png',
                      'data/framestiles/portal anim/finish-portal anim0004.png',
                      'data/framestiles/portal anim/finish-portal anim0005.png',
                      'data/framestiles/portal anim/finish-portal anim0006.png']

tiles_textures = {}


class Platform(sprite.Sprite):
    WIDTH = 32
    HEIGHT = 32
    WIDTH_2 = WIDTH // 2
    HEIGHT_4 = HEIGHT // 4

    def __init__(self, x, y, filename):
        self.hurts = False
        sprite.Sprite.__init__(self)
        if filename is not None:
            if filename not in tiles_textures:
                tiles_textures[filename] = \
                    pygame.transform.scale(image.load(filename).convert_alpha(), (64, 64))
            self.image = tiles_textures[filename]
        else:
            self.image = Surface((Platform.WIDTH, Platform.HEIGHT))
            self.image.set_alpha(0)
        self.rect = Rect(x, y, Platform.WIDTH * 2, Platform.HEIGHT * 2)
        self.hitbox = pygame.Rect(x + PLAT_W // 2, y + PLAT_H // 2,
                                  PLAT_W, PLAT_H)


class Blank(Platform):
    def __init__(self, x, y):
        super().__init__(x, y, None)


class Lava(Platform):
    def __init__(self, x, y):
        super().__init__(x, y, None)
        self.hurts = True
        self.image = Surface((128, 128))
        self.image.fill(Color("White"))
        self.image.set_colorkey(Color("White"))
        self.rect = Rect(x - 32, y - 30, 64, 64)
        bolt_anim = []
        for anim in ANIMATION_LAVA:
            bolt_anim.append((pygame.transform.scale(image.load(anim), (128, 128)),
                              ANIMATION_DELAY))
        self.boltAnimLava = pyganim.PygAnimation(bolt_anim)
        self.boltAnimLava.play()
        self.boltAnimLava.blit(self.image, (0, 0))

    def update(self, *args):
        self.image.fill(Color("White"))
        self.boltAnimLava.blit(self.image, (0, 0))

class Spikes(Platform):
    def __init__(self, x, y, filename):
        super().__init__(x, y, filename)
        self.hurts = True


class Ice(Platform):
    def __init__(self, x, y, filename):
        super().__init__(x, y, filename)
        self.hurts = True


class Teleport(Platform):
    def __init__(self, x, y):
        super().__init__(x, y, None)
        self.rect = Rect(x - 256, y - 348, PLAT_W, PLAT_H)
        self.image = Surface((512, 512))
        self.image.fill(Color("White"))
        self.image.set_colorkey(Color("White"))
        bolt_anim = []
        for anim in ANIMATION_TELEPORT:
            bolt_anim.append((pygame.transform.scale(image.load(anim), (512, 512)),
                              ANIMATION_DELAY))
        self.boltAnimTeleport = pyganim.PygAnimation(bolt_anim)
        self.boltAnimTeleport.play()
        self.boltAnimTeleport.blit(self.image, (0, 0))

    def update(self, *args):
        self.image.fill(Color("White"))
        self.boltAnimTeleport.blit(self.image, (0, 0))
