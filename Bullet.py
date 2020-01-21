from pygame import *
import pygame


class Bullet(sprite.Sprite):
    def __init__(self, x, y, direction):
        sprite.Sprite.__init__(self)
        if direction == "right":
            self.xvel = 10
        else:
            self.xvel = -10
        self.start_x = x
        self.start_y = y
        self.image = Surface((6, 4))
        self.image.fill(Color("Green"))
        self.rect = Rect(x, y, 6, 4)  # прямоугольный объект

    def update(self, enemies, platforms):

        self.rect.x += self.xvel  # переносим положение на xvel
        self.collide(enemies, platforms)
        self.check_range()

    def collide(self, enemies, platforms):
        for e in enemies:
            if sprite.collide_rect(self, e):
                e.kill()
                self.kill()
        for p in platforms:
            if sprite.collide_rect(self, p):
                self.kill()

    def check_range(self):
        if self.rect.x >= self.start_x + 512:
            print("kill")
            self.kill()