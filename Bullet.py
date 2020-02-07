from pygame import *
from Boss import *
import random

COLORS = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', "A", 'B', "C", 'D', 'E', 'F')


class Bullet(sprite.Sprite):
    def __init__(self, x, y, direction):
        sprite.Sprite.__init__(self)
        if direction == "Right":
            self.xvel = 10
        else:
            self.xvel = -10
        self.start_x = x
        self.start_y = y
        self.image = Surface((6, 4))
        self.color = f"#{random.choice(COLORS)}{random.choice(COLORS)}{random.choice(COLORS)}{random.choice(COLORS)}{random.choice(COLORS)}{random.choice(COLORS)}"
        self.image.fill(Color(self.color))
        self.rect = Rect(x, y, 6, 4)  # прямоугольный объект
        self.kill_delay = False

    def update(self, enemies, platforms, bullets):

        self.rect.x += self.xvel  # переносим положение на xvel
        self.collide(enemies, platforms)
        self.check_range()
        if self.kill_delay:
            self.kill_delay = False
            self.kill()
            del bullets[bullets.index(self)]

    def collide(self, enemies, platforms):
        for e in enemies:
            if sprite.collide_rect(self, e):
                if type(e) != Boss:
                    e.kill()
                    self.kill_delay = True
                    del enemies[enemies.index(e)]
                else:
                    e.hp -= 1
                    print(e.hp)
                    self.kill_delay = True

        for p in platforms:
            if sprite.collide_rect(self, p):
                self.kill()

    def check_range(self):
        if self.rect.x >= self.start_x + 512 or self.rect.x <= self.start_x - 512:
            print("kill")
            self.kill()


class Blast(sprite.Sprite):
    def __init__(self, x, y, sizex, sizey):
        sprite.Sprite.__init__(self)
        self.start_x = x
        self.start_y = y
        self.image = pygame.transform.scale(image.load("data\enemyframes\\fireball.png"), (sizex, sizey))
        self.rect = Rect(x+60, y+60, 8, 8)
        self.dmg = 10

    def update(self, blanks, platforms, hero_coords, enemies, enemies_group, all_sprites):
        if self.rect.x > hero_coords[0] + 32:
            self.rect.x -= 3
        elif self.rect.x < hero_coords[0] + 32:
            self.rect.x += 3
        if self.rect.y > hero_coords[1] - 64:
            self.rect.y -= 3
        elif self.rect.y < hero_coords[1] - 64:
            self.rect.y += 3
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

    def update(self, enemies, platforms, bullets):

        self.rect.x += self.xvel  # переносим положение на xvel
        self.collide(enemies)
        self.check_range(bullets)


    def collide(self, enemies):
        for e in enemies:
            if sprite.collide_rect(self, e):
                if type(e) != Boss:
                    e.kill()
                    self.kill_delay = True
                    del enemies[enemies.index(e)]
                else:
                    e.hp -= 5
                    print(e.hp)
                    self.kill_delay = True

    def check_range(self, bullets):
        if self.rect.x >= self.start_x + 100 or self.rect.x <= self.start_x - 100:
            print("kill")
            self.kill()
            del bullets[bullets.index(self)]