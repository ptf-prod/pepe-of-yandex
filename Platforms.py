#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import os

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"

 
class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class Blank(Platform):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image.fill((50, 150, 255))
        self.image.set_alpha(0)


class Lava(Platform):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image.fill((255, 255, 255))


class Spikes(Platform):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image.fill((0, 0, 0))


class Ice(Platform):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image.fill((0, 255, 0))