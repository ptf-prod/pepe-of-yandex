import pyganim

from entity import Entity
from enemies import *
from bullet import *
from main import Keys
from constants import *
import platforms as plat


class Player(Entity):
    MOVE_SPEED = 220
    JUMP_POWER = 355
    WIDTH, HEIGHT = PLAT_W * 4, PLAT_H * 4

    def __init__(self, x, y):
        self.boltAnimRun = (load_animation(0, 8, ANIMATION_DELAY, 'data', 'pepeframes', 'running',
                                           'runnin anim{:04d}.png', flip=True),
                            load_animation(0, 8, ANIMATION_DELAY, 'data', 'pepeframes', 'running',
                                           'runnin anim{:04d}.png'))
        self.boltAnimJump = (load_animation(0, 10, ANIMATION_DELAY, 'data', 'pepeframes', 'jump',
                                            'jump-anim{:04d}.png', flip=True),
                             load_animation(0, 10, ANIMATION_DELAY, 'data', 'pepeframes',
                                            'jump', 'jump-anim{:04d}.png'))
        self.boltAnimGun = (load_animation(0, 4, ANIMATION_DELAY, 'data', 'pepeframes', 'gun',
                                           'gun{:04d}.png', flip=True),
                            load_animation(0, 4, ANIMATION_DELAY, 'data', 'pepeframes', 'gun',
                                           'gun{:04d}.png'))
        self.boltAnimHit = (load_animation(0, 6, ANIMATION_DELAY, 'data', 'pepeframes', 'hit',
                                           'pepe molot anim{:04d}.png', flip=True),
                            load_animation(0, 6, ANIMATION_DELAY, 'data', 'pepeframes', 'hit',
                                           'pepe molot anim{:04d}.png'))
        self.boltAnimShoot = (load_animation(0, 4, ANIMATION_DELAY, 'data', 'pepeframes', 'shoot',
                                             'pepe shoot{:04d}.png', flip=True),
                              load_animation(0, 4, ANIMATION_DELAY, 'data', 'pepeframes', 'shoot',
                                             'pepe shoot{:04d}.png'))
        self.boltAnimStay = (load_animation(0, 5, ANIMATION_DELAY * 8, 'data', 'pepeframes',
                                            'idle', 'idle anim{:04d}.png', flip=True),
                             load_animation(0, 5, ANIMATION_DELAY * 8, 'data', 'pepeframes',
                                            'idle', 'idle anim{:04d}.png'))

        self.cur_anim = self.boltAnimStay[1]
        super().__init__(x, y, self.boltAnimStay[1].getCurrentFrame(),
                         [Player.WIDTH * 26 // 64, Player.HEIGHT * 7 // 32,
                          Player.WIDTH * 12 // 64, Player.HEIGHT // 2])
        self.hp = 100
        self.hit_take = True
        self.immortal_time = 0
        self.shot_done = False
        self.hit_done = False
        self.reload_time = 0
        self.hit_delay_time = 0
        self.burn_time = 0
        self.previous_block = ""
        self.block = ""
        self.shoot_start = 0
        self.keys = Keys()
        self.cur_anim = self.boltAnimStay
        self.hit = None

    def start_hit(self):
        self.hit = timetime.time()

    def update(self, t, platforms, blanks, entities, player):
        import time as timetime
        prev_anim = self.cur_anim
        self.cur_anim[self.right].pause()
        self.cur_anim = self.boltAnimRun
        if self.keys.left and not self.keys.right:
            self.right = False
            self.xvel = -Player.MOVE_SPEED  # Лево = x - n
        elif self.keys.right and not self.keys.left:
            self.right = True
            self.xvel = Player.MOVE_SPEED  # Право = x + n
        elif not self.keys.right and not self.keys.left:
            self.cur_anim = self.boltAnimStay
            self.xvel = 0
        elif self.right:
            self.xvel = Player.MOVE_SPEED  # Право = x + n
        else:
            self.xvel = -Player.MOVE_SPEED  # Лево = x - n

        if self.keys.down and not self.keys.up:
            if not self.on_ground:
                self.yvel += Player.JUMP_POWER // 2
                self.xvel = 0
        elif self.keys.up:
            if self.on_ground:  # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -Player.JUMP_POWER
                if self.block == "ice":
                    if not self.right:
                        self.xvel = -Player.MOVE_SPEED
                    else:
                        self.xvel = Player.MOVE_SPEED
            self.cur_anim = self.boltAnimJump

        if self.keys.shoot or self.shoot_start + 0.5 > timetime.time():
            self.cur_anim = self.boltAnimShoot
            self.xvel /= 1.5  # При стрельбе медленнее бежим
            if self.on_ground:
                self.yvel /= 1.5  # При стрельбе ниже прыгаем

        elif self.hit or self.hit_done:
            self.cur_anim = self.boltAnimHit
            if prev_anim != self.cur_anim:
                for i in self.boltAnimHit:
                    i.pause(0)
            self.hitbox = pygame.Rect(self.hitbox.centerx + 8 * PLAT_W // 32, self.hitbox.top,
                                      12 * PLAT_W // 32, self.hitbox.height)

        super().update(t, platforms, blanks, entities, player)

        self.cur_anim[self.right].play()
        self.image = self.cur_anim[self.right].getCurrentFrame()

    def take_dmg(self, who, dmg):
        if DEBUG:
            print(type(who).__name__)
        try:
            a = super().take_dmg(who, dmg)
            return a
        except AttributeError:
            h0 = self.hp
            if DEBUG:
                print('No .dmg', type(who))
            if type(who) == Uka:
                self.hp -= 10
                self.immortality()
            elif type(who) == Flyling:
                self.hp -= 15
                self.immortality()
            elif type(who) == Crackatoo:
                self.hp -= 20
                self.immortality()
            elif type(who) == Lava:
                self.hp -= 0.05
                self.previous_block = "lava"
                self.block = "lava"
            elif type(who) == Spikes:
                self.hp -= 15
                self.immortality()
            elif type(who) == Blast:
                self.hp -= who.dmg
            if self.hp < 0:
                return True, True
            else:
                return self.hp < h0, False

    def immortality(self):
        self.hit_take = False

    def check_portal(self, other_blocks):
        for ob in other_blocks:
            if sprite.collide_rect(self, ob):
                if type(ob) == Teleport:
                    return True


class HitPoints:
    def __init__(self, max_h):
        self.x = 50
        self.y = 50
        self.width = 200
        self.max = max_h
        self.height = 25
        self.dmg = 0

    def draw(self, screen, value):
        pygame.draw.rect(screen, Color("Red"), (self.x, self.y, self.width, self.height))
        if value > 0:
            pygame.draw.rect(screen, Color("Green"),
                             (self.x, self.y, value * self.width / self.max, self.height))
