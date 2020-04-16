#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

import pygame
import pyganim
from pygame import sprite, Rect, Surface, image

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
        self.visible = True
        if filename is not None:
            if filename not in tiles_textures:
                tiles_textures[filename] = \
                    pygame.transform.scale(image.load(filename).convert_alpha(), (64, 64))
            self.image = tiles_textures[filename]
        else:
            self.image = Surface((PLAT_W, PLAT_H))
            self.image.set_alpha(0)
            self.visible = False
        self.rect = Rect(x, y, PLAT_W * 2, PLAT_H * 2)
        self.hitbox = pygame.Rect(x + PLAT_W // 2, y + PLAT_H // 2,
                                  PLAT_W, PLAT_H)


class Trigger(Platform):
    def __init__(self, x, y, edge=0):
        super().__init__(x, y, None)
        if edge != 0:
            self.hitbox.width = int(PLAT_W * abs(edge))
            if edge > 0:
                self.hitbox.right = x + PLAT_W * 3 // 2


class InteractivePlatform(Platform):
    def __init__(self, x, y, filename, parent_group):
        super().__init__(x, y, filename)
        self.parent_group = parent_group

    def check_collision_plat(self, who):
        pass


class Lava(InteractivePlatform):
    dmg = 3
    hit_delay = 0.05

    def __init__(self, x, y, group, filename=None):
        if filename is None:
            super().__init__(x, y, None, group)
            bolt_anim = []
            for anim in ANIMATION_LAVA:
                bolt_anim.append((pygame.transform.scale(image.load(anim), (PLAT_W * 2, PLAT_H * 2)),
                                  ANIMATION_DELAY))
            self.boltAnimLava = pyganim.PygAnimation(bolt_anim)
            self.boltAnimLava.play()
            self.image = self.boltAnimLava.getCurrentFrame()
        else:
            super().__init__(x, y, filename, group)
        self.hitbox.top = y + PLAT_H * 18 // 16
        self.hitbox.height = PLAT_H * 6 // 16
        self.damage_zone = pygame.Rect(x + PLAT_W * 8 // 16, y + PLAT_H * 10 // 16,
                                       PLAT_W, PLAT_H * 10 // 16)

    def check_collision_plat(self, who):
        if self.damage_zone.colliderect(who.hitbox):
            self.parent_group.declare_collision(who)

    def update(self, *args):
        try:
            self.image = self.boltAnimLava.getCurrentFrame()
        except AttributeError:
            pass


class LavaGroup(sprite.Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)
        self.victims = {}
        self.old_victims = {}

    def declare_collision(self, ent):
        if ent in self.victims:
            pass
        elif ent in self.old_victims:
            self.victims[ent] = self.old_victims[ent]
        else:
            self.victims[ent] = [time.time(), None, time.time()]
        # (вошёл в лаву, вышел, последний удар)

    def update(self, t, on_screen, blanks_group, enemies_group, player_group):
        for i in self.victims.items():
            dt = time.time() - i[1][2]
            if dt > Lava.hit_delay:
                i[0].take_dmg(self, Lava.dmg)
                i[1][2] = time.time()
        for i in self.old_victims.items():
            if i[0] not in self.victims:
                if i[1][1] is None:
                    i[1][1] = time.time()
                if time.time() - i[1][1] > (i[1][1] - i[1][0]) / 2:
                    continue
                if time.time() - i[1][2] > Lava.hit_delay:
                    i[1][2] = time.time()
                    i[0].take_dmg(self, Lava.dmg)
                self.victims[i[0]] = i[1]
        self.old_victims = self.victims
        self.victims = {}


class Spikes(InteractivePlatform):
    dmg = 7
    hit_delay_stay = 1.2
    hit_delay_move = 0.2

    def __init__(self, x, y, filename, spikes_group):
        super().__init__(x, y, filename, spikes_group)
        self.hitbox = pygame.Rect(x + PLAT_W // 2, y + PLAT_H * 20 // 16,
                                  PLAT_W, PLAT_H * 4 // 16)
        self.fight_zone = pygame.Rect(x + PLAT_W * 10 // 32, y + PLAT_H * 15 // 32,
                                      PLAT_W, PLAT_H * 4 // 16)
        self.damage_zone = pygame.Rect(x + PLAT_W * 10 // 16, y + PLAT_H * 13 // 16,
                                       PLAT_W * 12 // 16, PLAT_H * 7 // 16)

    def check_collision_plat(self, who):
        if self.damage_zone.colliderect(who.hitbox):
            self.parent_group.declare_collision(who)


class SpikesGroup(sprite.Group):
    def declare_collision(self, ent):
        if ent in self.victims:
            pass
        elif ent in self.old_victims:
            self.victims[ent] = self.old_victims[ent]
        else:
            self.victims[ent] = time.time() - Spikes.hit_delay_stay

    def __init__(self, *sprites):
        super().__init__(*sprites)
        self.victims = {}
        self.old_victims = {}

    def update(self, t, on_screen, blanks_group, enemies_group, player_group):
        for i in self.victims.items():
            dt = time.time() - i[1]
            if dt > Spikes.hit_delay_stay or dt > Spikes.hit_delay_move and i[0].xvel != 0:
                self.victims[i[0]] = time.time()
                i[0].take_dmg(self, Spikes.dmg)
        self.old_victims = self.victims
        self.victims = {}


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
