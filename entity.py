import pygame
from pygame import sprite
import pyganim
import time
from platforms import Ice

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
        self.hp = 1

    def update(self, t, platforms, blanks, entities, player):
        if not self.on_ground:
            self.yvel += self.gravity * t
        self.on_ground = False
        dy = self.yvel * t
        dx = self.xvel * t
        n = int(max(abs(dy / self.hitbox.height), abs(dx / self.hitbox.width)) + 1)
        dy /= n
        dx /= n
        for i in range(n):
            self.hitbox.y += dy
            a = self.collide_plat(0, dy, platforms)
            self.hitbox.x += dx
            a = self.collide_plat(dx, 0, platforms) or a
            if a:
                break
        self.rect.x = self.hitbox.x - self.hb_shape[0]
        self.rect.y = self.hitbox.y - self.hb_shape[1]

    def collide_plat(self, xvel, yvel, platforms):
        colliding = False
        ok = False
        while not ok:
            ok = True
            for p in platforms:
                if self.hitbox.colliderect(p.hitbox):  # если есть пересечение платформы с игроком
                    self.block = "platform"
                    if xvel > 0:  # если движется вправо
                        self.hitbox.right = p.hitbox.left  # то не движется вправо

                    elif xvel < 0:  # если движется влево
                        self.hitbox.left = p.hitbox.right  # то не движется вправо

                    elif yvel > 0:  # если падает вниз
                        self.hitbox.bottom = p.hitbox.top  # то не падает вниз
                        self.yvel = 0
                        self.on_ground = True  # и становится на что-то твердое

                    elif yvel < 0:  # если движется вверх
                        self.hitbox.top = p.hitbox.bottom  # то не движется вверх
                        self.yvel = 0  # и энергия прыжка пропадает
                    else:
                        break
                    if type(p) == Ice:
                        self.previous_block = self.block
                        self.block = "ice"
                    if p.hurts and sprite.collide_rect(self, p):
                        self.take_dmg(p, p.hurts)
                        self.block = f"{p}"
                    colliding = True
                    ok = False
                    break
        return colliding

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
