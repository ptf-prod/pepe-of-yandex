# Импортируем все модули проекта

import os

from Background import *
from PepeHero import *
from Platforms import *
from Enemies import *
from Boss import *
from Bullet import *
from Animation import *

# Объявляем константы
WIN_WIDTH = 800  # Ширина создаваемого окна
WIN_HEIGHT = 640  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = (50, 150, 255)
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"
LEVEL = 1
MAX_WIDTH = 0
MAX_HEIGHT = 0


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    x, y = target_rect[0], target_rect[1]  # координаты игрока
    w, h = camera[2], camera[3]  # размер окна
    x, y = -x + WIN_WIDTH / 2, -y + WIN_HEIGHT / 2  # выравниваем камеру по центру

    x = min(0, x)  # Не движемся дальше левой границы
    x = max(-(camera.width - WIN_WIDTH), x)  # Не движемся дальше правой границы
    y = max(-(camera.height - WIN_HEIGHT), y)  # Не движемся дальше нижней границы
    y = min(0, y)  # Не движемся дальше верхней границы
    return Rect(x, y, w, h)


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
    screen = pygame.display.set_mode((1280, 720))
    w, h = pygame.display.get_surface().get_size()
    pygame.display.set_caption("Pepe the Frog")  # Пишем в шапку
    background = Background('data/Background.jpg', [0, 0], w, h)
    # будем использовать как фон
    hero = Player(55, 555)
    hp = HitPoints()

    # создаем героя по (x,y) координатам
    left = right = up = down = blast = hit = False  # по умолчанию — стоим
    enemies_group = pygame.sprite.Group()
    lava_group = pygame.sprite.Group()
    bullets_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(hero)
    boss_group = pygame.sprite.Group()
    boss_attacks_group = pygame.sprite.Group()
    platforms = []  # то, во что мы будем врезаться или опираться
    enemies = []  # Враги
    blanks = []
    boss_attacks = []
    other_blocks = []
    bullets = []
    timer = pygame.time.Clock()
    level = load_level("level_1.txt")

    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "G":
                plat = Platform(x, y, "data/framestiles/tiles/up.png")
                platforms.append(plat)
                all_sprites.add(plat)
            if col == "*":
                plat = Platform(x, y, None)
                platforms.append(plat)
                all_sprites.add(plat)
            elif col == "/":
                plat = Platform(x, y, "data/framestiles/tiles/upleft.png")
                platforms.append(plat)
                all_sprites.add(plat)
            elif col == "\\":
                plat = Platform(x, y, "data/framestiles/tiles/upright.png")
                platforms.append(plat)
                all_sprites.add(plat)
            elif col == "R":
                plat = Platform(x, y, "data/framestiles/tiles/centre.png")
                platforms.append(plat)
                all_sprites.add(plat)
            elif col == "<":
                plat = Platform(x, y, "data/framestiles/tiles/left.png")
                platforms.append(plat)
                all_sprites.add(plat)
            elif col == ">":
                plat = Platform(x, y, "data/framestiles/tiles/right.png")
                platforms.append(plat)
                all_sprites.add(plat)
            elif col == "_":
                plat = Platform(x, y, "data/framestiles/tiles/down.png")
                platforms.append(plat)
                all_sprites.add(plat)
            elif col == "-":
                plat = Platform(x, y, "data/framestiles/tiles/downleft.png")
                platforms.append(plat)
                all_sprites.add(plat)
            elif col == "+":
                plat = Platform(x, y, "data/framestiles/tiles/downright.png")
                platforms.append(plat)
                all_sprites.add(plat)
            elif col == "=":
                plat = Platform(x, y, "data/framestiles/tiles/incline.png")
                platforms.append(plat)
                all_sprites.add(plat)
            elif col == "%":
                plat = Platform(x, y, "data/framestiles/tiles/outcline.png")
                plat.image = pygame.transform.flip("data/framestiles/tiles/incline.png", True, False)
                platforms.append(plat)
                all_sprites.add(plat)
            elif col == ".":
                plat = Platform(x, y, "data/framestiles/tiles/alonecentre.png")
                platforms.append(plat)
                all_sprites.add(plat)
            elif col == "{":
                plat = Platform(x, y, "data/framestiles/tiles/aloneleft.png")
                platforms.append(plat)
                all_sprites.add(plat)
            elif col == "}":
                plat = Platform(x, y, "data/framestiles/tiles/aloneright.png")
                platforms.append(plat)
                all_sprites.add(plat)
            elif col == "^":
                plat = Platform(x, y, "data/framestiles/tiles/alone.png")
                platforms.append(plat)
                all_sprites.add(plat)
            elif col == "?":
                plat = Platform(x, y, "data/framestiles/tiles/aloneconnectleft.png")
                platforms.append(plat)
                all_sprites.add(plat)
            elif col == "!":
                plat = Platform(x, y, "data/framestiles/tiles/connectleft.png")
                platforms.append(plat)
                all_sprites.add(plat)
            elif col == "#":
                plat = Platform(x, y, "data/framestiles/tiles/aloneconnectright.png")
                platforms.append(plat)
                all_sprites.add(plat)
            elif col == "@":
                plat = Platform(x, y, "data/framestiles/tiles/connectright.png")
                platforms.append(plat)
                all_sprites.add(plat)
            elif col == "U":
                uka = Uka(x, y)
                enemies.append(uka)
                enemies_group.add(uka)
                all_sprites.add(uka)
            elif col == "b":
                blank = Blank(x, y)
                blanks.append(blank)
                all_sprites.add(blank)
            elif col == "F":
                flyling = Flyling(x, y)
                enemies.append(flyling)
                enemies_group.add(flyling)
                all_sprites.add(flyling)
            elif col == "L":
                lava = Lava(x, y)
                other_blocks.append(lava)
                all_sprites.add(lava)
                lava_group.add(lava)
            elif col == "[":
                lava = Platform(x, y, "data/framestiles/tiles/lavaleft.png")
                other_blocks.append(lava)
                all_sprites.add(lava)
            elif col == "]":
                lava = Platform(x, y, "data/framestiles/tiles/lavaright.png")
                other_blocks.append(lava)
                all_sprites.add(lava)
            elif col == "S":
                spikes = Spikes(x, y, "data/framestiles/tiles/spikes.png")
                other_blocks.append(spikes)
                all_sprites.add(spikes)
            elif col == "T":
                tp = Teleport(x, y)
                other_blocks.append(tp)
                all_sprites.add(tp)
            elif col == "I":
                ice = Ice(x, y, "data/framestiles/tiles/icecenter.png")
                platforms.append(ice)
                all_sprites.add(ice)
            elif col == "(":
                ice = Ice(x, y, "data/framestiles/tiles/iceleft.png")
                platforms.append(ice)
                all_sprites.add(ice)
            elif col == ")":
                ice = Ice(x, y, "data/framestiles/tiles/iceright.png")
                platforms.append(ice)
                all_sprites.add(ice)
            elif col == "C":
                crack = Crackatoo(x, y)
                all_sprites.add(crack)
                enemies.append(crack)
                enemies_group.add(crack)
            elif col == "B":
                boss = Boss(x, y)
                all_sprites.add(boss)
                enemies.append(boss)
                boss_group.add(boss)

            x += PLATFORM_WIDTH   # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)

    while 1:  # Основной цикл программы
        for event in pygame.event.get():  # Обрабатываем события
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                raise SystemExit("QUIT")
            if event.type == KEYDOWN and event.key == K_LEFT:
                left = True
            elif event.type == KEYUP and event.key == K_LEFT:
                left = False
            if event.type == KEYDOWN and event.key == K_RIGHT:
                right = True
            elif event.type == KEYUP and event.key == K_RIGHT:
                right = False
            if event.type == KEYDOWN and event.key == K_UP:
                up = True
            elif event.type == KEYUP and event.key == K_UP:
                up = False
            if event.type == KEYDOWN and event.key == K_DOWN:
                down = True
            elif event.type == KEYUP and event.key == K_DOWN:
                down = False
            if event.type == KEYDOWN and event.key == K_c:
                print("c")
                hit = True
                print(hero.hit_done, hit, left, right, up)
            if event.type == KEYUP and event.key == K_c:
                hit = False
            if event.type == KEYDOWN and event.key == K_z:
                blast = True
            elif event.type == KEYUP and event.key == K_z:
                blast = False
        if hero.shot_done is False and blast is True and not left and not right and not up:
            print("bullet")
            bullet = Bullet(hero.rect.x + 75, hero.rect.y + 54, hero.previosly_move)
            bullets.append(bullet)
            bullets_group.add(bullet)
            all_sprites.add(bullet)
            hero.shot_done = True
        if hero.hit_done is False and hit is True and not left and not right and not up:
            print("hit")
            smash = Hit(hero.rect.x + 32, hero.rect.y + 24, hero.previosly_move)
            bullets.append(smash)
            bullets_group.add(smash)
            all_sprites.add(smash)
            hero.hit_done = True
        screen.fill([255, 255, 255])
        screen.blit(background.image, background.rect)

        hero.update(left, right, up, platforms, down, enemies, screen, hp, other_blocks)  # передвижение
        camera.update(hero)
        lava_group.update()
        tp.update()
        boss_group.update(hero, hp, enemies, boss_attacks_group, boss_attacks, all_sprites, enemies_group)
        boss_attacks_group.update(enemies, hero, boss_attacks, hp, enemies_group, all_sprites)
        enemies_group.update(blanks, platforms, [hero.rect.x, hero.rect.y], enemies, enemies_group, all_sprites)
        bullets_group.update(enemies, platforms, bullets)
        for i in all_sprites:
            screen.blit(i.image, camera.apply(i))
        hp.draw(screen)
        pygame.draw.rect(screen, pygame.Color('red'), hero.rect)
        pygame.display.flip()  # обновление и вывод всех изменений на экран
        timer.tick(60)


if __name__ == "__main__":
    main()
