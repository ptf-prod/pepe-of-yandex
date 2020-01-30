from pygame import *
import pygame
from Platforms import *
from Bullet import *


class Boss(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 1
        self.start_x = x
        self.start_y = y
        self.image = Surface((128, 256))
        self.image.fill(Color("Red"))
        self.rect = Rect(x, y, 128, 256)  # прямоугольный объект
        self.hp = 100
        self.attack = True
        self.attack_delay = 0


    def update(self, hero, hp):
        if self.attack:
            if self.rect.x - 32 <= hero.rect.x:
                hero.take_boss_dmg("clap", hp)
                self.attack = False
            elif self.rect.x + 32 >= hero.rect.x:
                hero.take_boss_dmg("clap", hp)
                self.attack = False
            elif self.rect.x - 512 <= hero.rect.x <= self.rect.x + 512 and hero.rect.y <= self.rect.x + 64:
                hero.take_boss_dmg("stomp", hp)
                self.attack = False
            elif self.rect.x - 512 <= hero.rect.x <= self.rect.x + 512:
                hero.take_boss_dmg("shot", hp)
        if not self.attack:
            if self.rect.x < hero.rect.x:
                self.rect.x += self.xvel
            elif self.rect.x > hero.rect.x:
                self.rect.x -= self.xvel
            self.attack_delay += 1
            if self.attack_delay == 300:
                hero.take_boss_dmg("shot", hp)
            elif self.attack_delay == 450:
                self.attack_delay = 0
                self.attack = True
            if self.hp <= 0:
                self.kill()



