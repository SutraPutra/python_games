import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Class to manage the alien sprite & behaviours"""

    def __init__(self, ai_game):
        """Initialise game assets & resources"""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings

        # Load the alien image & get its rect
        self.image = pygame.image.load("./images/alien1.png")
        self.rect = self.image.get_rect()

        # position the rect
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Setting a variable to capture accurate position of rect.x
        self.x = self.rect.x

    def check_edges(self):
        """Returns true if the alien has hit any screen edge"""
        if self.rect.right >= self.screen_rect.right or self.rect.left <= 0:
            return True


    def update(self):
        """Updates the position of the alien"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

