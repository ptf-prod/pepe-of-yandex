from pygame import *
import pygame
from platforms import *
from bullet import *

ANIMATION_UKA_RUN = [('data\enemyframes\monkeyrunning\manky runnin0000.png'),
                     ('data\enemyframes\monkeyrunning\manky runnin0001.png'),
                     ('data\enemyframes\monkeyrunning\manky runnin0002.png'),
                     ('data\enemyframes\monkeyrunning\manky runnin0003.png'),
                     ('data\enemyframes\monkeyrunning\manky runnin0004.png'),
                     ('data\enemyframes\monkeyrunning\manky runnin0005.png')]

ANIMATION_CRACKATOO_RUN = [('data\enemyframes\chickenrunning\chicken runnin0000.png'),
                     ('data\enemyframes\chickenrunning\chicken runnin0001.png'),
                     ('data\enemyframes\chickenrunning\chicken runnin0002.png'),
                     ('data\enemyframes\chickenrunning\chicken runnin0003.png')]

ANIMATION_FLYLING_FLY = [('data\enemyframes\headflying\head flying0000.png'),
                         ('data\enemyframes\headflying\head flying0001.png'),
                         ('data\enemyframes\headflying\head flying0002.png'),
                         ('data\enemyframes\headflying\head flying0003.png')]
ANIMATION_FLYLING_FIRE = [('data\enemyframes\headfire\head fireball0000.png'),
                         ('data\enemyframes\headfire\head fireball0001.png'),
                         ('data\enemyframes\headfire\head fireball0002.png'),
                         ('data\enemyframes\headfire\head fireball0003.png')]

MOVE_SPEED = 4
WIDTH = 64
HEIGHT = 64
COLOR = "RED"
JUMP_POWER = 20
GRAVITY = 0.7  # Сила, которая будет тянуть нас вниз


class Enemy(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 6  # скорость перемещения. 0 - стоять на месте
        self.yvel = 6
        self.start_x = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.start_y = y
        self.image = Surface((128, 128))
        self.image.set_colorkey(Color("Red"))
        self.image.fill(Color("Red"))
        self.rect = Rect(x, y - 47, 100, 128)
        self.onGround = False
        self.target_detected = False

    def update(self, blanks, platforms, target_coords, enemies, enemies_group, all_sprites):
        if self.target_detected is False:
            self.rect.x += self.xvel  # переносим положение на xvel
        if type(self) == Crackatoo:
            if self.xvel < 0:
                self.image.fill(Color("Red"))
                self.boltAnimCrackLeft.blit(self.image, (0, 0))
            else:
                self.image.fill(Color("Red"))
                self.boltAnimCrackLeft.blit(self.image, (0, 0))
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
            boltAnim.append((pygame.transform.flip(pygame.transform.scale(image.load(anim), (128, 128)), True, False),
                             ANIMATION_DELAY))
        self.boltAnimUkaRunRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimUkaRunRight.play()
        self.boltAnimUkaRunRight.blit(self.image, (0, 0))

        boltAnim = []
        for anim in ANIMATION_UKA_RUN:
            boltAnim.append((pygame.transform.scale(image.load(anim), (128, 128)), ANIMATION_DELAY))
        self.boltAnimUkaRunLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimUkaRunLeft.play()

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

        if self.xvel < 0:
            self.image.fill(Color("Red"))
            self.boltAnimUkaRunLeft.blit(self.image, (0, 0))
        else:
            self.image.fill(Color("Red"))
            self.boltAnimUkaRunRight.blit(self.image, (0, 0))


class Flyling(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.flytime = 0
        self.rect = Rect(x, y - 47, 64, 64)
        self.blast_done = False
        self.blast_time = 0
        self.blast_row = 0
        boltAnim = []
        for anim in ANIMATION_FLYLING_FLY:
            boltAnim.append((pygame.transform.flip(pygame.transform.scale(image.load(anim), (128, 128)), True, False),
                             ANIMATION_DELAY))
        self.boltAnimFlylingFlyRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimFlylingFlyRight.play()
        self.boltAnimFlylingFlyRight.blit(self.image, (0, 0))

        boltAnim = []
        for anim in ANIMATION_FLYLING_FLY:
            boltAnim.append((pygame.transform.scale(image.load(anim), (128, 128)), ANIMATION_DELAY))
        self.boltAnimFlylingFlyLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimFlylingFlyLeft.play()

        boltAnim = []
        for anim in ANIMATION_FLYLING_FIRE:
            boltAnim.append((pygame.transform.flip(pygame.transform.scale(image.load(anim), (128, 128)), True, False),
                             ANIMATION_DELAY))
        self.boltAnimFlylingFireRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimFlylingFireRight.play()

        boltAnim = []
        for anim in ANIMATION_FLYLING_FIRE:
            boltAnim.append((pygame.transform.scale(image.load(anim), (128, 128)), ANIMATION_DELAY))
        self.boltAnimFlylingFireLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimFlylingFireLeft.play()

    def update(self, blanks, platforms, coords, enemies, enemies_group, all_sprites):
        self.rect.x += self.xvel  # переносим положение на xvel
        self.collide(blanks, platforms)
        self.check_time()
        self.flytime += 1
        if self.blast_done is False:
            if self.rect.x - 512 <= coords[0] <= self.rect.x + 512 and self.rect.y - 512 <= coords[1] <= self.rect.x + 512:
                if self.rect.x < coords[0]:
                    self.image.fill(Color("Red"))
                    self.boltAnimFlylingFireLeft.blit(self.image, (0, 0))  # По-умолчанию, стоим
                else:
                    self.image.fill(Color("Red"))
                    self.boltAnimFlylingFireRight.blit(self.image, (0, 0))  # По-умолчанию, стоим
                blast = Blast(self.rect.x, self.rect.y + 14, 128, 128)
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
        if self.xvel < 0:
            self.image.fill(Color("Red"))
            self.boltAnimFlylingFlyLeft.blit(self.image, (0, 0))  # По-умолчанию, стоим
        else:
            self.image.fill(Color("Red"))
            self.boltAnimFlylingFlyRight.blit(self.image, (0, 0))  # По-умолчанию, стоим

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

        boltAnim = []
        for anim in ANIMATION_CRACKATOO_RUN:
            boltAnim.append((pygame.transform.flip(pygame.transform.scale(image.load(anim), (128, 128)), True, False),
                             ANIMATION_DELAY))
        self.boltAnimCrackRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimCrackRight.play()
        self.boltAnimCrackRight.blit(self.image, (0, 0))

        boltAnim = []
        for anim in ANIMATION_CRACKATOO_RUN:
            boltAnim.append((pygame.transform.scale(image.load(anim), (128, 128)), ANIMATION_DELAY))
        self.boltAnimCrackLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimCrackLeft.play()

    def target_check(self, coords):
        if self.rect.x - 256 <= coords[0] <= self.rect.x + 256 and self.rect.y - 256 <= coords[1] <= self.rect.x + 256:
            self.xvel = 15
            self.target_detected = True

    def chasing(self, coords):
        if self.rect.x <= coords[0]:
            self.rect.x += self.xvel
            self.image.fill(Color("Red"))
            self.boltAnimCrackRight.blit(self.image, (0, 0))
        elif self.rect.x > coords[0]:
            self.rect.x -= self.xvel
            self.image.fill(Color("Red"))
            self.boltAnimCrackLeft.blit(self.image, (0, 0))
