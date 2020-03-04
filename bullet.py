from pygame import *
from boss import *
import random

import enemies
from entity import Entity
from main import DEBUG


class Bullet(Entity):
    def __init__(self, x, y, right):
        image = Surface((6, 4))
        image.fill(random.sample(range(0, 256), 3))
        super().__init__(x, y, image)
        if right:
            self.xvel = 2500
        else:
            self.xvel = -2500
        self.yvel = random.random() * 100 - 50
        self.kill_delay = False

    def update(self, t, platforms, blanks, entities, player):
        if not self.on_ground:
            self.yvel += self.gravity * t
        self.on_ground = False
        dy = self.yvel * t
        dx = self.xvel * t
        if self.yvel > 0:
            self.hitbox.y += min(dy, PLAT_H)
        else:
            self.hitbox.y -= min(-dy, PLAT_H)
        self.hitbox.x += dx
        for e in entities:
            if isinstance(e, enemies.Enemy) and self.hitbox.colliderect(e.hitbox):
                a = e.take_dmg(self, 40)
                if a[0]:
                    self.kill()
                    return
        for p in platforms:
            if self.hitbox.colliderect(p.hitbox):
                self.kill()
                return
        self.rect.topleft = self.hitbox.topleft
        if DEBUG:
            print(self.hitbox.x // PLAT_W, self.hitbox.y // PLAT_H)


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
            if sprite.collide_rect(self, p):
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
