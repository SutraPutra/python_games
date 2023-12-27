import pygame, random

class Food:
    """Class to hold food attributes & behaviours"""

    def __init__(self, snake_game):
        """Initialize the resources & methods"""
        self.screen = snake_game.screen
        self.screen_rect = self.screen.get_rect()

        self.create_food()


    def create_food(self):
        """Create a food rect & give it a random position on screen"""
        self.rect = pygame.Rect(random.randrange(0, self.screen_rect.width - 20, 20), random.randrange(0, self.screen_rect.height - 20, 20), 20, 20)

    
    
    def draw_food(self):
        """Draw the food on screen"""
        pygame.draw.rect(self.screen, (83,12,89), self.rect)
