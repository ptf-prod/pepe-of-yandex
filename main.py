# Импортируем все модули проекта

import os

from background import *
from pepe_hero import *
from platforms import *
from enemies import *
from boss import *
from bullet import *
from animation import *

draw_hitboxes = True
draw_rects = True
show_fps = True

# Объявляем константы
WIN_WIDTH = 1280  # Ширина создаваемого окна
WIN_HEIGHT = 720  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = (50, 150, 255)
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"
LEVEL = 1
MAX_WIDTH = 0
MAX_HEIGHT = 0


class Camera(object):
    def __init__(self, width, height):
        self.state = Rect(0, 0, width, height)

    def apply(self, rect):
        return rect.x - self.state.x, rect.y - self.state.y

    def update(self, target):
        x = target.rect.x - WIN_WIDTH // 2 + WIDTH // 2
        y = target.rect.y - WIN_HEIGHT // 2 + HEIGHT // 2  # выравниваем камеру по центру
        x = max(PLATFORM_WIDTH // 2, x)  # Не движемся дальше левой границы
        # x = max(-(camera.width - WIN_WIDTH), x)  # Не движемся дальше правой границы
        # y = max(-(camera.height - WIN_HEIGHT), y)  # Не движемся дальше нижней границы
        y = max(PLATFORM_HEIGHT // 2, y)  # Не движемся дальше верхней границы
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


def main():
    global LEVEL
    pygame.init()  # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Pepe the Frog")  # Пишем в шапку
    background = Background('data/Background.jpg', [0, 0], WIN_WIDTH, WIN_HEIGHT)
    # будем использовать как фон
    hero = Player(55, 555)
    hp = HitPoints(hero.hp)

    # создаем героя по (x,y) координатам
    left = right = up = down = blast = hit = False  # по умолчанию — стоим
    enemies_group = pygame.sprite.Group()
    bullets_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    platforms_group = pygame.sprite.Group()
    all_sprites.add(hero)
    boss_group = pygame.sprite.Group()
    blanks_group = pygame.sprite.Group()
    lava_group = pygame.sprite.Group()
    other_blocks = []
    timer = pygame.time.Clock()
    level = load_level("level_1.txt")

    x = y = 0  # координаты
    platforms_legend = {
        'G': 'up',
        '/': 'upleft',
        '\\': 'upright',
        'R': 'centre',
        '<': 'left',
        '>': 'right',
        '_': 'down',
        '-': 'downleft',
        '+': 'downright',
        '=': 'incline',
        '%': 'outcline',
        '.': 'alonecentre',
        '{': 'aloneleft',
        '}': 'aloneright',
        '^': 'alone',
        '?': 'aloneconnectleft',
        '!': 'connectleft',
        '#': 'aloneconnectright',
        '@': 'connectright',
    }
    for row in level:  # вся строка
        for sym in row:  # каждый символ
            if sym == "*":
                plat = Platform(x, y, None)
                platforms_group.add(plat)
                all_sprites.add(plat)
            elif sym in platforms_legend.keys():
                plat = Platform(x, y, f"data/framestiles/tiles/{platforms_legend[sym]}.png")
                platforms_group.add(plat)
                all_sprites.add(plat)
            elif sym == "U":
                uka = Uka(x, y)
                enemies_group.add(uka)
                all_sprites.add(uka)
            elif sym == "b":
                blank = Blank(x, y)
                blanks_group.add(blank)
                all_sprites.add(blank)
            elif sym == "F":
                flyling = Flyling(x, y)
                enemies_group.add(flyling)
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
                enemies_group.add(crack)
            elif sym == "B":
                boss = Boss(x, y)
                all_sprites.add(boss)
                boss_group.add(boss)


            x += PLATFORM_WIDTH   # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # высоту

    camera = Camera(WIN_WIDTH, WIN_HEIGHT)
    import time as timetime
    prev_time = timetime.time()

    while True:  # Основной цикл программы
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
                    if pressed:
                        print("c")
                        print(hero.hit_done, hit, left, right, up)
                elif event.key == K_z:
                    blast = pressed
        if hero.shot_done is False and blast is True and not left and not right and not up:
            print("bullet")
            bullet = Bullet(hero.rect.x + 75, hero.rect.y + 54, ('Left', 'Right')[hero.right])
            bullets_group.add(bullet)
            all_sprites.add(bullet)
            hero.shot_done = True
        if hero.hit_done is False and hit is True and not left and not right and not up:
            print("hit")
            smash = Hit(hero.rect.x + 32, hero.rect.y + 24, ('Left', 'Right')[hero.right])
            bullets_group.add(smash)
            all_sprites.add(smash)
            hero.hit_done = True

        on_screen = pygame.sprite.Group()
        for i in platforms_group:
            if camera.state.colliderect(i.rect):
                on_screen.add(i)

        screen.blit(background.image, background.rect)
        # передвижение
        hero.update(left, right, up, on_screen, down, enemies_group, other_blocks)
        camera.update(hero)
        lava.update()
        tp.update()
        # boss_group.update(hero, hp, enemies_group, boss_attacks_group,
        #                   boss_attacks, all_sprites, enemies_group)
        # boss_attacks_group.update(enemies_group, hero, boss_attacks,
        #                           hp, enemies_group, all_sprites)
        enemies_group.update(blanks_group, platforms_group, [hero.rect.x, hero.rect.y],
                             enemies_group, all_sprites)
        bullets_group.update(enemies_group, platforms_group, bullets_group)
        for i in all_sprites:
            if camera.state.colliderect(i.rect):
                coordi = camera.apply(i.rect)
                screen.blit(i.image, coordi)
                if draw_rects:
                    pygame.draw.rect(screen, pygame.Color('blue'),
                                     coordi + (i.rect.width, i.rect.height), 1)
                if draw_hitboxes:
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
        # timer.tick(60)
        if show_fps:
            print('fps:', 1 / (timetime.time() - prev_time))
            prev_time = timetime.time()


if __name__ == "__main__":
    main()
