import pygame
from pygame.sprite import Sprite

class ShipLife(Sprite):
    """Class to hold the life sprite"""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Load the life image & get its rect & then position it
        self.image = pygame.image.load('images/life.png')
        self.rect = self.image.get_rect()