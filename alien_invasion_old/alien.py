import pygame
from pygame.sprite import Sprite
import random

class Alien(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, ai_game):
        """Initialise the alien and set its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and set its rect position
        self.image = pygame.image.load("images/alien" + str(random.randint(1,5)) + ".bmp")
        self.rect = self.image.get_rect()

        # Start each alien at the top-left corner of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store the alien's exact horizontal location
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if the alien is at the edge of the screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien to the left or right"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x