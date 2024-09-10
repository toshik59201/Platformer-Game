import pygame
from settings import *


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, player):
        # Center the camera on the player
        x = -player.rect.centerx + int(self.width / 2)
        y = -player.rect.centery + int(self.height / 2)

        # Limit scrolling to map size
        x = min(0, x)  # Left side
        y = min(0, y)  # Top side
        x = max(-(self.width - WIDTH), x)  # Right side
        y = max(-(self.height - HEIGHT), y)  # Bottom side

        self.camera = pygame.Rect(x, y, self.width, self.height)
