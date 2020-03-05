from pygame import *
from boss import *
import random

from main import DEBUG


class Bullet(sprite.Sprite):
    def __init__(self, x, y, direction):
        sprite.Sprite.__init__(self)
        if direction == "Right":
            self.xvel = 1000
        else:
            self.xvel = -1000
        self.y = y
        self.yvel = random.random() * 100 - 50
        self.start_x = x
        self.start_y = y
        self.image = Surface((6, 4))
        self.color = random.sample(range(0, 256), 3)
        self.image.fill(self.color)
        self.rect = Rect(x, y, 6, 4)  # прямоугольный объект
        self.kill_delay = False

    def update(self, t, enemies, platforms, bullets):

        self.rect.x += self.xvel * t  # переносим положение на xvel
        self.rect.y = self.y = self.y + self.yvel * t
        self.collide(enemies, platforms)
        self.check_range()
        if self.kill_delay:
            self.kill_delay = False
            self.kill()
        if DEBUG:
            print(self.rect.y)

    def collide(self, enemies, platforms):
        for e in enemies:
            if sprite.collide_rect(self, e):
                if type(e) != Boss:
                    e.kill()
                    self.kill_delay = True
                else:
                    e.hp -= 1
                    if DEBUG:
                        print(e.hp)
                    self.kill_delay = True

        for p in platforms:
            if sprite.collide_rect(self, p):
                self.kill()

    def check_range(self):
        if abs(self.rect.x - self.start_x) > 3000:
            if DEBUG:
                print("kill")
            self.kill()


class Blast(sprite.Sprite):
    def __init__(self, x, y, sizex, sizey):
        sprite.Sprite.__init__(self)
        self.start_x = x
        self.start_y = y
        self.image = pygame.transform.scale(image.load("data/enemyframes/fireball.png"),
                                            (sizex, sizey))
        self.rect = Rect(x, y, 8, 8)
        self.dmg = 10
        self.hitbox = Rect(0, 0, 8, 8)

    def update(self, blanks, platforms, hero_coords, enemies_group, all_sprites):
        if self.hitbox.x > hero_coords[0] + 16:
            self.rect.x -= 3
        elif self.hitbox.x < hero_coords[0] + 16:
            self.rect.x += 3
        if self.hitbox.y > hero_coords[1] + 32:
            self.rect.y -= 3
        elif self.hitbox.y < hero_coords[1] + 32:
            self.rect.y += 3
        self.hitbox.x = self.rect.x + 60
        self.hitbox.y = self.rect.y + 60
        self.collide(platforms)

    def collide(self, platforms):
        for p in platforms:
            if self.hitbox.colliderect(p.hitbox):
                self.kill()


class Hit(sprite.Sprite):
    def __init__(self, x, y, direction):
        sprite.Sprite.__init__(self)
        if direction == "Right":
            self.xvel = 100
        else:
            self.xvel = -100
        self.start_x = x
        self.start_y = y
        self.image = Surface((64, 64))
        self.image.fill(Color("White"))
        self.image.set_alpha(255)
        self.rect = Rect(x, y, 64, 64)  # прямоугольный объект

    def update(self, t, enemies, platforms, bullets):

        self.rect.x += self.xvel  # переносим положение на xvel
        self.collide(enemies)
        self.check_range(bullets)

    def collide(self, enemies):
        for e in enemies:
            if sprite.collide_rect(self, e):
                if type(e) != Boss:
                    e.kill()
                    self.kill_delay = True
                else:
                    e.hp -= 5
                    if DEBUG:
                        print(e.hp)
                    self.kill_delay = True

    def check_range(self, bullets):
        if self.rect.x >= self.start_x + 100 or self.rect.x <= self.start_x - 100:
            if DEBUG:
                print("kill")
            self.kill()
