import pygame


class Background(pygame.sprite.Sprite):
    def __init__(self, filename, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.transform.scale(pygame.image.load(filename), (800, 640))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location