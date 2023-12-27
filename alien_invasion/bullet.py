import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to hold bullet assets"""
    
    def __init__(self, ai_game):
        super().__init__() # this is to initialise the Sprite class for inheritance purpose
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.color = self.settings.bullet_color

        # Draw rectangle & position it at the top-left corner
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)

        # Position bullet
        self.rect.midbottom = ai_game.ship.rect.midtop

        # Setting accurate position of bullet
        self.y = int(self.rect.y)


    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y


    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

    