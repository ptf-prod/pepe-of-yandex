# Импортируем все модули проекта
import time
import pygame
from pygame.constants import *
import pygameMenu

from constants import *
import platforms as plat
import enemies
from background import Background
import pepe_hero
import bullet
from boss import Boss


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
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, rect):
        return rect.x - self.state.x, rect.y - self.state.y

    def update(self, target):
        x = target.rect.x - WIN_W // 2 + PLAT_W // 2
        y = target.rect.y - WIN_H // 2 + PLAT_H // 2  # выравниваем камеру по центру
        x = max(PLAT_W // 2, x)  # Не движемся дальше левой границы
        # x = max(-(camera.width - WIN_WIDTH), x)  # Не движемся дальше правой границы
        # y = max(-(camera.height - WIN_HEIGHT), y)  # Не движемся дальше нижней границы
        y = max(PLAT_H // 2, y)  # Не движемся дальше верхней границы
        self.state.topleft = (x, y)


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip('\n') for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками (' ')
    return list(map(lambda x: x.ljust(max_width, ' '), level_map))


def start_level(level_name):
    global hero, hp, left, right, up, down, shoot, hit, enemies_group, bullets_group
    global all_sprites, platforms_group, boss_group, blanks_group, player_group, entities_group
    global updating_blocks, level, camera, clock, edge_platforms, boss_attacks, boss_attacks_group

    hero = None
    left = right = up = down = shoot = hit = False  # по умолчанию — стоим
    enemies_group = pygame.sprite.Group()
    bullets_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    platforms_group = pygame.sprite.Group()
    boss_group = pygame.sprite.Group()
    boss_attacks_group = pygame.sprite.Group()
    boss_attacks = []
    blanks_group = pygame.sprite.Group()
    edge_platforms = pygame.sprite.Group()
    updating_blocks = {
        plat.Lava: plat.LavaGroup(),
        plat.Spikes: plat.SpikesGroup(),
        plat.Teleport: pygame.sprite.Group()
    }
    player_group = pygame.sprite.Group()
    entities_group = pygame.sprite.Group()
    level = load_level(CURRENT_LEVEL)

    for i, row in enumerate(level):  # вся строка
        for j, sym in enumerate(row):  # каждый символ
            if sym == "P":
                hero = pepe_hero.Player(j * PLAT_W, i * PLAT_H - PLAT_H * 3 // 2)
    if hero is None:
        hero = pepe_hero.Player(55, 555)
    all_sprites.add(hero)
    player_group.add(hero)
    hp = pepe_hero.HitPoints(hero.hp)

    for i, row in enumerate(level):  # вся строка
        for j, sym in enumerate(row):  # каждый символ
            p = None
            if sym == "*":
                p = plat.Platform(j * PLAT_W, i * PLAT_H, None)
                platforms_group.add(p)
                all_sprites.add(p)
            elif sym in PLATFORMS_LEGEND.keys():
                p = plat.Platform(j * PLAT_W, i * PLAT_H, f"data/framestiles/tiles/{PLATFORMS_LEGEND[sym]}.png")
                platforms_group.add(p)
                all_sprites.add(p)
            elif sym == "U":
                uka = enemies.Uka(j * PLAT_W, i * PLAT_H)
                entities_group.add(uka)
                all_sprites.add(uka)
            elif sym == "b":
                blank = plat.Trigger(j * PLAT_W, i * PLAT_H)
                blanks_group.add(blank)
                all_sprites.add(blank)
            elif sym == "F":
                flyling = enemies.Flyling(j * PLAT_W, i * PLAT_H, entities_group, all_sprites)
                entities_group.add(flyling)
                all_sprites.add(flyling)
            elif sym == "L":
                p = plat.Lava(j * PLAT_W, i * PLAT_H, updating_blocks[plat.Lava])
                all_sprites.add(p)
                platforms_group.add(p)
                updating_blocks[plat.Lava].add(p)
            elif sym == "[":
                p = plat.Lava(j * PLAT_W, i * PLAT_H, updating_blocks[plat.Lava], "data/framestiles/tiles/lavaleft.png")
                all_sprites.add(p)
                platforms_group.add(p)
                updating_blocks[plat.Lava].add(p)
            elif sym == "]":
                p = plat.Lava(j * PLAT_W, i * PLAT_H, updating_blocks[plat.Lava],
                              "data/framestiles/tiles/lavaright.png")
                all_sprites.add(p)
                platforms_group.add(p)
                updating_blocks[plat.Lava].add(p)
            elif sym == "S":
                p = plat.Spikes(j * PLAT_W, i * PLAT_H, "data/framestiles/tiles/spikes.png",
                                updating_blocks[plat.Spikes])
                updating_blocks[plat.Spikes].add(p)
                all_sprites.add(p)
                platforms_group.add(p)
            elif sym == "T":
                p = plat.Teleport(j * PLAT_W, i * PLAT_H)
                updating_blocks[plat.Teleport].add(p)
                all_sprites.add(p)
            elif sym == "I":
                p = plat.Ice(j * PLAT_W, i * PLAT_H, "data/framestiles/tiles/icecentre.png")
                all_sprites.add(p)
                platforms_group.add(p)
            elif sym == "(":
                p = plat.Ice(j * PLAT_W, i * PLAT_H, "data/framestiles/tiles/iceleft.png")
                all_sprites.add(p)
                platforms_group.add(p)
            elif sym == ")":
                p = plat.Ice(j * PLAT_W, i * PLAT_H, "data/framestiles/tiles/iceright.png")
                all_sprites.add(p)
                platforms_group.add(p)
            elif sym == "C":
                crack = enemies.Crackatoo(j * PLAT_W, i * PLAT_H)
                all_sprites.add(crack)
                entities_group.add(crack)
            elif sym == "B":
                 boss = Boss(j * PLAT_W, i * PLAT_H)
                 all_sprites.add(boss)
                 boss_group.add(boss)
            if isinstance(p, plat.Platform):
                edge = False
                for q in level[max(0, i - 1):i + 2]:
                    for w in q[max(0, j - 1):j + 2]:
                        if w not in PLATFORMS_LEGEND.keys() and w not in '[L]S(I)*':
                            edge = True
                            break
                if edge:
                    edge_platforms.add(p)

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


def game_over():
    global MODE, FIRST_TIME
    game_over_menu.enable()
    MODE = 'GAME_OVER'
    FIRST_TIME = True


def back(menu_2):
    def f():
        global MODE
        menu_2.disable()
        menu.enable()
        MODE = 'MENU'
    return f


def game_cycle(events):
    global hero, hp, left, right, up, down, shoot, hit, enemies_group, bullets_group
    global all_sprites, platforms_group, boss_group, blanks_group, lava_group
    global other_blocks, level, camera, prev_fps, MODE, menu, edge_platforms, boss_attacks, boss_attacks_group

    if hero.hp <= 0:
        game_over()
    t = clock.tick() / 1000 * TIMESCALE
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
    hero.update(t, on_screen, blanks_group, entities_group, player_group)
    camera.update(hero)
    for i in updating_blocks.values():
        i.update(t, on_screen, blanks_group, enemies_group, player_group)
    boss_group.update(hero, hp, enemies_group, boss_attacks_group,
                       boss_attacks, all_sprites, enemies_group)
    boss_attacks_group.update(enemies_group, hero, boss_attacks,
                               hp, enemies_group, all_sprites)
    enemies_group.update(t, platforms_group, blanks_group, entities_group, player_group)
    entities_group.update(t, edge_platforms, blanks_group, entities_group, player_group)
    bullets_group.update(t, platforms_group, blanks_group, entities_group, player_group)

    if time.time() * TIMESCALE - hero.shoot_start > 1 and shoot is True and hero.on_ground \
            or time.time() * TIMESCALE - hero.shoot_start > 5 and shoot:
        if DEBUG:
            print("bullet")
        if hero.right:
            b = bullet.Bullet(hero.hitbox.right + 5, hero.hitbox.y + hero.hitbox.height // 8 * 3, True)
        else:
            b = bullet.Bullet(hero.hitbox.left - 5, hero.hitbox.y + hero.hitbox.height // 8 * 3, False)
        entities_group.add(b)
        all_sprites.add(b)
        hero.shoot_start = time.time() * TIMESCALE
    if hit and not hero.hit:
        hero.start_hit()

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
                if isinstance(i, plat.Trigger):
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


def background_fun(color):
    def f():
        screen.fill(color)
    return f


def main():
    global hero, hp, left, right, up, down, shoot, hit, enemies_group, bullets_group
    global all_sprites, platforms_group, boss_group, blanks_group, lava_group
    global other_blocks, level, camera, clock, background, screen, menu, game_submenu, boss_attacks, boss_attacks_group
    global game_over_menu, you_win_menu

    pygame.init()  # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption("Pepe of Yandex")  # Пишем в шапку
    background = Background('data/Background.jpg', [0, 0], WIN_W, WIN_H)  # фон

    menu_font = pygameMenu.font.FONT_8BIT
    menu = pygameMenu.Menu(screen, 1280, 720, menu_font, 'Pepe of Yandex',
                           bgfun=background_fun((51, 153, 255)), font_size_title=30,
                           menu_alpha=70)
    game_submenu = pygameMenu.Menu(screen, 1280, 720, menu_font, 'Play',
                                   bgfun=background_fun((51, 153, 255)), font_size_title=30,
                                   menu_alpha=70)
    game_submenu.add_option('Start new game', start_new_game)
    game_submenu.add_option('Continue', continue_game)
    game_submenu.add_option('Back', pygameMenu.events.BACK)
    menu.add_option('Play', game_submenu)
    menu.add_option('Quit', pygameMenu.events.EXIT)

    game_over_menu = pygameMenu.Menu(screen, 1280, 720, menu_font, 'Game Over',
                                     bgfun=background_fun((250, 128, 114)), font_size_title=30,
                                     menu_alpha=70)
    game_over_menu.add_option('Back', back(game_over_menu))

    you_win_menu = pygameMenu.Menu(screen, 1280, 720, menu_font, 'You Win',
                                   bgfun=background_fun((0, 255, 127)), font_size_title=30,
                                   menu_alpha=70)
    you_win_menu.add_option('Back', back(you_win_menu))

    while True:  # Основной цикл программы
        events = pygame.event.get()
        if MODE == 'GAME':
            game_cycle(events)
        elif MODE == 'MENU':
            menu.mainloop(events)
        elif MODE == 'GAME_OVER':
            game_over_menu.mainloop(events)
        elif MODE == 'YOU_WIN':
            you_win_menu.mainloop(events)


if __name__ == "__main__":
    main()
