# Импортируем все модули проекта
enemies_group = None
all_sprites = None

import os
import time as timetime

import pygameMenu

from constants import *
from background import *
from pepe_hero import *
import platforms as plat
from enemies import *
# from boss import *
from bullet import *
from animation import *

prev_fps = 0
MODE = 'MENU'
FIRST_TIME = True


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
    global all_sprites, platforms_group, boss_group, blanks_group, player_group, entities_group
    global updating_blocks, level, camera, clock

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
    updating_blocks = {
        plat.Lava: plat.LavaGroup(),
        plat.Spikes: plat.SpikesGroup(),
        plat.Teleport: pygame.sprite.Group()
    }
    player_group = pygame.sprite.Group()
    player_group.add(hero)
    entities_group = pygame.sprite.Group()
    level = load_level("level_1.txt")

    x = y = 0  # координаты
    for row in level:  # вся строка
        for sym in row:  # каждый символ
            if sym == "*":
                p = Platform(x, y, None)
                platforms_group.add(p)
                all_sprites.add(p)
            elif sym in PLATFORMS_LEGEND.keys():
                p = Platform(x, y, f"data/framestiles/tiles/{PLATFORMS_LEGEND[sym]}.png")
                platforms_group.add(p)
                all_sprites.add(p)
            elif sym == "U":
                uka = Uka(x, y)
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
                lava = plat.Lava(x, y, updating_blocks[plat.Lava])
                all_sprites.add(lava)
                platforms_group.add(lava)
                updating_blocks[plat.Lava].add(lava)
            elif sym == "[":
                lava = Lava(x, y, updating_blocks[plat.Lava], "data/framestiles/tiles/lavaleft.png")
                all_sprites.add(lava)
                platforms_group.add(lava)
                updating_blocks[plat.Lava].add(lava)
            elif sym == "]":
                lava = Lava(x, y, updating_blocks[plat.Lava], "data/framestiles/tiles/lavaright.png")
                all_sprites.add(lava)
                platforms_group.add(lava)
                updating_blocks[plat.Lava].add(lava)
            elif sym == "S":
                spikes = plat.Spikes(x, y, "data/framestiles/tiles/spikes.png", updating_blocks[plat.Spikes])
                updating_blocks[plat.Spikes].add(spikes)
                all_sprites.add(spikes)
                platforms_group.add(spikes)
            elif sym == "T":
                tp = plat.Teleport(x, y)
                updating_blocks[plat.Teleport].add(tp)
                all_sprites.add(tp)
            elif sym == "I":
                ice = plat.Ice(x, y, "data/framestiles/tiles/icecenter.png")
                all_sprites.add(ice)
                platforms_group.add(ice)
            elif sym == "(":
                ice = plat.Ice(x, y, "data/framestiles/tiles/iceleft.png")
                all_sprites.add(ice)
                platforms_group.add(ice)
            elif sym == ")":
                ice = plat.Ice(x, y, "data/framestiles/tiles/iceright.png")
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
    clock = pygame.time.Clock()


def start_new_game():
    global MODE, FIRST_TIME, menu, game_submenu
    start_level(CURRENT_LEVEL)
    MODE = 'GAME'
    menu.disable()
    if FIRST_TIME:
        FIRST_TIME = False


def continue_game():
    global MODE, menu, clock
    if FIRST_TIME:
        start_new_game()
    else:
        MODE = 'GAME'
        menu.disable()
        clock = pygame.time.Clock()


def game_cycle(events):
    global hero, hp, left, right, up, down, shoot, hit, enemies_group, bullets_group
    global all_sprites, platforms_group, boss_group, blanks_group, lava_group
    global other_blocks, level, camera, prev_fps, MODE, menu

    if hero.hp <= 0:
        start_level(CURRENT_LEVEL)
    t = clock.tick() / 1000
    for event in events:  # Обрабатываем события
        if event.type == QUIT:
            raise SystemExit("QUIT")
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            MODE = 'MENU'
            menu.enable()
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
    for i in updating_blocks.values():
        i.update(t, on_screen, blanks_group, enemies_group, player_group)
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
    on_screen.remove(on_screen)


def background_fun():
    global screen
    screen.fill((51, 153, 255))


def main():
    global hero, hp, left, right, up, down, shoot, hit, enemies_group, bullets_group
    global all_sprites, platforms_group, boss_group, blanks_group, lava_group
    global other_blocks, level, camera, clock, background, screen, menu, game_submenu

    pygame.init()  # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption("Pepe of Yandex")  # Пишем в шапку
    background = Background('data/Background.jpg', [0, 0], WIN_W, WIN_H)  # фон

    menu_font = pygameMenu.font.FONT_8BIT
    menu = pygameMenu.Menu(screen, 1280, 720, menu_font, 'Pepe of Yandex',
                           bgfun=background_fun, font_size_title=30,
                           menu_alpha=70)
    game_submenu = pygameMenu.Menu(screen, 1280, 720, menu_font, 'Game',
                                   bgfun=background_fun, font_size_title=30,
                                   menu_alpha=70)
    game_submenu.add_option('START NEW GAME', start_new_game)
    game_submenu.add_option('CONTINUE', continue_game)
    menu.add_option('PLAY', game_submenu)
    menu.add_option('QUIT', pygameMenu.events.EXIT)
    start_level(CURRENT_LEVEL)

    while True:  # Основной цикл программы
        events = pygame.event.get()
        if MODE == 'GAME':
            game_cycle(events)
        else:
            menu.mainloop(events)


if __name__ == "__main__":
    main()
