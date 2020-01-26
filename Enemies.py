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
        self.target_detected = False

    def update(self, blanks, platforms, target_coords):

        if self.target_detected is False:
            self.rect.x += self.xvel  # переносим положение на xvel
        if type(self) == Crackatoo:
            if self.target_detected is False:
                self.target_check(target_coords)
            else:
                self.chasing(target_coords)

        if self.onGround is False:
            self.yvel += GRAVITY
        self.onGround = False
        self.rect.y += self.yvel
        self.collide(blanks, platforms)

    def collide(self, blanks, platforms):
        for b in blanks:
            if sprite.collide_rect(self, b):  # если есть пересечение врага с бланком
                if type(self) == Crackatoo and self.target_detected is False or type(self) != Crackatoo:
                    self.xvel = -self.xvel
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                if self.yvel > 0:  # если падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.yvel = 0  # и энергия падения пропадает

                if self.yvel < 0:
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
        self.collide(blanks, platforms)
        self.check_time()
        self.flytime += 1

    def check_time(self):
        if self.flytime >= 60:
            self.xvel = -self.xvel
            self.flytime = 0

    def collide(self, blanks, platforms):
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
        if self.rect.x - 64 < coords[0] or\
            self.rect.x + 64 > coords[0] or \
            self.rect.y - 64 < coords[1] or \
                self.rect.y + 64 > coords[1]:
            self.xvel = 8
            self.target_detected = True

    def chasing(self, coords):
        if self.rect.x <= coords[0]:
            self.rect.x += self.xvel
        elif self.rect.x > coords[0]:
            self.rect.x -= self.xvel


