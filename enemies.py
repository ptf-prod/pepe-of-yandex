from pygame import *
import pygame
import time as timetime

import platforms as plat
from entity import Entity
from bullet import *
from constants import *
import pyganim

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
        self.barriers = None

    def get_barriers_x(self, platforms, blanks):
        a = platforms.sprites() + blanks.sprites()
        left = right = None
        for i in a:
            if self.hitbox.colliderect(Rect(self.hitbox.x, i.hitbox.top, 1, i.hitbox.height)):
                if i.hitbox.right <= self.hitbox.left and \
                        (left is None or i.hitbox.right > left.hitbox.right):
                    left = i
                elif i.hitbox.left >= self.hitbox.right and \
                        (right is None or i.hitbox.right < right.hitbox.right):
                    right = i
        self.barriers = sprite.Group()
        if left is not None:
            self.barriers.add(left)
        if right is not None:
            self.barriers.add(right)

    def update(self, t, platforms, blanks, entities, player):
        super().update(t, platforms, blanks, entities, player)
        for p in player:
            if self.hitbox.colliderect(p.hitbox):
                if self.make_dmg(p)[0]:
                    break

    def check_collision(self, xvel, yvel, platforms, blanks, entities, player):
        if yvel:
            self.collide(xvel, yvel, platforms, True)
        else:
            if self.barriers is not None:
                a = self.collide(xvel, yvel, self.barriers, True)
                if a:
                    self.reverse()
                return
            a = self.collide(xvel, yvel, blanks, True)
            if a != self.blank:
                self.blank = a
                # Поменяйте что-нибудь здесь, если враги будут застревать в бланках
            if not a:
                a = self.collide(xvel, yvel, platforms, True)
            if a:
                self.reverse()

    def make_dmg(self, who):
        if timetime.time() - self.last_hit < self.hit_delay:
            return False, False
        a = who.take_dmg(self, self.dmg)
        if a[0]:
            self.last_hit = timetime.time()
        return a

    def reverse(self):
        self.xvel *= -1
        self.right = not self.right


class Uka(Enemy):
    MOVE_SPEED = 120

    def __init__(self, x, y):
        self.boltAnimRun = (load_animation(0, 6, ANIMATION_DELAY, 'data', 'enemyframes',
                                           'monkeyrunning', 'monkey running{:04d}.png'),
                            load_animation(0, 6, ANIMATION_DELAY, 'data', 'enemyframes',
                                           'monkeyrunning', 'monkey running{:04d}.png', flip=True))
        self.boltAnimRun[0].play()
        self.boltAnimRun[1].play()

        super().__init__(x, y - PLAT_H * 44 // 32, self.boltAnimRun[0], [PLAT_W * 44 // 32, PLAT_H * 56 // 32,
                                                                         PLAT_W * 44 // 32, PLAT_H * 36 // 32])
        self.dmg = 10
        self.hp = 30
        self.xvel = Uka.MOVE_SPEED

    def update(self, t, platforms, blanks, entities, player):
        if self.barriers is None:
            self.get_barriers_x(platforms, blanks)
        super().update(t, platforms, blanks, entities, player)
        self.image = self.boltAnimRun[self.right].getCurrentFrame()


class Flyling(Enemy):
    MOVE_SPEED = 50

    def __init__(self, x, y):
        self.blast_delay = 3
        self.boltAnimFly = (load_animation(0, 4, ANIMATION_DELAY, 'data', 'enemyframes',
                                           'headflying', 'head flying{:04d}.png'),
                            load_animation(0, 4, ANIMATION_DELAY, 'data', 'enemyframes',
                                           'headflying', 'head flying{:04d}.png', flip=True))
        self.boltAnimFly[0].play()
        self.boltAnimFly[1].play()

        self.boltAnimFire = (load_animation(1, 4, ANIMATION_DELAY, 'data', 'enemyframes',
                                            'headfire', 'head fireball{:04d}.png'),
                             load_animation(1, 4, ANIMATION_DELAY, 'data', 'enemyframes',
                                            'headfire', 'head fireball{:04d}.png', flip=True))
        self.boltAnimFire[0].play()
        self.boltAnimFire[1].play()

        super().__init__(x, y, self.boltAnimFly[0], [50, 42, 28, 24])
        self.dmg = 10
        self.hp = 30
        self.xvel = Flyling.MOVE_SPEED
        self.last_blast = 0
        self.blast_row = 0
        self.gravity = 0
        self.blast_waiting = False

    def update(self, t, platforms, blanks, entities, player):
        if self.barriers is None:
            self.get_barriers_x(platforms, blanks)
        try:
            target_coords = player.sprites()[0].hitbox.center
        except IndexError:
            return
        super().update(t, platforms, blanks, entities, player)
        db = timetime.time() - self.last_blast
        if db > self.blast_delay and self.blast_row < 3 or db > self.blast_delay * 3:
            if self.blast_row >= 3:
                self.blast_row = 0
            d = abs(self.hitbox.centerx - target_coords[0]) + abs(
                self.hitbox.centery - target_coords[1])
            if d < 1000:
                if self.rect.x < target_coords[0]:
                    self.right = True
                    self.xvel = Flyling.MOVE_SPEED
                else:
                    self.right = False
                    self.xvel = -Flyling.MOVE_SPEED
            else:
                self.xvel = 0
            if d <= 600:
                self.boltAnimFire[self.right].play(0)
                self.last_blast = timetime.time()
                self.blast_row += 1
                self.blast_waiting = True

        if self.last_blast + 0.3 > timetime.time():
            if self.last_blast + 0.2 < timetime.time() and self.blast_waiting:
                if self.right:
                    blast = Blast(self.hitbox.right, self.hitbox.top, 1)
                else:
                    blast = Blast(self.hitbox.left - PLAT_W, self.hitbox.top, 1)
                self.eg.add(blast)
                self.ass.add(blast)
                self.blast_waiting = False
            self.image = self.boltAnimFire[self.right].getCurrentFrame()
        else:
            self.image = self.boltAnimFly[self.right].getCurrentFrame()

    def check_collision(self, xvel, yvel, platforms, blanks, entities, player):
        if self.collide(xvel, yvel, self.barriers, True):
            self.reverse()
            return True
        return False


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

        super().__init__(x, y, self.boltAnimRun[0], [PLAT_W * 48 // 32, PLAT_H * 36 // 32,
                                                     PLAT_W * 32 // 32, PLAT_H * 56 // 32])
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
                self.reverse()
            return x
        else:
            self.collide(xvel, yvel, entities, True,
                         filt=lambda s: s.xvel == self.xvel)
            a = self.collide(xvel, yvel, player, True)
            if a:
                self.make_dmg(a)
                return a
            return a


class Blast(Enemy):
    def __init__(self, x, y, target, size_c=2):
        self.target = target
        im = pygame.transform.scale(image.load("data/enemyframes/fireball.png"),
                                    (int(16 * size_c), int(16 * size_c)))
        anim = [pyganim.PygAnimation([(im, 99999)]),
                pyganim.PygAnimation([(pygame.transform.flip(im, True, False), 99999)])]
        anim[0].play()
        anim[1].play()
        super().__init__(x, y, anim[0], [int(5 * size_c), int(6 * size_c),
                                         int(5 * size_c), int(4 * size_c)])
        self.dmg = 5
        self.hero_coords = (0, 0)
        self.gravity = GRAVITY / 4
        self.xvel0 = 250
        self.xvel = 250
        self.yvel = 100

    def check_collision(self, xvel, yvel, platforms, blanks, entities, player):
        if self.collide(xvel, yvel, platforms, False):
            self.kill()
        if self.collide(xvel, yvel, player, False):
            self.kill()
        for i in entities:
            if isinstance(i, Enemy) and self.collide(xvel, yvel, (i,), False):
                if self.make_dmg(i):
                    break

    def update(self, t, platforms, blanks, entities, player):
        if len(player) > 0:
            if self.hitbox.right <= player.sprites()[0].hitbox.left:
                self.right = True
                self.xvel = self.xvel0
            elif self.hitbox.left >= player.sprites()[0].hitbox.right:
                self.right = False
                self.xvel = -self.xvel0
            else:
                self.xvel = 0
        super().update(t, platforms, blanks, entities, player)