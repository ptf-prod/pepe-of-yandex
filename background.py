import pygame


class Background(pygame.sprite.Sprite):
    def __init__(self, filename, location, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(filename), (w, h))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
