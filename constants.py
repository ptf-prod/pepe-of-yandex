PLATFORMS_LEGEND = {
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

DEBUG = True
DRAW_HITBOXES = DEBUG and True
DRAW_RECTS = DEBUG and False
SHOW_FPS = DEBUG and True
CURRENT_LEVEL = 'level_1.txt'

# Объявляем константы
WIN_W = 1280  # Ширина создаваемого окна
WIN_H = 720  # Высота
PLAT_W = 32  # Размеры именно закрашенной части платформы, у её картинки в 2 раза больше
PLAT_H = 32
GRAVITY = 400  # px/sec^2
ANIMATION_DELAY = 100
