from pygame import *
import pygame
from Platforms import *


MOVE_SPEED = 7
WIDTH = 22
HEIGHT = 32
COLOR = "RED"
JUMP_POWER = 10
GRAVITY = 0.35  # Сила, которая будет тянуть нас вниз


class Enemy(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 3  # скорость перемещения. 0 - стоять на месте
        self.yvel = 3
        self.start_x = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.start_y = y
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)  # прямоугольный объект
        self.onGround = False

    def update(self, blanks, platforms, target_coords):

        self.rect.x += self.xvel  # переносим положение на xvel
        self.collide(blanks, platforms)
        if type(self) == Crackatoo:
            self.target_check(target_coords)

        if not self.onGround:
            self.yvel += GRAVITY

    def collide(self, blanks, platforms):
        for b in blanks:
            if sprite.collide_rect(self, b):  # если есть пересечение врага с бланком
                if type(self) == Crackatoo and self.target_detected is False or type(self) != Crackatoo:
                    self.xvel = -self.xvel
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком
                if self.xvel != 0:
                    self.xvel = -self.xvel

                if self.yvel > 0:  # если падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.yvel = 0  # и энергия падения пропадает

                if self.yvel < 0:  # если движется вверх
                    self.yvel = 0  # и энергия прыжка пропадает



class Uka(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)


class Flyling(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.flytime = 0

    def update(self, blanks, platforms, target_coords):
        self.rect.x += self.xvel  # переносим положение на xvel
        self.collide(platforms)
        self.check_time()
        self.flytime += 1

    def check_time(self):
        if self.flytime >= 60:
            self.xvel = -self.xvel
            self.flytime = 0

    def collide(self, platforms):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            self.xvel = -self.xvel
            self.flytime = 0


class Crackatoo(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.hero_coords = ()
        self.target_detected = False

    def target_check(self, coords):
        if self.rect.x - 100 < coords[0] or\
            self.rect.x + 100 > coords[0] or \
            self.rect.y - 100 < coords[1] or \
                self.rect.y + 100 > coords[1]:
            self.xvel = 14
            self.target_detected = True
            if self.rect.y == coords[1] and self.rect < coords[0]:
                self.rect.x += self.xvel
            elif self.rect.y == coords[1] and self.rect > coords[0]:
                self.rect.x -= self.xvel


