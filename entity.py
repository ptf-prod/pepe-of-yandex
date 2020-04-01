import pygame
from pygame import sprite
import pyganim
import time
import platforms as plat

from constants import *


class Entity(sprite.Sprite):
    def __init__(self, x, y, image=None, hb_shape=None):
        super().__init__()
        if image is None:
            self.image = pygame.Surface((PLAT_W, PLAT_H))
        else:
            self.image = image
        self.rect = self.image.get_rect()
        if hb_shape is None:
            hb_shape = [0, 0, self.rect.width, self.rect.height]
        self.hb_shape = hb_shape
        self.rect.topleft = (x, y)
        self.hitbox = pygame.Rect(x + hb_shape[0], y + hb_shape[1], *hb_shape[2:])
        self.xvel = 0
        self.yvel = 0
        self.on_ground = False
        self.gravity = GRAVITY
        self.right = True
        self.block = None
        self.hp = 1

    def update(self, t, platforms, blanks, entities, player):
        old_yvel = self.yvel
        if not self.on_ground:
            self.yvel += self.gravity * t
        self.on_ground = False
        dy = (old_yvel + self.yvel) / 2 * t
        dx = self.xvel * t
        n = int(max(abs(dy / self.hitbox.height), abs(dx / self.hitbox.width)) + 1)
        dy /= n
        dx /= n
        for i in range(n):
            self.hitbox.y += dy
            a = self.check_collision(0, dy, platforms, blanks, entities, player)
            self.hitbox.x += dx
            a = self.check_collision(dx, 0, platforms, blanks, entities, player) or a
            if a:
                break
        self.rect.x = self.hitbox.x - self.hb_shape[0]
        self.rect.y = self.hitbox.y - self.hb_shape[1]

    def check_collision(self, xvel, yvel, platforms, blanks, entities, player):
        return self.collide(xvel, yvel, platforms, True)

    def collide(self, xvel, yvel, group, prevent=True, filt=lambda x: True):
        for s in group:
            if self.hitbox.colliderect(s.rect):
                if isinstance(s, plat.InteractivePlatform):
                    s.check_collision_plat(self)
                if filt(s) and self.hitbox.colliderect(s.hitbox) and s is not self:
                    if isinstance(s, plat.Platform):
                        if self.yvel == 0:
                            self.block = (s, 1)
                        else:
                            self.block = (s, 0)
                    if prevent:
                        if xvel > 0:  # если движется вправо
                            self.hitbox.right = s.hitbox.left  # то не движется вправо

                        elif xvel < 0:  # если движется влево
                            self.hitbox.left = s.hitbox.right  # то не движется вправо

                        elif yvel > 0:  # если падает вниз
                            self.hitbox.bottom = s.hitbox.top  # то не падает вниз
                            self.yvel = 0
                            self.on_ground = True  # и становится на что-то твердое

                        elif yvel < 0:  # если движется вверх
                            self.hitbox.top = s.hitbox.bottom  # то не движется вверх
                            self.yvel = 0  # и энергия прыжка пропадает
                    # if type(s) == Ice:
                    #     self.previous_block = self.block
                    #     self.block = "ice"
                    if isinstance(s, plat.Platform) and s.dmg:
                        self.take_dmg(s, s.dmg)
                    return s
        return False

    def take_dmg(self, who, dmg):
        """
        :param who: кто ударил
        :param dmg: количество урона
        :return: Получил ли урон (вдруг иммунитет), умер ли
        """
        self.hp -= dmg
        if self.hp <= 0:
            self.kill()
            return True, True
        else:
            return True, False
