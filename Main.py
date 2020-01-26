# -*- coding: utf-8 -*-

# Импортируем библиотеку pygame
from PepeHero import *
from Platforms import *
from Enemies import *

# Объявляем переменные
WIN_WIDTH = 800  # Ширина создаваемого окна
WIN_HEIGHT = 640  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = (50, 150, 255)
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    x, y = target_rect[0], target_rect[1]
    w, h = camera[2], camera[3]
    x, y = -x + WIN_WIDTH / 2, -y + WIN_HEIGHT / 2

    x = min(0, x)  # Не движемся дальше левой границы
    x = max(-(camera.width - WIN_WIDTH), x)  # Не движемся дальше правой границы
    y = max(-(camera.height - WIN_HEIGHT), y)  # Не движемся дальше нижней границы
    y = min(0, y)  # Не движемся дальше верхней границы
    return Rect(x, y, w, h)


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def main():
    pygame.init()  # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
    pygame.display.set_caption("Pepe the Frog")  # Пишем в шапку
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности
    # будем использовать как фон
    bg.fill(BACKGROUND_COLOR)  # Заливаем поверхность сплошным цветом
    hero = Player(55, 55)
    hp = HitPoints()

    # создаем героя по (x,y) координатам
    left = right = up = down = blast = False  # по умолчанию — стоим
    enemies_group = pygame.sprite.Group()
    bullets_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    platforms = []  # то, во что мы будем врезаться или опираться
    enemies = []  # Враги
    blanks = []
    other_blocks = []
    bullets = []
    all_sprites.add(hero)
    timer = pygame.time.Clock()
    level = load_level("level.txt")

    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                plat = Platform(x, y)
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
            elif col == "S":
                spikes = Spikes(x, y)
                other_blocks.append(spikes)
                all_sprites.add(spikes)
            elif col == "I":
                ice = Ice(x, y)
                platforms.append(ice)
                all_sprites.add(ice)
            elif col == "C":
                crack = Crackatoo(x, y)
                all_sprites.add(crack)
                enemies.append(crack)
                enemies_group.add(crack)


            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)

    while 1:  # Основной цикл программы
        for event in pygame.event.get():  # Обрабатываем события
            if event.type == QUIT:
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
                hero.hit(enemies)
            if event.type == KEYDOWN and event.key == K_z:
                blast = True
            elif event.type == KEYUP and event.key == K_z:
                blast = False
        if hero.shot_done is False and blast is True:
            bullet = Bullet(hero.rect.x, hero.rect.y + 14, hero.previosly_move)
            bullets.append(bullet)
            bullets_group.add(bullet)
            all_sprites.add(bullet)
            hero.shot_done = True
        screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать

        hero.update(left, right, up, platforms, down, enemies, screen, hp, other_blocks)  # передвижение
        camera.update(hero)
        enemies_group.update(blanks, platforms, (hero.rect.x, hero.rect.y))
        bullets_group.update(enemies, platforms, bullets)
        for i in all_sprites:
            screen.blit(i.image, camera.apply(i))
        hp.draw(screen)
        pygame.display.update()  # обновление и вывод всех изменений на экран
        timer.tick(60)


if __name__ == "__main__":
    main()
