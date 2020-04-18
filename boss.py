import pygame
import pyganim
from pygame import Surface, sprite, Rect, Color, image
import enemies
from animation import load_animation
from constants import *
import time

ANIMATION_DELAY = 100

ANIMATION_CLAP = ['data/bossframes/bossattack3/boss attack30000.png',
                  'data/bossframes/bossattack3/boss attack30001.png',
                  'data/bossframes/bossattack3/boss attack30002.png',
                  'data/bossframes/bossattack3/boss attack30003.png',
                  'data/bossframes/bossattack3/boss attack30004.png',
                  'data/bossframes/bossattack3/boss attack30005.png',
                  'data/bossframes/bossattack3/boss attack30006.png']

ANIMATION_STOMP = ['data/bossframes/bossattack2/boss attack20000.png',
                   'data/bossframes/bossattack2/boss attack20001.png',
                   'data/bossframes/bossattack2/boss attack20002.png',
                   'data/bossframes/bossattack2/boss attack20003.png',
                   'data/bossframes/bossattack2/boss attack20004.png',
                   'data/bossframes/bossattack2/boss attack20005.png',
                   'data/bossframes/bossattack2/boss attack20006.png',
                   'data/bossframes/bossattack2/boss attack20007.png',
                   'data/bossframes/bossattack2/boss attack20008.png']

ANIMATION_BLAST = ['data/bossframes/bossattack1/boss attack10000.png',
                   'data/bossframes/bossattack1/boss attack10001.png',
                   'data/bossframes/bossattack1/boss attack10002.png',
                   'data/bossframes/bossattack1/boss attack10003.png',
                   'data/bossframes/bossattack1/boss attack10004.png',
                   'data/bossframes/bossattack1/boss attack10005.png',
                   'data/bossframes/bossattack1/boss attack10006.png']

ANIMATION_WALK = ['data/bossframes/bosswalk/boss walk0000.png',
                  'data/bossframes/bosswalk/boss walk0001.png',
                  'data/bossframes/bosswalk/boss walk0002.png',
                  'data/bossframes/bosswalk/boss walk0003.png',
                  'data/bossframes/bosswalk/boss walk0004.png',
                  'data/bossframes/bosswalk/boss walk0005.png',
                  'data/bossframes/bosswalk/boss walk0006.png',
                  'data/bossframes/bosswalk/boss walk0007.png']


class Boss(enemies.Enemy):
    def __init__(self, x, y, eg, ass):
        self.ass = ass
        self.eg = eg
        self.boltAnimWalk = (load_animation(0, 8, ANIMATION_DELAY, 'data', 'bossframes',
                                            'bosswalk', 'boss walk{:04d}.png', size=(512, 512)),
                             load_animation(0, 8, ANIMATION_DELAY, 'data', 'bossframes',
                                            'bosswalk', 'boss walk{:04d}.png', flip=True, size=(512, 512)))
        self.boltAnimBlast = (load_animation(0, 7, ANIMATION_DELAY, 'data', 'bossframes',
                                            'bossattack1', 'boss attack1{:04d}.png', size=(512, 512)),
                             load_animation(0, 7, ANIMATION_DELAY, 'data', 'bossframes',
                                            'bossattack1', 'boss attack1{:04d}.png', flip=True, size=(512, 512)))
        self.boltAnimStomp = (load_animation(0, 9, ANIMATION_DELAY, 'data', 'bossframes',
                                            'bossattack2', 'boss attack2{:04d}.png', size=(512, 512)),
                             load_animation(0, 9, ANIMATION_DELAY, 'data', 'bossframes',
                                            'bossattack2', 'boss attack2{:04d}.png', flip=True, size=(512, 512)))
        self.boltAnimClap = (load_animation(0, 7, ANIMATION_DELAY, 'data', 'bossframes',
                                            'bossattack3', 'boss attack3{:04d}.png', size=(512, 512)),
                             load_animation(0, 7, ANIMATION_DELAY, 'data', 'bossframes',
                                            'bossattack3', 'boss attack3{:04d}.png', flip=True, size=(512, 512)))
        super().__init__(x, y - PLAT_H * 400 // 32, self.boltAnimWalk[0], [PLAT_W * 44 // 32, PLAT_H * 56 // 32,
                                                                           PLAT_W * 44 // 32, PLAT_H * 36 // 32])
        self.gravity = 0
        self.last_hit = [0, None]  # Время последнего удара, на всякий случай его вид
        self.attacks = pygame.sprite.Group()

        self.xvel = 1
        self.start_x = x
        self.start_y = y
        self.hp = 100
        self.attack = False
        self.attack_delay = 0
        self.direction = ""
        self.walk = True
        self.stand_time = 0
        self.clap = False
        self.stomp = False
        self.blast = False
        bolt_anim = []
        for anim in ANIMATION_WALK:
            bolt_anim.append((pygame.transform.flip(
                pygame.transform.scale(image.load(anim), (512, 512)), True, False),
                             ANIMATION_DELAY))
        self.boltAnimWalkRight = pyganim.PygAnimation(bolt_anim)
        self.boltAnimWalkRight.play()

        bolt_anim = []
        for anim in ANIMATION_WALK:
            bolt_anim.append((pygame.transform.scale(image.load(anim), (512, 512)), ANIMATION_DELAY))
        self.boltAnimWalkLeft = pyganim.PygAnimation(bolt_anim)
        self.boltAnimWalkLeft.play()
        self.boltAnimWalkLeft.blit(self.image, (0, 0))

        bolt_anim = []
        for anim in ANIMATION_CLAP:
            bolt_anim.append((pygame.transform.flip(
                pygame.transform.scale(image.load(anim), (512, 512)), True, False),
                             ANIMATION_DELAY))
        self.boltAnimClapRight = pyganim.PygAnimation(bolt_anim)
        self.boltAnimClapRight.play()

        bolt_anim = []
        for anim in ANIMATION_CLAP:
            bolt_anim.append((pygame.transform.scale(image.load(anim), (512, 512)),
                              ANIMATION_DELAY))
        self.boltAnimClapLeft = pyganim.PygAnimation(bolt_anim)
        self.boltAnimClapLeft.play()

        bolt_anim = []
        for anim in ANIMATION_STOMP:
            bolt_anim.append((pygame.transform.flip(
                pygame.transform.scale(image.load(anim), (512, 512)), True, False),
                             ANIMATION_DELAY))
        self.boltAnimStompRight = pyganim.PygAnimation(bolt_anim)
        self.boltAnimStompRight.play()

        bolt_anim = []
        for anim in ANIMATION_STOMP:
            bolt_anim.append((pygame.transform.scale(image.load(anim), (512, 512)),
                              ANIMATION_DELAY))
        self.boltAnimStompLeft = pyganim.PygAnimation(bolt_anim)
        self.boltAnimStompLeft.play()

        bolt_anim = []
        for anim in ANIMATION_BLAST:
            bolt_anim.append((pygame.transform.flip(
                pygame.transform.scale(image.load(anim), (512, 512)), True, False),
                             ANIMATION_DELAY))
        self.boltAnimBlastRight = pyganim.PygAnimation(bolt_anim)
        self.boltAnimBlastRight.play()

        bolt_anim = []
        for anim in ANIMATION_BLAST:
            bolt_anim.append((pygame.transform.scale(image.load(anim), (512, 512)),
                              ANIMATION_DELAY))
        self.boltAnimBlastLeft = pyganim.PygAnimation(bolt_anim)
        self.boltAnimBlastLeft.play()

    def update(self, t, platforms, blanks, entities, player):
        try:
            target_coords = player.sprites()[0].hitbox.center
        except IndexError:
            return
        old_anim = self.cur_anim
        if self.cur_anim not in self.boltAnimWalk:
            if time.time() * TIMESCALE - self.last_hit[0] > self.cur_anim.numFrames * ANIMATION_DELAY / 1000:
                self.cur_anim = self.boltAnimWalk[self.right]
        if self.cur_anim in self.boltAnimWalk:
            if self.rect.x - 512 <= target_coords[0] <= self.rect.x + 640 and time.time() - self.last_hit[0] > 5:
                if DEBUG:
                    print("blast")
                blast = BossHit(self.rect.x, self.rect.y, self, "blast", enemies, self.ass)
                self.attacks.add(blast)
                self.cur_anim = self.boltAnimBlast[self.right]
                self.last_hit = [time.time() * TIMESCALE, 'blast']

        self.attacks.update(t, platforms, blanks, entities, player)

        # if self.attack:
        #     if self.rect.x - 64 <= hero.rect.x:
        #         print('clapLeft')
        #         clap = BossHit(self.rect.x, self.rect.y, self, "clap", enemies, enemies_group,
        #                        all_sprites)
        #         all_sprites.add(clap)
        #         boss_attacks.append(clap)
        #         boss_attacks_group.add(clap)
        #         self.attack = False
        #         self.walk = False
        #         self.clap = True
        #     elif self.rect.x + 160 >= hero.rect.x:
        #         print('clapRight')
        #         clap = BossHit(self.rect.x, self.rect.y, self, "clap", enemies, enemies_group,
        #                        all_sprites)
        #         all_sprites.add(clap)
        #         boss_attacks.append(clap)
        #         boss_attacks_group.add(clap)
        #         self.attack = False
        #         self.walk = False
        #         self.clap = True
        #     elif self.rect.x - 512 >= hero.rect.x >= self.rect.x + 640 and hero.rect.y <= self.rect.y + 300:
        #         print('stomp')
        #         stomp = BossHit(self.rect.x, self.rect.y, self, "stomp", enemies, enemies_group,
        #                         all_sprites)
        #         all_sprites.add(stomp)
        #         boss_attacks.append(stomp)
        #         boss_attacks_group.add(stomp)
        #         self.attack = False
        #         self.walk = False
        #         self.stomp = True
        #     elif self.rect.x - 512 <= hero.rect.x <= self.rect.x + 640:
        #         print('blast')
        #         blast = BossHit(self.rect.x, self.rect.y, self, "blast", enemies, enemies_group,
        #                         all_sprites)
        #         all_sprites.add(blast)
        #         boss_attacks.append(blast)
        #         boss_attacks_group.add(blast)
        #         self.walk = False
        #         self.blast = True
        # if not self.attack and self.walk is True:
        #     if self.rect.x + 160 < hero.rect.x:
        #         self.rect.x += self.xvel
        #         self.direction = "Right"
        #         self.image.fill(Color("Red"))
        #         self.boltAnimWalkRight.blit(self.image, (0, 0))
        #     elif self.rect.x + 160 > hero.rect.x:
        #         self.rect.x -= self.xvel
        #         self.direction = "Left"
        #         self.image.fill(Color("Red"))
        #         self.boltAnimWalkLeft.blit(self.image, (0, 0))
        #     self.attack_delay += 1
        #     if self.attack_delay == 300:
        #         print("blast")
        #         blast = BossHit(self.rect.x, self.rect.y, self, "blast", enemies, enemies_group,
        #                         all_sprites)
        #         all_sprites.add(blast)
        #         boss_attacks.append(blast)
        #         boss_attacks_group.add(blast)
        #         self.blast = True
        #         self.walk = False
        #     elif self.attack_delay == 450:
        #         self.attack_delay = 0
        #         self.attack = True
        #     if self.hp <= 0:
        #         self.kill()
        #         del enemies[enemies.index(self)]

        if not self.walk and self.clap:
            if self.direction == "Right":
                self.image.fill(Color("Red"))
                self.boltAnimClapRight.blit(self.image, (0, 0))
            else:
                self.image.fill(Color("Red"))
                self.boltAnimClapLeft.blit(self.image, (0, 0))

        elif not self.walk and self.stomp:
            if self.direction == "Right":
                self.image.fill(Color("Red"))
                self.boltAnimStompRight.blit(self.image, (0, 0))
            else:
                self.image.fill(Color("Red"))
                self.boltAnimStompLeft.blit(self.image, (0, 0))

        elif not self.walk and self.blast:
            if self.direction == "Right":
                self.image.fill(Color("Red"))
                self.boltAnimBlastRight.blit(self.image, (0, 0))
            else:
                self.image.fill(Color("Red"))
                self.boltAnimBlastLeft.blit(self.image, (0, 0))

        if not self.walk:
            self.stand_time += 1
            if self.stand_time == 30:
                self.walk = True
                self.stand_time = 0

        if old_anim != self.cur_anim:
            old_anim.pause()
            self.cur_anim.currentFrameNum = 0
            self.cur_anim.play()
        self.image = self.cur_anim.getCurrentFrame()

    # def take_dmg(self, dmg):
    #     self.hp -= dmg
    #     print(self.hp)
    #     if self.hp <= 0:
    #         self.kill()


class BossHit(sprite.Sprite):
    def __init__(self, x, y, boss, hit_type, entities_group, all_sprites):
        sprite.Sprite.__init__(self)
        self.boss = boss
        self.start_x = x
        self.start_y = y
        self.type = hit_type
        self.start_time = time.time() * TIMESCALE
        self.delay = -1

        if hit_type == "clap":
            if boss.direction == "Right":
                self.xvel = 100
            else:
                self.xvel = -100
            self.image = Surface((128, 256))
            self.rect = Rect(x + 64, y + 128, 128, 256)  # прямоугольный объект
        elif hit_type == "stomp":
            if boss.direction == "Right":
                self.xvel = 100
            else:
                self.xvel = -100
            self.image = Surface((128, 64))
            self.rect = Rect(x + 64, y + 192, 128, 64)  # прямоугольный объект
        elif False:
            if boss.direction == "Right":
                self.xvel = 100
                boss.calp = True
            else:
                self.xvel = -100
            self.image = Surface((64, 64))
            self.rect = Rect(x + 64, y + 256, 256, 64)  # прямоугольный объект
            boss_blast = enemies.Blast(self.rect.x, self.rect.y - 64, 1, 4, 50)
            entities_group.add(boss_blast)
            all_sprites.add(boss_blast)

    def update(self, t, platforms, blanks, entities, player):

        # self.rect.x += self.xvel  # переносим положение на xvel
        # self.collide(hero, hp, enemies, enemies_group, all_sprites)
        # self.check_range(boss_bullets)
        if self.type == 'blast' and time.time() * TIMESCALE - self.start_time > 2:
            boss_blast = enemies.Blast(self.boss.rect.x, self.boss.rect.y - 64, 1, 4, 50)
            self.boss.eg.add(boss_blast)
            self.boss.ass.add(boss_blast)
            self.kill()
            return

    def collide(self, hero, hp, enemies, enemies_group, all_sprites):
        if sprite.collide_rect(self, hero):
            if self.type == "clap":
                hero.hp -= 100
                hp.dmg += 100
                self.kill()
            elif self.type == "stomp":
                hero.hp -= 75
                hp.dmg += 75
                self.kill()
            else:
                hero.hp -= 49
                hp.dmg += 49
                self.kill()

    def check_range(self, boss_bullets):
        if self.type == "clap":
            if self.rect.x >= self.start_x + 128 or self.rect.x <= self.start_x - 128:
                print("kill")
                self.kill()
                del boss_bullets[boss_bullets.index(self)]
        elif self.type == "stomp":
            if self.rect.x >= self.start_x + 512 or self.rect.x <= self.start_x - 512:
                print("kill")
                self.kill()
                del boss_bullets[boss_bullets.index(self)]
        else:
            if self.rect.x >= self.start_x + 128 or self.rect.x <= self.start_x - 128:
                print("kill")
                self.kill()
                del boss_bullets[boss_bullets.index(self)]
