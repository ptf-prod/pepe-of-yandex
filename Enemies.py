from pygame import *
import random
import pygame
import PepeHero
import math

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
        self.onGround = False  # На земле ли я?


    def update(self, blanks, platforms):

        self.rect.x += self.xvel  # переносим положение на xvel
        self.collide(blanks)

    def collide(self, blanks):
        for p in blanks:
            if sprite.collide_rect(self, p):  # если есть пересечение врага с бланком
                self.xvel = -self.xvel


class Uka(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)


class Flyling(Enemy):
    def __init__(self, x , y):
        super().__init__(x, y)
        self.flytime = 0
        self.hero_coords = (0, 0)

    def update(self, blanks, platforms):
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


