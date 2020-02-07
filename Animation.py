from os.path import join as pjoin

import pygame
import pyganim


def load_animation(start, end, delay, *args):
    path = pjoin(*args)
    anim = []
    for i in range(start, end):
        p = path.format(i)
        anim.append((pygame.transform.scale(pygame.image.load(p).convert_alpha(), (128, 128)), delay))
    anim = pyganim.PygAnimation(anim)
    anim.play()
    return anim
