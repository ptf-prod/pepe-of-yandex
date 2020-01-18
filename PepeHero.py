from pygame import *
import pygame
from NewHope import *
from Enemies import *

MOVE_SPEED = 7
WIDTH = 22
HEIGHT = 32
COLOR = "#888888"
JUMP_POWER = 10
GRAVITY = 0.35  # Сила, которая будет тянуть нас вниз





class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        self.start_x = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.start_y = y
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)  # прямоугольный объект
        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False  # На земле ли я?
        self.previosly_move = "right"


    def update(self, left, right, up, platforms, down, enemies, hit, screen):
        if up:
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER
        if left:
            self.xvel = -MOVE_SPEED  # Лево = x- n
            self.previosly_move = "left"

        if right:
            self.xvel = MOVE_SPEED  # Право = x + n
            self.previosly_move = "right"

        if down:
            if not self.onGround:
                self.yvel += JUMP_POWER // 2
                self.xvel = 0

        if hit:
            for e in enemies:
                if self.previosly_move == "right":
                    if self.rect.x <= e.rect.x <= self.rect.x + 86 and \
                            self.rect.y <= e.rect.y <= self.rect.y + 32:
                        e.kill()
                else:
                    if self.rect.x >= e.rect.x >= self.rect.x - 64 and \
                            self.rect.y <= e.rect.y <= self.rect.y + 32:
                        e.kill()


        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0
        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms, enemies)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms, enemies)

    def collide(self, xvel, yvel, platforms, enemies):
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                if xvel > 0:                      # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if xvel < 0:                      # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

                if yvel > 0:                      # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True          # и становится на что-то твердое
                    self.yvel = 0                 # и энергия падения пропадает

                if yvel < 0:                      # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.yvel = 0                 # и энергия прыжка пропадает

        for p in enemies:
            if sprite.collide_rect(self, p):
                self.die()

    def die(self):
        self.kill()


