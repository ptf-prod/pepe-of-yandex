from pygame import *
import pygame
from Platforms import *
from Bullet import *

ANIMATION_UKA_RUN = [('data\enemyframes\monkeyrunning\manky runnin0000.png'),
                    ('data\enemyframes\monkeyrunning\manky runnin0001.png'),
                    ('data\enemyframes\monkeyrunning\manky runnin0002.png'),
                    ('data\enemyframes\monkeyrunning\manky runnin0003.png'),
                    ('data\enemyframes\monkeyrunning\manky runnin0004.png'),
                    ('data\enemyframes\monkeyrunning\manky runnin0005.png')]
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
        self.image = Surface((64, 64))
        self.image.set_colorkey(Color("Red"))
        self.image.fill(Color("Red"))
        self.rect = Rect(x, y, 64, 64)
        self.rect = Rect(x, y, WIDTH, HEIGHT)  # прямоугольный объект
        self.onGround = False
        self.target_detected = False

    def update(self, blanks, platforms, target_coords, enemies, enemies_group, all_sprites):
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
                if p.rect.y == self.rect.y:
                    self.xvel = -self.xvel
                if self.yvel > 0:  # если падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.yvel = 0  # и энергия падения пропадает

                if self.yvel < 0:
                    self.yvel = 0  # и энергия прыжка пропадает



class Uka(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        boltAnim = []
        for anim in ANIMATION_UKA_RUN:
            boltAnim.append((image.load(anim), ANIMATION_DELAY))
        self.boltAnimUkaRunRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimUkaRunRight.play()


        boltAnim = []
        for anim in ANIMATION_UKA_RUN:
            boltAnim.append((pygame.transform.flip(image.load(anim), True, False), ANIMATION_DELAY))
        self.boltAnimUkaRunLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimUkaRunLeft.play()


    def update(self, blanks, platforms, target_coords, enemies, enemies_group, all_sprites):
        if self.xvel > 0:
            self.image.fill(Color("Red"))
            self.boltAnimUkaRunLeft.blit(self.image, (0, 0))  # По-умолчанию, стоим
        else:
            self.image.fill(Color("Red"))
            self.boltAnimUkaRunRight.blit(self.image, (0, 0))  # По-умолчанию, стоим



class Flyling(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.flytime = 0
        self.blast_done = False
        self.blast_time = 0
        self.blast_row = 0

    def update(self, blanks, platforms, coords, enemies, enemies_group, all_sprites):
        self.rect.x += self.xvel  # переносим положение на xvel
        self.collide(blanks, platforms)
        self.check_time()
        self.flytime += 1
        if self.blast_done is False:
            if self.rect.x - 512 <= coords[0] <= self.rect.x + 512 and self.rect.y - 512 <= coords[1] <= self.rect.x + 512 :
                blast = Blast(self.rect.x, self.rect.y + 14)
                enemies.append(blast)
                enemies_group.add(blast)
                all_sprites.add(blast)
                self.blast_done = True
        else:
            self.blast_time += 1
            if self.blast_time == 15:
                self.blast_time = 0
                self.blast_done = False
                self.blast_row += 1
            if self.blast_row == 3:
                self.blast_time = -150
                self.blast_done = False
                self.blast_row = 0

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
        if self.rect.x - 256 <= coords[0] <= self.rect.x + 256 and self.rect.y - 256 <= coords[1] <= self.rect.x + 256:
            self.xvel = 8
            self.target_detected = True

    def chasing(self, coords):
        if self.rect.x <= coords[0]:
            self.rect.x += self.xvel
        elif self.rect.x > coords[0]:
            self.rect.x -= self.xvel


