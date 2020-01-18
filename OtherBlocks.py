#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import os




PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "Black"


class Blank(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill((50, 150, 255))
        self.image.set_alpha(0)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)