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
                  'data/framestiles/lava anim/lava anim0004.png',
                  'data/framestiles/lava anim/lava anim0005.png',
                  'data/framestiles/lava anim/lava anim0006.png']

ANIMATION_TELEPORT = ['data/framestiles/portal anim/finish-portal anim0000.png',
                      # 'data/framestiles/portal anim/finish-portal anim0001.png',
                      'data/framestiles/portal anim/finish-portal anim0002.png',
                      'data/framestiles/portal anim/finish-portal anim0003.png',
                      'data/framestiles/portal anim/finish-portal anim0004.png',
                      'data/framestiles/portal anim/finish-portal anim0005.png',
                      'data/framestiles/portal anim/finish-portal anim0006.png']

tiles_textures = {}


class Platform(sprite.Sprite):

    def __init__(self, x, y, filename):
        super().__init__()
        self.dmg = False
        if filename is not None:
            if filename not in tiles_textures:
                tiles_textures[filename] = \
                    pygame.transform.scale(image.load(filename).convert_alpha(), (64, 64))
            self.image = tiles_textures[filename]
        else:
            self.image = Surface((PLAT_W, PLAT_H))
            self.image.set_alpha(0)
        self.rect = Rect(x, y, PLAT_W * 2, PLAT_H * 2)
        self.hitbox = pygame.Rect(x + PLAT_W // 2, y + PLAT_H // 2,
                                  PLAT_W, PLAT_H)


class Blank(Platform):
    def __init__(self, x, y):
        super().__init__(x, y, None)


class Lava(Platform):
    def __init__(self, x, y):
        super().__init__(x, y, None)
        self.dmg = True
        bolt_anim = []
        for anim in ANIMATION_LAVA:
            bolt_anim.append((pygame.transform.scale(image.load(anim), (PLAT_W * 2, PLAT_H * 2)),
                              ANIMATION_DELAY))
        self.boltAnimLava = pyganim.PygAnimation(bolt_anim)
        self.boltAnimLava.play()
        self.image = self.boltAnimLava.getCurrentFrame()
        self.hitbox.top = y + PLAT_H * 18 // 16
        self.hitbox.height = PLAT_H * 6 // 16

    def update(self, *args):
        self.image = self.boltAnimLava.getCurrentFrame()


class Spikes(Platform):
    def __init__(self, x, y, filename):
        super().__init__(x, y, filename)
        self.dmg = True
        self.hitbox = pygame.Rect(x + PLAT_W // 2, y + PLAT_H * 20 // 16,
                                  PLAT_W, PLAT_H * 4 // 16)


class Ice(Platform):
    def __init__(self, x, y, filename):
        super().__init__(x, y, filename)
        self.hurts = True


class Teleport(Platform):
    def __init__(self, x, y):
        super().__init__(x, y, None)
        bolt_anim = []
        for anim in ANIMATION_TELEPORT:
            bolt_anim.append((pygame.transform.scale(image.load(anim), (PLAT_W * 16, PLAT_H * 16)),
                              ANIMATION_DELAY))
        self.boltAnimTeleport = pyganim.PygAnimation(bolt_anim)
        self.boltAnimTeleport.play()
        self.image = self.boltAnimTeleport.getCurrentFrame()
        self.rect = Rect(x - PLAT_W * 7, y - PLAT_H * 21 // 2, PLAT_W * 16, PLAT_H * 16)
        self.hitbox.top -= PLAT_H * 6
        self.hitbox.height = PLAT_H * 6

    def update(self, *args):
        self.image = self.boltAnimTeleport.getCurrentFrame()
