# Импортируем все модули проекта
enemies_group = None
all_sprites = None

import os

from constants import *
from background import *
from pepe_hero import *
from platforms import *
from enemies import *
from boss import *
from bullet import *
from animation import *
import time as timetime  # time is already defined with pygame


class Keys:
    def __init__(self, left=False, right=False, up=False, down=False, shoot=False, hit=False):
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.shoot = shoot
        self.hit = hit


class Camera(object):
    def __init__(self, width, height):
        self.state = Rect(0, 0, width, height)

    def apply(self, rect):
        return rect.x - self.state.x, rect.y - self.state.y

    def update(self, target):
        x = target.rect.x - WIN_W // 2 + WIDTH // 2
        y = target.rect.y - WIN_H // 2 + HEIGHT // 2  # выравниваем камеру по центру
        x = max(PLAT_W // 2, x)  # Не движемся дальше левой границы
        # x = max(-(camera.width - WIN_WIDTH), x)  # Не движемся дальше правой границы
        # y = max(-(camera.height - WIN_HEIGHT), y)  # Не движемся дальше нижней границы
        y = max(PLAT_H // 2, y)  # Не движемся дальше верхней границы
        self.state.topleft = (x, y)


def load_level(filename):
    global MAX_WIDTH
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))
    MAX_WIDTH = max_width

    # дополняем каждую строку пустыми клетками (' ')
    return list(map(lambda x: x.ljust(max_width, ' '), level_map))


def load_image(name, colorkey=-1):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def start_level(level_name):
    global hero, hp, left, right, up, down, shoot, hit, enemies_group, bullets_group
    global all_sprites, platforms_group, boss_group, blanks_group, lava_group, player_group, entities_group
    global other_blocks, level, camera

    hero = Player(55, 555)
    hp = HitPoints(hero.hp)
    left = right = up = down = shoot = hit = False  # по умолчанию — стоим
    enemies_group = pygame.sprite.Group()
    bullets_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    platforms_group = pygame.sprite.Group()
    all_sprites.add(hero)
    boss_group = pygame.sprite.Group()
    blanks_group = pygame.sprite.Group()
    lava_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    player_group.add(hero)
    entities_group = pygame.sprite.Group()
    other_blocks = []
    level = load_level("level_1.txt")

    x = y = 0  # координаты
    for row in level:  # вся строка
        for sym in row:  # каждый символ
            if sym == "*":
                plat = Platform(x, y, None)
                platforms_group.add(plat)
                all_sprites.add(plat)
            elif sym in PLATFORMS_LEGEND.keys():
                plat = Platform(x, y, f"data/framestiles/tiles/{PLATFORMS_LEGEND[sym]}.png")
                platforms_group.add(plat)
                all_sprites.add(plat)
            elif sym == "U":
                uka = Uka(x, y)
                # enemies_group.add(uka)
                entities_group.add(uka)
                all_sprites.add(uka)
            elif sym == "b":
                blank = Blank(x, y)
                blanks_group.add(blank)
                all_sprites.add(blank)
            elif sym == "F":
                flyling = Flyling(x, y)
                flyling.eg = entities_group
                flyling.ass = all_sprites
                entities_group.add(flyling)
                all_sprites.add(flyling)
            elif sym == "L":
                lava = Lava(x, y)
                other_blocks.append(lava)
                all_sprites.add(lava)
                lava_group.add(lava)
            elif sym == "[":
                lava = Platform(x, y, "data/framestiles/tiles/lavaleft.png")
                other_blocks.append(lava)
                all_sprites.add(lava)
                platforms_group.add(lava)
            elif sym == "]":
                lava = Platform(x, y, "data/framestiles/tiles/lavaright.png")
                other_blocks.append(lava)
                all_sprites.add(lava)
                platforms_group.add(lava)
            elif sym == "S":
                spikes = Spikes(x, y, "data/framestiles/tiles/spikes.png")
                other_blocks.append(spikes)
                all_sprites.add(spikes)
                platforms_group.add(spikes)
            elif sym == "T":
                tp = Teleport(x, y)
                other_blocks.append(tp)
                all_sprites.add(tp)
                platforms_group.add(tp)
            elif sym == "I":
                ice = Ice(x, y, "data/framestiles/tiles/icecenter.png")
                all_sprites.add(ice)
                platforms_group.add(ice)
            elif sym == "(":
                ice = Ice(x, y, "data/framestiles/tiles/iceleft.png")
                all_sprites.add(ice)
                platforms_group.add(ice)
            elif sym == ")":
                ice = Ice(x, y, "data/framestiles/tiles/iceright.png")
                all_sprites.add(ice)
                platforms_group.add(ice)
            elif sym == "C":
                crack = Crackatoo(x, y)
                all_sprites.add(crack)
                entities_group.add(crack)
            elif sym == "B":
                boss = Boss(x, y)
                all_sprites.add(boss)
                boss_group.add(boss)

            x += PLAT_W  # блоки платформы ставятся на ширине блоков
        y += PLAT_H  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    total_level_width = len(level[0]) * PLAT_W  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLAT_H  # высоту
    camera = Camera(WIN_W, WIN_H)


def main():
    global hero, hp, left, right, up, down, shoot, hit, enemies_group, bullets_group
    global all_sprites, platforms_group, boss_group, blanks_group, lava_group, entities_group, player_group
    global other_blocks, level, camera

    pygame.init()  # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption("Pepe the Frog")  # Пишем в шапку
    background = Background('data/Background.jpg', [0, 0], WIN_W,
                            WIN_H)  # будем использовать как фон
    clock = pygame.time.Clock()

    start_level(CURRENT_LEVEL)

    prev_fps = 0
    while True:  # Основной цикл программы
        if hero.hp <= 0:
            start_level(CURRENT_LEVEL)
        t = clock.tick() / 1000
        for event in pygame.event.get():  # Обрабатываем события
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                raise SystemExit("QUIT")
            if event.type in (KEYUP, KEYDOWN):
                pressed = event.type == KEYDOWN
                if event.key == K_LEFT:
                    left = pressed
                elif event.key == K_RIGHT:
                    right = pressed
                elif event.key == K_UP:
                    up = pressed
                elif event.key == K_DOWN:
                    down = pressed
                elif event.key == K_c:
                    hit = pressed
                    if pressed and DEBUG:
                        print("c")
                        print(hero.hit_done, hit, left, right, up)
                elif event.key == K_z:
                    shoot = pressed
        hero.keys = Keys(left, right, up, down, shoot, hit)

        on_screen = pygame.sprite.Group()
        for i in platforms_group:
            if camera.state.colliderect(i.rect):
                on_screen.add(i)
        # передвижение
        hero.update(t, on_screen, blanks_group, enemies_group, player_group)
        camera.update(hero)
        lava_group.update()
        # tp.update()
        # boss_group.update(hero, hp, enemies_group, boss_attacks_group,
        #                   boss_attacks, all_sprites, enemies_group)
        # boss_attacks_group.update(enemies_group, hero, boss_attacks,
        #                           hp, enemies_group, all_sprites)
        enemies_group.update(blanks_group, platforms_group, [hero.hitbox.x, hero.hitbox.y],
                             enemies_group, all_sprites)
        entities_group.update(t, platforms_group, blanks_group, entities_group, player_group)
        bullets_group.update(t, platforms_group, blanks_group, entities_group, player_group)

        if timetime.time() - hero.shoot_start > 1 and shoot is True and hero.on_ground \
                or timetime.time() - hero.shoot_start > 5 and shoot:
            if DEBUG:
                print("bullet")
            if hero.right:
                bullet = Bullet(hero.hitbox.right, hero.hitbox.y + hero.hitbox.height // 8 * 3,
                                True)
            else:
                bullet = Bullet(hero.hitbox.left - 10, hero.hitbox.y + hero.hitbox.height // 8 * 3,
                                False)
            entities_group.add(bullet)
            all_sprites.add(bullet)
            hero.shoot_start = timetime.time()
        if hero.hit_done is False and hit is True and not left and not right and not up:
            if DEBUG:
                print("hit")
            smash = Hit(hero.rect.x + 32, hero.rect.y + 24, ('Left', 'Right')[hero.right])
            bullets_group.add(smash)
            all_sprites.add(smash)
            hero.hit_done = True

        screen.blit(background.image, background.rect)
        for i in all_sprites:
            if camera.state.colliderect(i.rect):
                coordi = camera.apply(i.rect)
                screen.blit(i.image, coordi)

        if DRAW_RECTS:
            for i in all_sprites:
                if camera.state.colliderect(i.rect):
                    coordi = camera.apply(i.rect)
                    pygame.draw.rect(screen, pygame.Color('blue'),
                        coordi + (i.rect.width, i.rect.height), 1)
        if DRAW_HITBOXES:
            for i in all_sprites:
                if camera.state.colliderect(i.rect):
                    coordi = camera.apply(i.rect)
                    if isinstance(i, Blank):
                        border_color = 'red4'
                    else:
                        border_color = 'red'
                    try:
                        pygame.draw.rect(screen, pygame.Color(border_color),
                                         camera.apply(i.hitbox) + (i.hitbox.width, i.hitbox.height),
                                         1)
                    except AttributeError:
                        pygame.draw.rect(screen, pygame.Color('purple4'),
                                         coordi + (i.rect.width, i.rect.height), 1)

        hp.draw(screen, hero.hp)
        pygame.display.flip()  # обновление и вывод всех изменений на экран
        if SHOW_FPS:
            if prev_fps != clock.get_fps():
                prev_fps = clock.get_fps()
                print('fps:', prev_fps)


if __name__ == "__main__":
    main()
