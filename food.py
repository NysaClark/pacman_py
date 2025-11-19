# food.py
import pygame
from settings import CHAR_SIZE

class Food(pygame.sprite.Sprite):
    def __init__(self, row, col, type, points):
        super().__init__()
        self.type = type
        self.points = points
        self.image = pygame.image.load(f"assets/food/{type}.png")
        self.image = pygame.transform.scale(self.image, (CHAR_SIZE, CHAR_SIZE))
        self.rect = self.image.get_rect(topleft=(col * CHAR_SIZE, row * CHAR_SIZE))