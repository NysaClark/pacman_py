import pygame

from settings import CHAR_SIZE

class Cherry(pygame.sprite.Sprite):
    def __init__(self, row, col):
        super().__init__()
        self.image = pygame.image.load("assets/cherry/cherry.png")
        self.image = pygame.transform.scale(self.image, (CHAR_SIZE, CHAR_SIZE))
        self.rect = self.image.get_rect(topleft=(col * CHAR_SIZE, row * CHAR_SIZE))