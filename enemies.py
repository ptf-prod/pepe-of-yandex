from pygame import *
import pygame
import time as timetime

from entity import Entity
from platforms import *
from bullet import *

ANIMATION_UKA_RUN = ['data/enemyframes/monkeyrunning/monkey running0000.png',
                     'data/enemyframes/monkeyrunning/monkey running0001.png',
                     'data/enemyframes/monkeyrunning/monkey running0002.png',
                     'data/enemyframes/monkeyrunning/monkey running0003.png',
                     'data/enemyframes/monkeyrunning/monkey running0004.png',
                     'data/enemyframes/monkeyrunning/monkey running0005.png']

ANIMATION_CRACKATOO_RUN = ['data/enemyframes/chickenrunning/chicken running0000.png',
                           'data/enemyframes/chickenrunning/chicken running0001.png',
                           'data/enemyframes/chickenrunning/chicken running0002.png',
                           'data/enemyframes/chickenrunning/chicken running0003.png']

ANIMATION_FLYLING_FLY = ['data/enemyframes/headflying/head flying0000.png',
                         'data/enemyframes/headflying/head flying0001.png',
                         'data/enemyframes/headflying/head flying0002.png',
                         'data/enemyframes/headflying/head flying0003.png']
ANIMATION_FLYLING_FIRE = ['data/enemyframes/headfire/head fireball0000.png',
                          'data/enemyframes/headfire/head fireball0001.png',
                          'data/enemyframes/headfire/head fireball0002.png',
                          'data/enemyframes/headfire/head fireball0003.png']

WIDTH = 64
HEIGHT = 64
COLOR = "RED"
JUMP_POWER = 20
GRAVITY = 0.7  # Сила, которая будет тянуть нас вниз


class Enemy(Entity):
    def __init__(self, x, y, cur_anim=None, hb_shape=None):
        self.cur_anim = None
        self.dmg = 15
        self.hit_delay = 1
        self.last_hit = 0
        if cur_anim is None:
            super().__init__(x, y, None, hb_shape)
        else:
            self.cur_anim = cur_anim
            super().__init__(x, y, cur_anim.getCurrentFrame(), hb_shape)
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        self.target_detected = False
        self.blank = None

    def update(self, t, platforms, blanks, entities, player):
        super().update(t, platforms, blanks, entities, player)
        for p in player:
            if self.hitbox.colliderect(p.hitbox):
                if self.make_dmg(p)[0]:
                    break
        # if self.collide(self.xvel, 0, blanks):
        #     self.xvel *= -1
        #     self.right = not self.right

    def check_collision(self, xvel, yvel, platforms, blanks, entities, player):
        if yvel:
            self.collide(xvel, yvel, platforms, True)
        else:
            a = self.collide(xvel, yvel, blanks, True)
            if a != self.blank:
                self.blank = a
                # Поменяйте что-нибудь здесь, если враги будут застревать в бланках
            if not a:
                a = self.collide(xvel, yvel, platforms, True)
            if a:
                self.xvel *= -1
                self.right = not self.right

    def make_dmg(self, who):
        if timetime.time() - self.last_hit < self.hit_delay:
            return False, False
        a = who.take_dmg(self, self.dmg)
        if a[0]:
            self.last_hit = timetime.time()
        return a


class OldEnemy(sprite.Sprite):
    def __init__(self, x, y, cur_anim=None, hb_shape=None):
        sprite.Sprite.__init__(self)
        self.xvel = 6  # скорость перемещения. 0 - стоять на месте
        self.yvel = 6
        self.start_x = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.start_y = y
        self.hb_shape = [0, 0, 64, 64]
        self.cur_anim = None
        self.dmg = 15
        if cur_anim is not None:
            self.hb_shape = hb_shape
            self.cur_anim = cur_anim
            self.image = cur_anim.getCurrentFrame()
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
            self.hitbox = pygame.Rect(*hb_shape)
            self.hitbox.x += x
            self.hitbox.y += y
        else:
            self.image = Surface((128, 128))
            self.image.set_colorkey(Color("Red"))
            self.image.fill(Color("Red"))
            self.rect = Rect(x, y - 47, 100, 128)
            self.hitbox = self.rect
        self.right = True
        self.on_ground = False
        self.target_detected = False

    def update(self, t, platforms, blanks, entities, players):
        self.target_check(players.sprites()[0].hitbox.topleft)
        # if type(self) == Crackatoo:  # Это надо переместить в клас курицы
        #     if self.xvel < 0:
        #         self.image.fill(Color("Red"))
        #         self.boltAnimCrackLeft.blit(self.image, (0, 0))
        #     else:
        #         self.image.fill(Color("Red"))
        #         self.boltAnimCrackLeft.blit(self.image, (0, 0))
        #     if self.target_detected is False:
        #         self.target_check(target_coords)
        #     else:
        #         self.chasing(target_coords)
        super().update(t, platforms, blanks, entities, players)

    def collide(self, blanks, platforms):
        for b in blanks:
            if self.hitbox.colliderect(b.hitbox):  # если есть пересечение врага с бланком
                if not self.target_detected:
                    self.xvel = -self.xvel
                    self.right = not self.right
                    break
        for p in platforms:
            if self.hitbox.colliderect(p.hitbox):  # если есть пересечение платформы с врагом
                if p.hitbox.y == self.hitbox.y:
                    self.xvel = -self.xvel
                if self.yvel > 0:  # если падает вниз
                    self.on_ground = True  # и становится на что-то твердое
                    self.yvel = 0  # и энергия падения пропадает
                self.hitbox.bottom = p.hitbox.top
                self.rect.top = self.hitbox.top - self.hb_shape[1]
                if self.yvel < 0:
                    self.yvel = 0  # и энергия прыжка пропадает
                    self.hitbox.top = p.hitbox.bottom
                    self.rect.top = self.hitbox.top - self.hb_shape[1]


class Uka(Enemy):
    MOVE_SPEED = 120

    def __init__(self, x, y):
        self.boltAnimRun = (load_animation(0, 6, ANIMATION_DELAY, 'data', 'enemyframes',
                                           'monkeyrunning', 'monkey running{:04d}.png'),
                            load_animation(0, 6, ANIMATION_DELAY, 'data', 'enemyframes',
                                           'monkeyrunning', 'monkey running{:04d}.png', flip=True))
        self.boltAnimRun[0].play()
        self.boltAnimRun[1].play()
        super().__init__(x, y - 32, self.boltAnimRun[0], [36, 46, 56, 46])
        self.dmg = 10
        self.hp = 30
        self.xvel = Uka.MOVE_SPEED

    def update(self, t, platforms, blanks, entities, player):
        super().update(t, platforms, blanks, entities, player)
        self.image = self.boltAnimRun[self.right].getCurrentFrame()


class Flyling(OldEnemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.flytime = 0
        self.rect = Rect(x, y - 47, 64, 64)
        self.blast_done = False
        self.blast_time = 0
        self.blast_row = 0
        boltAnim = []
        for anim in ANIMATION_FLYLING_FLY:
            boltAnim.append((pygame.transform.flip(
                pygame.transform.scale(image.load(anim), (128, 128)), True, False),
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
            boltAnim.append((pygame.transform.flip(
                pygame.transform.scale(image.load(anim), (128, 128)), True, False),
                             ANIMATION_DELAY))
        self.boltAnimFlylingFireRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimFlylingFireRight.play()

        boltAnim = []
        for anim in ANIMATION_FLYLING_FIRE:
            boltAnim.append((pygame.transform.scale(image.load(anim), (128, 128)), ANIMATION_DELAY))
        self.boltAnimFlylingFireLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimFlylingFireLeft.play()

    def update(self, blanks, platforms, target_coords, enemies_group, all_sprites):
        self.rect.x += self.xvel  # переносим положение на xvel
        self.collide(blanks, platforms)
        self.check_time()
        self.flytime += 1
        if self.blast_done is False:
            if self.rect.x - 512 <= target_coords[0] <= self.rect.x + 512 and \
                    self.rect.y - 512 <= target_coords[1] <= self.rect.x + 512:
                if self.rect.x < target_coords[0]:
                    self.image.fill(Color("Red"))
                    self.boltAnimFlylingFireLeft.blit(self.image, (0, 0))  # По-умолчанию, стоим
                else:
                    self.image.fill(Color("Red"))
                    self.boltAnimFlylingFireRight.blit(self.image, (0, 0))  # По-умолчанию, стоим
                blast = Blast(self.rect.x, self.rect.y + 14, 128, 128)
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
    MOVE_SPEED = 80

    def __init__(self, x, y):
        self.boltAnimRun = (load_animation(0, 4, ANIMATION_DELAY, 'data', 'enemyframes',
                                           'chickenrunning', 'chicken running{:04d}.png'),
                            load_animation(0, 4, ANIMATION_DELAY, 'data', 'enemyframes',
                                           'chickenrunning', 'chicken running{:04d}.png',
                                           flip=True))
        self.boltAnimRun[0].play()
        self.boltAnimRun[1].play()

        super().__init__(x, y, self.boltAnimRun[0], [48, 36, 32, 56])
        self.dmg = 15
        self.hp = 20
        self.hit_delay = 1.5
        self.target_detected = False

    def update(self, t, platforms, blanks, entities, player):
        if len(player) > 0:
            p = player.sprites()[0]
            self.target_check(p.hitbox.center)
        else:
            self.target_detected = False
        if self.target_detected:
            if p.hitbox.x > self.hitbox.x:
                self.xvel = Crackatoo.MOVE_SPEED * 2
                self.right = True
            else:
                self.xvel = -Crackatoo.MOVE_SPEED * 2
                self.right = False
        else:
            if self.xvel >= 0:
                self.xvel = Crackatoo.MOVE_SPEED
            else:
                self.xvel = -Crackatoo.MOVE_SPEED
        super().update(t, platforms, blanks, entities, player)
        self.image = self.boltAnimRun[self.right].getCurrentFrame()

    def target_check(self, coords):
        d = abs(self.hitbox.centerx - coords[0]) + abs(self.hitbox.centery - coords[1])
        if d < 300:
            self.target_detected = True
        elif d > 600:
            self.target_detected = False

    def check_collision(self, xvel, yvel, platforms, blanks, entities, player):
        if self.yvel != 0:
            return self.collide(xvel, yvel, platforms, True)
        if not self.target_detected:
            x = self.collide(xvel, yvel, blanks, True)
            if x:
                self.xvel *= -1
                self.right = not self.right
            return x
        else:
            self.collide(xvel, yvel, entities, True,
                         filt=lambda s: s.xvel == self.xvel)
            a = self.collide(xvel, yvel, player, True)
            if a:
                self.make_dmg(a)
                return a
            return a