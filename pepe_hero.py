import pyganim

from enemies import *
from bullet import *

ANIMATION_DELAY = 100
MOVE_SPEED = 220
WIDTH = 128
HEIGHT = 128
COLOR = "#888888"
JUMP_POWER = 355
GRAVITY = 400  # Сила, которая будет тянуть нас вниз


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        self.start_x = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.start_y = y
        self.image = Surface((WIDTH, HEIGHT))
        self.image.set_colorkey(Color(COLOR))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)  # прямоугольный объект
        self.yvel = 0  # скорость вертикального перемещения
        self.on_ground = False  # На земле ли я?
        self.right = True
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

        self.cur_anim = self.boltAnimStay
        self.hitbox = pygame.Rect(x + WIDTH * 3 // 8, y + HEIGHT * 7 // 32,
                                  WIDTH // 4, HEIGHT // 2)

    def update(self, t, keys, platforms, other_blocks, enemies):
        import time as timetime
        self.cur_anim[self.right].pause()
        self.cur_anim = self.boltAnimRun
        if keys.left and not keys.right:
            self.right = False
            self.xvel = -MOVE_SPEED  # Лево = x - n
        elif keys.right and not keys.left:
            self.right = True
            self.xvel = MOVE_SPEED  # Право = x + n
        elif not keys.right and not keys.left:
            self.cur_anim = self.boltAnimStay
            self.xvel = 0
            if not keys.up:
                self.image.fill(Color(COLOR))
        elif self.right:
            self.xvel = MOVE_SPEED  # Право = x + n
        else:
            self.xvel = -MOVE_SPEED  # Лево = x - n

        if keys.down and not keys.up:
            if not self.on_ground:
                self.yvel += JUMP_POWER // 2
                self.xvel = 0
        elif keys.up:
            if self.on_ground:  # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER
                if self.block == "ice":
                    if not self.right:
                        self.xvel = -MOVE_SPEED
                    else:
                        self.xvel = MOVE_SPEED
            self.cur_anim = self.boltAnimJump

        if not self.on_ground:
            self.yvel += GRAVITY * t

        if keys.shoot or self.shoot_start + 0.5 > timetime.time():
            self.image.fill(Color(COLOR))
            self.cur_anim = self.boltAnimShoot
            self.xvel /= 1.5  # При стрельбе медленнее бежим
            if self.on_ground:
                self.yvel /= 1.5  # При стрельбе ниже прыгаем

        if self.hit_done is True:
            self.cur_anim = self.boltAnimHit
            self.hit_delay_time += 1
            if self.hit_delay_time == 45:
                self.hit_done = False
                self.hit_delay_time = 0

        self.on_ground = False
        dy = self.yvel * t
        dx = self.xvel * t

        if self.yvel > 0:
            self.hitbox.y += min(dy, PLATFORM_HEIGHT)
        else:
            self.hitbox.y -= min(-dy, PLATFORM_HEIGHT)
        self.collide(0, self.yvel, platforms, enemies)

        if self.xvel > 0:
            self.hitbox.x += min(dx, PLATFORM_WIDTH)
        else:
            self.hitbox.x -= min(-dx, PLATFORM_WIDTH)
        self.collide(self.xvel, 0, platforms, enemies)

        if self.hit_take is False:
            self.immortal_time += 1
            if self.immortal_time == 120:
                self.hit_take = True
                self.immortal_time = 0

        if self.previous_block == "lava" and self.block != "lava":
            self.hp -= 0.1
            self.burn_time += 1
            if self.burn_time == 200 and self.block != "lava":
                self.burn_time = 0
                self.previous_block = ""

        self.rect.x = self.hitbox.x - WIDTH * 3 // 8
        self.rect.y = self.hitbox.y - HEIGHT * 7 // 32
        self.image.fill(Color(COLOR))
        self.cur_anim[self.right].play()
        self.cur_anim[self.right].blit(self.image, (0, 0))

    def collide(self, xvel, yvel, platforms, enemies):
        ok = False
        while not ok:
            ok = True
            for p in platforms:
                if self.hitbox.colliderect(p.hitbox):  # если есть пересечение платформы с игроком
                    self.block = "platform"
                    if xvel > 0:  # если движется вправо
                        t = self.hitbox.x
                        self.hitbox.right = p.hitbox.left  # то не движется вправо
                        self.rect.x += self.hitbox.x - t

                    if xvel < 0:  # если движется влево
                        t = self.hitbox.x
                        self.hitbox.left = p.hitbox.right  # то не движется вправо
                        self.rect.x += self.hitbox.x - t

                    if yvel > 0:  # если падает вниз
                        t = self.hitbox.y
                        self.hitbox.bottom = p.hitbox.top  # то не падает вниз
                        self.rect.y += self.hitbox.y - t
                        self.on_ground = True  # и становится на что-то твердое
                        self.yvel = 0  # и энергия падения пропадает

                    if yvel < 0:  # если движется вверх
                        t = self.hitbox.y
                        self.hitbox.top = p.hitbox.bottom  # то не движется вверх
                        self.rect.y += self.hitbox.y - t
                        self.yvel = 0  # и энергия прыжка пропадает
                    if type(p) == Ice:
                        self.previous_block = self.block
                        self.block = "ice"
                    if p.hurts and sprite.collide_rect(self, p):
                        self.take_dmg(p)
                        self.block = f"{p}"

                    ok = False
                    break

        if self.hit_take is True:
            for e in enemies:
                try:
                    if self.hitbox.colliderect(e.hitbox):
                        self.take_dmg(e)
                        if type(e) == Blast:
                            e.kill()
                except AttributeError:
                    if self.hitbox.colliderect(e.rect):
                        self.take_dmg(e)
                        if type(e) == Blast:
                            e.kill()

    def take_dmg(self, enemy):
        print(type(enemy).__name__)
        if type(enemy) == Uka:
            self.hp -= 10
            self.immortality()
        elif type(enemy) == Flyling:
            self.hp -= 15
            self.immortality()
        elif type(enemy) == Crackatoo:
            self.hp -= 20
            self.immortality()
        elif type(enemy) == Lava:
            self.hp -= 0.05
            self.previous_block = "lava"
            self.block = "lava"
        elif type(enemy) == Spikes:
            self.hp -= 15
            self.immortality()
        elif type(enemy) == Blast:
            self.hp -= enemy.dmg
        if self.hp <= 0:
            self.die()

    def die(self):
        self.kill()

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
