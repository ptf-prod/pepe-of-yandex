from os.path import join as pjoin

import pygame
import pyganim


def load_animation(start, end, delay, *args, flip=False, size=(128, 128)):
    path = pjoin(*args)
    anim = []
    for i in range(start, end):
        p = path.format(i)
        anim.append((pygame.transform.scale(
            pygame.transform.flip(pygame.image.load(p).convert_alpha(),
                                  flip, 0), size), delay))
    anim = pyganim.PygAnimation(anim)
    anim.pause()
    return anim
